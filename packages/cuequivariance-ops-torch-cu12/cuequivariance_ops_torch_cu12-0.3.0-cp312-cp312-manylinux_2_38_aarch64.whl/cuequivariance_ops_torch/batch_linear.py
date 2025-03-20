# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import math
from typing import List, Optional

import numpy as np
import torch
import torch.nn as nn

import cuequivariance_ops_torch._ext as ops
from cuequivariance_ops_torch.utils import (
    get_operator_from_module,
    maybe_detach,
    maybe_empty_like,
)

float_int_mappings = {
    torch.bfloat16: torch.int16,
    torch.float16: torch.uint16,
    torch.float32: torch.int32,
    torch.float64: torch.int64,
}

int_float_mappings = {v: k for k, v in float_int_mappings.items()}

linear_mode_mappings = {
    "uv_v_u": 0,
    "u_uv_v": 1,
}


def _make_batch_linear_info(
    operand_segment_modes,
    path_indices,
    path_coefficients,
    tensor_w_offsets,
    tensor_w_shapes,
    math_dtype,
):
    key_index = operand_segment_modes.index("uv")

    num_w_segments = len(tensor_w_offsets)
    w_offsets_segment_map = dict(zip(tensor_w_offsets, range(num_w_segments)))

    sorted_indices_vals = sorted(
        zip(path_indices, path_coefficients), key=lambda x: x[0][key_index]
    )

    new_path_indices, new_path_vals = [], []
    for index, val in sorted_indices_vals:
        if key_index == 0:
            new_index = [index[2], index[1]]
        if key_index == 1:
            new_index = ([index[2], index[0]],)
        elif key_index == 2:
            new_index = [index[0], index[1]]
        new_path_indices.append(new_index)
        new_path_vals.append(val)

    curr_w_segment = -1
    path_start, path_end, path_num = 0, 0, 0
    tensor_w_layouts = torch.zeros((num_w_segments, 2), dtype=torch.int32)
    index_offsets = torch.zeros((num_w_segments, 2), dtype=torch.int32)

    for index, val in sorted_indices_vals:
        new_w_segment = w_offsets_segment_map[index[key_index]]
        if curr_w_segment == -1:
            curr_w_segment = new_w_segment
            path_num = 1
        elif curr_w_segment == new_w_segment:
            path_num = path_num + 1
        elif curr_w_segment != new_w_segment:
            path_end = path_start + path_num
            index_offsets[curr_w_segment] = torch.tensor([path_start, path_end])
            path_num = 1
            path_start = path_end
            shapes = tensor_w_shapes[curr_w_segment]

            layout = torch.tensor([shapes[0], shapes[1]])
            tensor_w_layouts[curr_w_segment] = layout

            curr_w_segment = new_w_segment
        else:
            raise AssertionError(
                "Unexpected value of curr_output and path index", curr_w_segment, index
            )
    if curr_w_segment != -1:
        path_end = path_start + path_num
        index_offsets[curr_w_segment] = torch.tensor([path_start, path_end])
        shapes = tensor_w_shapes[curr_w_segment]

        layout = torch.tensor([shapes[0], shapes[1]])
        tensor_w_layouts[curr_w_segment] = layout

    return (
        tensor_w_layouts.flatten().contiguous(),
        index_offsets.flatten().contiguous(),
        torch.tensor(new_path_indices, dtype=torch.int32).flatten().contiguous(),
        torch.tensor(new_path_vals, dtype=math_dtype).contiguous(),
    )


# derivative with respect to operand symbol 'u'
def _diff_imp_u(operand_id, x):
    return [x[-1]] + x[0:operand_id] + x[operand_id + 1 : -1] + [x[operand_id]]


# derivative with respect to operand symbol 'v'
def _diff_imp_v(operand_id, x):
    return x[0:operand_id] + x[operand_id + 1 :] + [x[operand_id]]


# derivative with respect to operand symbol 'uv'
def _dif_imp_uv(operand_id, x):
    return x[0:operand_id] + [x[-1]] + x[operand_id + 1 : -1] + [x[operand_id]]


# perform the derivative with respect to the two input operands and the output operands
def _diff_operand_list(operand_id, operand_segment_modes, path_indices):
    diff_func = None
    if operand_segment_modes[-1] == "u":
        diff_func = _diff_imp_u
    elif operand_segment_modes[-1] == "v":
        diff_func = _diff_imp_v
    elif operand_segment_modes[-1] == "uv":
        diff_func = _dif_imp_uv

    new_operand_segment_modes = diff_func(operand_id, operand_segment_modes)
    new_path_indices = [diff_func(operand_id, index) for index in path_indices]

    return new_operand_segment_modes, new_path_indices


def _compute_alignments(operand_segment_modes, operand_segment_shapes):
    in_op_id = 0 if operand_segment_modes.index("uv") == 1 else 1
    out_op_id = 2

    align_in = 16
    for shape in operand_segment_shapes[in_op_id]:
        while shape[0] % align_in != 0 and align_in > 0:
            align_in = align_in // 2

    align_out = 16
    for shape in operand_segment_shapes[out_op_id]:
        while shape[0] % align_out != 0 and align_out > 0:
            align_out = align_out // 2

    return align_in, align_out


def _compute_stride(shapes):
    return sum([math.prod(shape) for shape in shapes])


def batch_linear_info(layouts, index_offsets, indices, alpha, math_dtype):
    make_batch_linear_info = get_operator_from_module(
        ops, "make_batch_linear_info", (math_dtype,)
    )
    return make_batch_linear_info(
        layouts,
        index_offsets,
        indices,
        alpha.view(math_dtype),
    )


class BatchLinearInfo(nn.Module):
    def __init__(
        self,
        operand_segment_modes,
        path_indices,
        path_coefficients,
        tensor_w_offsets,
        tensor_w_shapes,
        math_dtype,
    ):
        super().__init__()

        layouts, index_offsets, indices, alpha = _make_batch_linear_info(
            operand_segment_modes,
            path_indices,
            path_coefficients,
            tensor_w_offsets,
            tensor_w_shapes,
            math_dtype,
        )

        self.register_buffer("layouts", layouts)
        self.register_buffer("index_offsets", index_offsets)
        self.register_buffer("indices", indices)
        self.register_buffer("alpha", alpha.view(dtype=float_int_mappings[math_dtype]))

    @torch.jit.ignore
    def forward(self):
        raise NotImplementedError(
            "BatchLinearInfo module is not intended to be called."
        )


@torch.library.custom_op(
    "cuequivariance_ops_torch::batch_linear_fwd_primitive",
    mutates_args=(),
    device_types="cuda",
)
def _(
    tensor_in: torch.Tensor,
    tensor_w: torch.Tensor,
    tensor_w_id: Optional[torch.Tensor],
    tensor_w_offsets: torch.Tensor,
    layouts_fwd: torch.Tensor,
    index_offsets_fwd: torch.Tensor,
    indices_fwd: torch.Tensor,
    alpha_fwd: torch.Tensor,
    layouts_grad_in: torch.Tensor,
    index_offsets_grad_in: torch.Tensor,
    indices_grad_in: torch.Tensor,
    alpha_grad_in: torch.Tensor,
    layouts_grad_w: torch.Tensor,
    index_offsets_grad_w: torch.Tensor,
    indices_grad_w: torch.Tensor,
    alpha_grad_w: torch.Tensor,
    layouts_grad_in_grad_w: torch.Tensor,
    index_offsets_grad_in_grad_w: torch.Tensor,
    indices_grad_in_grad_w: torch.Tensor,
    alpha_grad_in_grad_w: torch.Tensor,
    layouts_grad_in_grad_grad_out: torch.Tensor,
    index_offsets_grad_in_grad_grad_out: torch.Tensor,
    indices_grad_in_grad_grad_out: torch.Tensor,
    alpha_grad_in_grad_grad_out: torch.Tensor,
    layouts_grad_w_grad_in: torch.Tensor,
    index_offsets_grad_w_grad_in: torch.Tensor,
    indices_grad_w_grad_in: torch.Tensor,
    alpha_grad_w_grad_in: torch.Tensor,
    layouts_grad_w_grad_grad_out: torch.Tensor,
    index_offsets_grad_w_grad_grad_out: torch.Tensor,
    indices_grad_w_grad_grad_out: torch.Tensor,
    alpha_grad_w_grad_grad_out: torch.Tensor,
    op_mode: int,
    weight_shared_mode: int,
    tensor_in_stride: int,
    tensor_w_stride: int,
    tensor_out_stride: int,
    num_w_segments: int,
    align_in: int,
    align_out: int,
) -> torch.Tensor:
    num_batches = tensor_in.shape[0]
    tensor_out = torch.empty(
        (num_batches, tensor_out_stride),
        dtype=tensor_in.dtype,
        device=tensor_in.device,
    )
    math_dtype = int_float_mappings[alpha_fwd.dtype]
    fwd_func = get_operator_from_module(
        ops,
        "batch_linear_fwd",
        (
            tensor_out.dtype,
            tensor_in.dtype,
            tensor_w.dtype,
            math_dtype,
        ),
    )
    batch_linear_info_fwd = batch_linear_info(
        layouts_fwd, index_offsets_fwd, indices_fwd, alpha_fwd, math_dtype
    )
    stream = torch.cuda.current_stream().cuda_stream

    fwd_func(
        tensor_out,
        maybe_detach(tensor_in),
        maybe_detach(tensor_w),
        maybe_detach(tensor_w_id),
        maybe_detach(tensor_w_offsets),
        batch_linear_info_fwd,
        op_mode,
        weight_shared_mode,
        num_w_segments,
        align_in,
        align_out,
        stream_id=stream,
    )

    return tensor_out


@torch.library.register_fake("cuequivariance_ops_torch::batch_linear_fwd_primitive")
def _(
    tensor_in: torch.Tensor,
    tensor_w: torch.Tensor,
    tensor_w_id: Optional[torch.Tensor],
    tensor_w_offsets: torch.Tensor,
    layouts_fwd: torch.Tensor,
    index_offsets_fwd: torch.Tensor,
    indices_fwd: torch.Tensor,
    alpha_fwd: torch.Tensor,
    layouts_grad_in: torch.Tensor,
    index_offsets_grad_in: torch.Tensor,
    indices_grad_in: torch.Tensor,
    alpha_grad_in: torch.Tensor,
    layouts_grad_w: torch.Tensor,
    index_offsets_grad_w: torch.Tensor,
    indices_grad_w: torch.Tensor,
    alpha_grad_w: torch.Tensor,
    layouts_grad_in_grad_w: torch.Tensor,
    index_offsets_grad_in_grad_w: torch.Tensor,
    indices_grad_in_grad_w: torch.Tensor,
    alpha_grad_in_grad_w: torch.Tensor,
    layouts_grad_in_grad_grad_out: torch.Tensor,
    index_offsets_grad_in_grad_grad_out: torch.Tensor,
    indices_grad_in_grad_grad_out: torch.Tensor,
    alpha_grad_in_grad_grad_out: torch.Tensor,
    layouts_grad_w_grad_in: torch.Tensor,
    index_offsets_grad_w_grad_in: torch.Tensor,
    indices_grad_w_grad_in: torch.Tensor,
    alpha_grad_w_grad_in: torch.Tensor,
    layouts_grad_w_grad_grad_out: torch.Tensor,
    index_offsets_grad_w_grad_grad_out: torch.Tensor,
    indices_grad_w_grad_grad_out: torch.Tensor,
    alpha_grad_w_grad_grad_out: torch.Tensor,
    op_mode: int,
    weight_shared_mode: int,
    tensor_in_stride: int,
    tensor_w_stride: int,
    tensor_out_stride: int,
    num_w_segments: int,
    align_in: int,
    align_out: int,
) -> torch.Tensor:
    num_batches = tensor_in.shape[0]
    return torch.empty(
        (num_batches, tensor_out_stride),
        dtype=tensor_in.dtype,
        device=tensor_in.device,
    )


@torch.library.custom_op(
    "cuequivariance_ops_torch::batch_linear_bwd_primitive",
    mutates_args=(),
    device_types="cuda",
)
def _(
    grad_tensor_out: torch.Tensor,
    tensor_in: torch.Tensor,
    tensor_w: torch.Tensor,
    tensor_w_id: Optional[torch.Tensor],
    tensor_w_offsets: torch.Tensor,
    layouts_fwd: torch.Tensor,
    index_offsets_fwd: torch.Tensor,
    indices_fwd: torch.Tensor,
    alpha_fwd: torch.Tensor,
    layouts_grad_in: torch.Tensor,
    index_offsets_grad_in: torch.Tensor,
    indices_grad_in: torch.Tensor,
    alpha_grad_in: torch.Tensor,
    layouts_grad_w: torch.Tensor,
    index_offsets_grad_w: torch.Tensor,
    indices_grad_w: torch.Tensor,
    alpha_grad_w: torch.Tensor,
    layouts_grad_in_grad_w: torch.Tensor,
    index_offsets_grad_in_grad_w: torch.Tensor,
    indices_grad_in_grad_w: torch.Tensor,
    alpha_grad_in_grad_w: torch.Tensor,
    layouts_grad_in_grad_grad_out: torch.Tensor,
    index_offsets_grad_in_grad_grad_out: torch.Tensor,
    indices_grad_in_grad_grad_out: torch.Tensor,
    alpha_grad_in_grad_grad_out: torch.Tensor,
    layouts_grad_w_grad_in: torch.Tensor,
    index_offsets_grad_w_grad_in: torch.Tensor,
    indices_grad_w_grad_in: torch.Tensor,
    alpha_grad_w_grad_in: torch.Tensor,
    layouts_grad_w_grad_grad_out: torch.Tensor,
    index_offsets_grad_w_grad_grad_out: torch.Tensor,
    indices_grad_w_grad_grad_out: torch.Tensor,
    alpha_grad_w_grad_grad_out: torch.Tensor,
    op_mode: int,
    weight_shared_mode: int,
    tensor_in_stride: int,
    tensor_w_stride: int,
    tensor_out_stride: int,
    num_w_segments: int,
    align_in: int,
    align_out: int,
    needs_grad_in: bool,
    needs_grad_w: bool,
) -> List[torch.Tensor]:
    math_dtype = int_float_mappings[alpha_fwd.dtype]
    grad_tensor_in = maybe_empty_like(tensor_in, needs_grad_in)
    grad_tensor_w = maybe_empty_like(tensor_w, needs_grad_w, dtype=math_dtype)

    stream = torch.cuda.current_stream().cuda_stream

    batch_linear_info_grad_in = batch_linear_info(
        layouts_grad_in,
        index_offsets_grad_in,
        indices_grad_in,
        alpha_grad_in,
        math_dtype,
    )
    batch_linear_info_grad_w = batch_linear_info(
        layouts_grad_w, index_offsets_grad_w, indices_grad_w, alpha_grad_w, math_dtype
    )

    bwd_func = get_operator_from_module(
        ops,
        "batch_linear_bwd",
        (
            grad_tensor_out.dtype,
            tensor_in.dtype,
            tensor_w.dtype,
            math_dtype,
        ),
    )

    stream = torch.cuda.current_stream().cuda_stream

    grad_tensor_out = maybe_detach(grad_tensor_out)
    tensor_in = maybe_detach(tensor_in)
    tensor_w = maybe_detach(tensor_w)

    bwd_func(
        grad_tensor_in,
        grad_tensor_w,
        maybe_detach(grad_tensor_out),
        maybe_detach(tensor_in),
        maybe_detach(tensor_w),
        maybe_detach(tensor_w_id),
        maybe_detach(tensor_w_offsets),
        batch_linear_info_grad_in,
        batch_linear_info_grad_w,
        op_mode,
        weight_shared_mode,
        num_w_segments,
        align_in,
        align_out,
        stream,
    )

    grad_tensor_w = (
        grad_tensor_w.to(tensor_w.dtype) if grad_tensor_w is not None else None
    )

    grads = []
    if grad_tensor_in is not None:
        grads.append(grad_tensor_in)
    if grad_tensor_w is not None:
        grads.append(grad_tensor_w)

    return grads


@torch.library.register_fake("cuequivariance_ops_torch::batch_linear_bwd_primitive")
def _(
    grad_tensor_out: torch.Tensor,
    tensor_in: torch.Tensor,
    tensor_w: torch.Tensor,
    tensor_w_id: Optional[torch.Tensor],
    tensor_w_offsets: torch.Tensor,
    layouts_fwd: torch.Tensor,
    index_offsets_fwd: torch.Tensor,
    indices_fwd: torch.Tensor,
    alpha_fwd: torch.Tensor,
    layouts_grad_in: torch.Tensor,
    index_offsets_grad_in: torch.Tensor,
    indices_grad_in: torch.Tensor,
    alpha_grad_in: torch.Tensor,
    layouts_grad_w: torch.Tensor,
    index_offsets_grad_w: torch.Tensor,
    indices_grad_w: torch.Tensor,
    alpha_grad_w: torch.Tensor,
    layouts_grad_in_grad_w: torch.Tensor,
    index_offsets_grad_in_grad_w: torch.Tensor,
    indices_grad_in_grad_w: torch.Tensor,
    alpha_grad_in_grad_w: torch.Tensor,
    layouts_grad_in_grad_grad_out: torch.Tensor,
    index_offsets_grad_in_grad_grad_out: torch.Tensor,
    indices_grad_in_grad_grad_out: torch.Tensor,
    alpha_grad_in_grad_grad_out: torch.Tensor,
    layouts_grad_w_grad_in: torch.Tensor,
    index_offsets_grad_w_grad_in: torch.Tensor,
    indices_grad_w_grad_in: torch.Tensor,
    alpha_grad_w_grad_in: torch.Tensor,
    layouts_grad_w_grad_grad_out: torch.Tensor,
    index_offsets_grad_w_grad_grad_out: torch.Tensor,
    indices_grad_w_grad_grad_out: torch.Tensor,
    alpha_grad_w_grad_grad_out: torch.Tensor,
    op_mode: int,
    weight_shared_mode: int,
    tensor_in_stride: int,
    tensor_w_stride: int,
    tensor_out_stride: int,
    num_w_segments: int,
    align_in: int,
    align_out: int,
    needs_grad_in: bool,
    needs_grad_w: bool,
) -> List[torch.Tensor]:
    grad_tensor_in = maybe_empty_like(tensor_in, needs_grad_in)
    grad_tensor_w = maybe_empty_like(tensor_w, needs_grad_w)

    grads = []
    if grad_tensor_in is not None:
        grads.append(grad_tensor_in)
    if grad_tensor_w is not None:
        grads.append(grad_tensor_w)

    return grads


@torch.library.custom_op(
    "cuequivariance_ops_torch::batch_linear_bwd_bwd_primitive",
    mutates_args=(),
    device_types="cuda",
)
def _(
    grad_grad_tensor_in: Optional[torch.Tensor],
    grad_grad_tensor_w: Optional[torch.Tensor],
    grad_tensor_out: torch.Tensor,
    tensor_in: torch.Tensor,
    tensor_w: torch.Tensor,
    tensor_w_id: Optional[torch.Tensor],
    tensor_w_offsets: torch.Tensor,
    layouts_fwd: torch.Tensor,
    index_offsets_fwd: torch.Tensor,
    indices_fwd: torch.Tensor,
    alpha_fwd: torch.Tensor,
    layouts_grad_in: torch.Tensor,
    index_offsets_grad_in: torch.Tensor,
    indices_grad_in: torch.Tensor,
    alpha_grad_in: torch.Tensor,
    layouts_grad_w: torch.Tensor,
    index_offsets_grad_w: torch.Tensor,
    indices_grad_w: torch.Tensor,
    alpha_grad_w: torch.Tensor,
    layouts_grad_in_grad_w: torch.Tensor,
    index_offsets_grad_in_grad_w: torch.Tensor,
    indices_grad_in_grad_w: torch.Tensor,
    alpha_grad_in_grad_w: torch.Tensor,
    layouts_grad_in_grad_grad_out: torch.Tensor,
    index_offsets_grad_in_grad_grad_out: torch.Tensor,
    indices_grad_in_grad_grad_out: torch.Tensor,
    alpha_grad_in_grad_grad_out: torch.Tensor,
    layouts_grad_w_grad_in: torch.Tensor,
    index_offsets_grad_w_grad_in: torch.Tensor,
    indices_grad_w_grad_in: torch.Tensor,
    alpha_grad_w_grad_in: torch.Tensor,
    layouts_grad_w_grad_grad_out: torch.Tensor,
    index_offsets_grad_w_grad_grad_out: torch.Tensor,
    indices_grad_w_grad_grad_out: torch.Tensor,
    alpha_grad_w_grad_grad_out: torch.Tensor,
    op_mode: int,
    weight_shared_mode: int,
    tensor_in_stride: int,
    tensor_w_stride: int,
    tensor_out_stride: int,
    num_w_segments: int,
    align_in: int,
    align_out: int,
    needs_grad_in: bool,
    needs_grad_w: bool,
) -> List[torch.Tensor]:
    math_dtype = int_float_mappings[alpha_fwd.dtype]
    grad_grad_tensor_out = torch.empty_like(grad_tensor_out)
    grad_tensor_in = maybe_empty_like(tensor_in, needs_grad_in)
    grad_tensor_w = maybe_empty_like(tensor_w, needs_grad_w, dtype=math_dtype)

    bwd_bwd_func = get_operator_from_module(
        ops,
        "batch_linear_bwd_bwd",
        (
            grad_tensor_out.dtype,
            tensor_in.dtype,
            tensor_w.dtype,
            math_dtype,
        ),
    )

    batch_linear_info_grad_in_grad_w = batch_linear_info(
        layouts_grad_in_grad_w,
        index_offsets_grad_in_grad_w,
        indices_grad_in_grad_w,
        alpha_grad_in_grad_w,
        math_dtype,
    )
    batch_linear_info_grad_in_grad_grad_out = batch_linear_info(
        layouts_grad_in_grad_grad_out,
        index_offsets_grad_in_grad_grad_out,
        indices_grad_in_grad_grad_out,
        alpha_grad_in_grad_grad_out,
        math_dtype,
    )
    batch_linear_info_grad_w_grad_in = batch_linear_info(
        layouts_grad_w_grad_in,
        index_offsets_grad_w_grad_in,
        indices_grad_w_grad_in,
        alpha_grad_w_grad_in,
        math_dtype,
    )
    batch_linear_info_grad_w_grad_grad_out = batch_linear_info(
        layouts_grad_w_grad_grad_out,
        index_offsets_grad_w_grad_grad_out,
        indices_grad_w_grad_grad_out,
        alpha_grad_w_grad_grad_out,
        math_dtype,
    )

    stream = torch.cuda.current_stream().cuda_stream

    bwd_bwd_func(
        grad_tensor_in,
        grad_tensor_w,
        grad_grad_tensor_out,
        maybe_detach(grad_grad_tensor_in),
        maybe_detach(grad_grad_tensor_w),
        maybe_detach(grad_tensor_out),
        maybe_detach(tensor_in),
        maybe_detach(tensor_w),
        maybe_detach(tensor_w_id),
        maybe_detach(tensor_w_offsets),
        batch_linear_info_grad_in_grad_w,
        batch_linear_info_grad_in_grad_grad_out,
        batch_linear_info_grad_w_grad_in,
        batch_linear_info_grad_w_grad_grad_out,
        op_mode,
        weight_shared_mode,
        num_w_segments,
        align_in,
        align_out,
        stream,
    )

    grad_tensor_w = (
        grad_tensor_w.to(tensor_w.dtype) if grad_tensor_w is not None else None
    )

    grads = [grad_grad_tensor_out]
    if needs_grad_in:
        grads.append(grad_tensor_in)
    if needs_grad_w:
        grads.append(grad_tensor_w)

    return grads


@torch.library.register_fake("cuequivariance_ops_torch::batch_linear_bwd_bwd_primitive")
def _(
    grad_tensor_in: Optional[torch.Tensor],
    grad_tensor_w: Optional[torch.Tensor],
    grad_tensor_out: torch.Tensor,
    tensor_in: torch.Tensor,
    tensor_w: torch.Tensor,
    tensor_w_id: Optional[torch.Tensor],
    tensor_w_offsets: torch.Tensor,
    layouts_fwd: torch.Tensor,
    index_offsets_fwd: torch.Tensor,
    indices_fwd: torch.Tensor,
    alpha_fwd: torch.Tensor,
    layouts_grad_in: torch.Tensor,
    index_offsets_grad_in: torch.Tensor,
    indices_grad_in: torch.Tensor,
    alpha_grad_in: torch.Tensor,
    layouts_grad_w: torch.Tensor,
    index_offsets_grad_w: torch.Tensor,
    indices_grad_w: torch.Tensor,
    alpha_grad_w: torch.Tensor,
    layouts_grad_in_grad_w: torch.Tensor,
    index_offsets_grad_in_grad_w: torch.Tensor,
    indices_grad_in_grad_w: torch.Tensor,
    alpha_grad_in_grad_w: torch.Tensor,
    layouts_grad_in_grad_grad_out: torch.Tensor,
    index_offsets_grad_in_grad_grad_out: torch.Tensor,
    indices_grad_in_grad_grad_out: torch.Tensor,
    alpha_grad_in_grad_grad_out: torch.Tensor,
    layouts_grad_w_grad_in: torch.Tensor,
    index_offsets_grad_w_grad_in: torch.Tensor,
    indices_grad_w_grad_in: torch.Tensor,
    alpha_grad_w_grad_in: torch.Tensor,
    layouts_grad_w_grad_grad_out: torch.Tensor,
    index_offsets_grad_w_grad_grad_out: torch.Tensor,
    indices_grad_w_grad_grad_out: torch.Tensor,
    alpha_grad_w_grad_grad_out: torch.Tensor,
    op_mode: int,
    weight_shared_mode: int,
    tensor_in_stride: int,
    tensor_w_stride: int,
    tensor_out_stride: int,
    num_w_segments: int,
    align_in: int,
    align_out: int,
    needs_grad_in: bool,
    needs_grad_w: bool,
) -> List[torch.Tensor]:
    math_dtype = int_float_mappings[alpha_fwd.dtype]
    grad_grad_tensor_out = torch.empty_like(grad_tensor_out)
    grad_tensor_in = maybe_empty_like(tensor_in, needs_grad_in)
    grad_tensor_w = maybe_empty_like(tensor_w, needs_grad_w, dtype=math_dtype)

    grads = [grad_grad_tensor_out]
    if needs_grad_in:
        grads.append(grad_tensor_in)
    if needs_grad_w:
        grads.append(grad_tensor_w)

    return grads


def batch_linear_setup_fwd_context(ctx, inputs, output):
    ctx.save_for_backward(*inputs[:-8])
    ctx.saved_constants = inputs[-8:]


def batch_linear_setup_bwd_context(ctx, inputs, output):
    ctx.save_for_backward(*inputs[:-10])
    ctx.saved_constants = inputs[-10:-2]


@torch.compiler.allow_in_graph
def batch_linear_fwd(*args):
    return torch.ops.cuequivariance_ops_torch.batch_linear_fwd_primitive(*args)


@torch.compiler.allow_in_graph
def batch_linear_bwd(ctx, grad_tensor_out):
    needs_grad_in = ctx.needs_input_grad[0]
    needs_grad_w = ctx.needs_input_grad[1]
    grads = torch.ops.cuequivariance_ops_torch.batch_linear_bwd_primitive(
        grad_tensor_out,
        *ctx.saved_tensors,
        *ctx.saved_constants,
        needs_grad_in,
        needs_grad_w,
    )

    not_empty = ctx.saved_tensors[0].shape[0] != 0

    grad_idx = 0
    grad_tensor_in, grad_tensor_w = None, None
    if needs_grad_in and not_empty:
        grad_tensor_in = grads[grad_idx]
        grad_idx += 1
    if needs_grad_w and not_empty:
        grad_tensor_w = grads[grad_idx]
        grad_idx += 1

    return (
        grad_tensor_in,
        grad_tensor_w,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )


@torch.compiler.allow_in_graph
def batch_linear_bwd_bwd(ctx, grad_grads):
    needs_grad_in = ctx.needs_input_grad[1]
    needs_grad_w = ctx.needs_input_grad[2]

    grad_idx = 0
    grad_grad_tensor_in, grad_grad_tensor_w = None, None
    if needs_grad_in:
        grad_grad_tensor_in = grad_grads[grad_idx]
        grad_idx += 1
    if needs_grad_w:
        grad_grad_tensor_w = grad_grads[grad_idx]
        grad_idx += 1

    grads = torch.ops.cuequivariance_ops_torch.batch_linear_bwd_bwd_primitive(
        grad_grad_tensor_in,
        grad_grad_tensor_w,
        *ctx.saved_tensors,
        *ctx.saved_constants,
        needs_grad_in,
        needs_grad_w,
    )

    not_empty = ctx.saved_tensors[1].shape[0] != 0

    grad_grad_tensor_out = grads[0] if not_empty else None

    grad_idx = 1
    grad_tensor_in, grad_tensor_w = None, None
    if needs_grad_in and not_empty:
        grad_tensor_in = grads[grad_idx]
        grad_idx += 1
    if needs_grad_w and not_empty:
        grad_tensor_w = grads[grad_idx]
        grad_idx += 1

    return (
        grad_grad_tensor_out,
        grad_tensor_in,
        grad_tensor_w,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )


torch.library.register_autograd(
    "cuequivariance_ops_torch::batch_linear_fwd_primitive",
    batch_linear_bwd,
    setup_context=batch_linear_setup_fwd_context,
)

torch.library.register_autograd(
    "cuequivariance_ops_torch::batch_linear_bwd_primitive",
    batch_linear_bwd_bwd,
    setup_context=batch_linear_setup_bwd_context,
)


def batch_linear(
    tensor_in: torch.Tensor,
    tensor_w: torch.Tensor,
    tensor_w_id: Optional[torch.Tensor],
    tensor_w_offsets: torch.Tensor,
    layouts_fwd: torch.Tensor,
    index_offsets_fwd: torch.Tensor,
    indices_fwd: torch.Tensor,
    alpha_fwd: torch.Tensor,
    layouts_grad_in: torch.Tensor,
    index_offsets_grad_in: torch.Tensor,
    indices_grad_in: torch.Tensor,
    alpha_grad_in: torch.Tensor,
    layouts_grad_w: torch.Tensor,
    index_offsets_grad_w: torch.Tensor,
    indices_grad_w: torch.Tensor,
    alpha_grad_w: torch.Tensor,
    layouts_grad_in_grad_w: torch.Tensor,
    index_offsets_grad_in_grad_w: torch.Tensor,
    indices_grad_in_grad_w: torch.Tensor,
    alpha_grad_in_grad_w: torch.Tensor,
    layouts_grad_in_grad_grad_out: torch.Tensor,
    index_offsets_grad_in_grad_grad_out: torch.Tensor,
    indices_grad_in_grad_grad_out: torch.Tensor,
    alpha_grad_in_grad_grad_out: torch.Tensor,
    layouts_grad_w_grad_in: torch.Tensor,
    index_offsets_grad_w_grad_in: torch.Tensor,
    indices_grad_w_grad_in: torch.Tensor,
    alpha_grad_w_grad_in: torch.Tensor,
    layouts_grad_w_grad_grad_out: torch.Tensor,
    index_offsets_grad_w_grad_grad_out: torch.Tensor,
    indices_grad_w_grad_grad_out: torch.Tensor,
    alpha_grad_w_grad_grad_out: torch.Tensor,
    op_mode: int,
    weight_shared_mode: int,
    tensor_in_stride: int,
    tensor_w_stride: int,
    tensor_out_stride: int,
    num_w_segments: int,
    align_in: int,
    align_out: int,
) -> torch.Tensor:
    return torch.ops.cuequivariance_ops_torch.batch_linear_fwd_primitive(
        tensor_in,
        tensor_w,
        tensor_w_id,
        tensor_w_offsets,
        layouts_fwd,
        index_offsets_fwd,
        indices_fwd,
        alpha_fwd,
        layouts_grad_in,
        index_offsets_grad_in,
        indices_grad_in,
        alpha_grad_in,
        layouts_grad_w,
        index_offsets_grad_w,
        indices_grad_w,
        alpha_grad_w,
        layouts_grad_in_grad_w,
        index_offsets_grad_in_grad_w,
        indices_grad_in_grad_w,
        alpha_grad_in_grad_w,
        layouts_grad_in_grad_grad_out,
        index_offsets_grad_in_grad_grad_out,
        indices_grad_in_grad_grad_out,
        alpha_grad_in_grad_grad_out,
        layouts_grad_w_grad_in,
        index_offsets_grad_w_grad_in,
        indices_grad_w_grad_in,
        alpha_grad_w_grad_in,
        layouts_grad_w_grad_grad_out,
        index_offsets_grad_w_grad_grad_out,
        indices_grad_w_grad_grad_out,
        alpha_grad_w_grad_grad_out,
        op_mode,
        weight_shared_mode,
        tensor_in_stride,
        tensor_w_stride,
        tensor_out_stride,
        num_w_segments,
        align_in,
        align_out,
    )


class BatchLinear(nn.Module):
    def __init__(
        self,
        operand_segment_modes: list[str],
        operand_segment_offsets: list[list[int]],
        operand_segment_shapes: list[list[list[int]]],
        path_indices: list[list[int]],
        path_coefficients: list[float],
        math_dtype,
    ):
        """
        Construct all the necessary attributes

        Parameters
        ---------------------------
        operand_segment_modes:
            symbols indicates feature layouts,
            ex. 'u' is a vector and 'uv' is a matrix
        operand_segment_offsets:
            list of memory offsets of segments for the three operands
        operand_segment_shapes:
            list of shapes of the three operands.
            dimensions of shapes must match operand_segment_modes.
            ex. 'u' has a 1-D shape and 'uv' has a 2-D shape.
        path_indices:
            list of integer tuples (paths) indicating which segments in operands to
            participate the operation indicated by operand_segment_modes.
        path_coefficients:
            list of scaling factors for each path
        math_dtype:
            data type for computation
        Example
        ---------------------------
        # valid operand_segment_modes are ['u', 'uv', 'v'] and ['uv', 'v', 'u']
        operand_segment_modes = ['u', 'uv', 'v']
        operand_segment_offsets = [[0, 8, 16], [0, 64, 128], [0, 8, 16]]
        operand_segment_shapes = [[[8], [8], [8]], [[8, 8], [8, 8], [8, 8]], [[8], [8], [8]]]

        # path_indices[i][-1] < len(operand_segment_offsets[-1])
        # path_indices[i][-2] < len(operand_segment_offsets[-2])
        # path_indices[i][0]  < len(operand_segment_offsets[0])
        path_indices = [[0, 0, 0], [1, 0, 1], [1, 1, 2]]
        path_coefficients = [0.1, 0.2, -0.1]

        batch_size = 100
        num_embeddings = 4
        math_dtype = torch.float32
        dtype = torch.float32

        batch_linear = BatchLinear(operand_segment_modes, operand_segment_offsets, \
        operand_segment_shapes, path_indices, path_coefficients, math_dtype)

        batch_linear.to('cuda')

        # strides along batch dimension
        tensor_in_stride  = operand_segment_offsets[0][-1] + \
                            math.prod(operand_segment_shapes[0][-1])
        tensor_w_stride   = operand_segment_offsets[1][-1] + \
                            math.prod(operand_segment_shapes[1][-1])
        tensor_out_stride = operand_segment_offsets[2][-1] + \
                            math.prod(operand_segment_shapes[2][-1])

        tensor_in = torch.randn(
        (batch_size, tensor_in_stride),
        dtype=dtype,
        requires_grad=True,
        device='cuda',
        )
        tensor_w = torch.randn(
        (num_embeddings, tensor_w_stride),
        dtype=dtype,
        requires_grad=True,
        device='cuda',
        )
        y = (
        torch.nn.functional.one_hot(
            torch.arange(0, batch_size) % num_embeddings, num_classes=num_embeddings
        )
        )
        tensor_w_id = (
        torch.nonzero(y)[:, 1]
        .contiguous()
        .to(dtype=torch.int32, device='cuda')
        .requires_grad_(False)
        )

        tensor_out = batch_linear.forward(tensor_in, tensor_w, tensor_w_id)
         """
        super().__init__()

        if not torch.cuda.is_available():
            raise AssertionError("No Nvidia GPU is detected")

        if (
            len(operand_segment_modes) != 3
            or len(operand_segment_offsets) != 3
            or len(operand_segment_shapes) != 3
        ):
            raise AssertionError("Only three-operand operation supported.")

        if len(path_indices) != len(path_coefficients):
            raise AssertionError(
                "Number of the path coefficients and of the path segment indices \
                have are different."
            )

        mode = "_".join(operand_segment_modes)
        if mode not in linear_mode_mappings:
            raise AssertionError("Not supported operation.")

        # map to integer
        self.op_mode = linear_mode_mappings[mode]

        w_op_id = operand_segment_modes.index("uv")
        in_op_id = 0 if w_op_id == 1 else 1
        out_op_id = 2

        self.align_in, self.align_out = _compute_alignments(
            operand_segment_modes, operand_segment_shapes
        )

        w_offsets = operand_segment_offsets[w_op_id]
        w_shapes = operand_segment_shapes[w_op_id]

        self.num_w_segments = len(w_offsets)

        def get_shape(op_shapes):
            return [len(op_shapes)] + np.array(op_shapes[0]).flatten().tolist()

        self.tensor_in_stride = _compute_stride(operand_segment_shapes[in_op_id])
        self.tensor_w_stride = _compute_stride(operand_segment_shapes[w_op_id])
        self.tensor_out_stride = _compute_stride(operand_segment_shapes[out_op_id])
        self.tensor_out_shape = get_shape(operand_segment_shapes[out_op_id])

        path_indices = [
            [operand_segment_offsets[i][idx] for i, idx in enumerate(index)]
            for index in path_indices
        ]
        self.fwd_info = BatchLinearInfo(
            operand_segment_modes,
            path_indices,
            path_coefficients,
            w_offsets,
            w_shapes,
            math_dtype,
        )

        op_modes_grad_in, path_indices_grad_in = _diff_operand_list(
            in_op_id, operand_segment_modes, path_indices
        )

        op_modes_grad_w, path_indices_grad_w = _diff_operand_list(
            w_op_id, operand_segment_modes, path_indices
        )

        self.grad_in_bwd_info = BatchLinearInfo(
            op_modes_grad_in,
            path_indices_grad_in,
            path_coefficients,
            w_offsets,
            w_shapes,
            math_dtype,
        )
        self.grad_w_bwd_info = BatchLinearInfo(
            op_modes_grad_w,
            path_indices_grad_w,
            path_coefficients,
            w_offsets,
            w_shapes,
            math_dtype,
        )

        w_op_id = op_modes_grad_in.index("uv")
        out_op_id = 1 if w_op_id == 0 else 0

        op_modes_grad_in_grad_w, path_indices_grad_in_grad_w = _diff_operand_list(
            w_op_id, op_modes_grad_in, path_indices_grad_in
        )
        (
            op_modes_grad_in_grad_grad_out,
            path_indices_grad_in_grad_grad_out,
        ) = _diff_operand_list(out_op_id, op_modes_grad_in, path_indices_grad_in)
        out_op_id = 0 if in_op_id == 1 else 1
        op_modes_grad_w_grad_in, path_indices_grad_w_grad_in = _diff_operand_list(
            in_op_id, op_modes_grad_w, path_indices_grad_w
        )
        (
            op_modes_grad_w_grad_grad_out,
            path_indices_grad_w_grad_grad_out,
        ) = _diff_operand_list(out_op_id, op_modes_grad_w, path_indices_grad_w)
        self.grad_in_grad_w_bwd_bwd_info = BatchLinearInfo(
            op_modes_grad_in_grad_w,
            path_indices_grad_in_grad_w,
            path_coefficients,
            w_offsets,
            w_shapes,
            math_dtype,
        )
        self.grad_in_grad_grad_out_bwd_bwd_info = BatchLinearInfo(
            op_modes_grad_in_grad_grad_out,
            path_indices_grad_in_grad_grad_out,
            path_coefficients,
            w_offsets,
            w_shapes,
            math_dtype,
        )
        self.grad_w_grad_in_bwd_bwd_info = BatchLinearInfo(
            op_modes_grad_w_grad_in,
            path_indices_grad_w_grad_in,
            path_coefficients,
            w_offsets,
            w_shapes,
            math_dtype,
        )
        self.grad_w_grad_grad_out_bwd_bwd_info = BatchLinearInfo(
            op_modes_grad_w_grad_grad_out,
            path_indices_grad_w_grad_grad_out,
            path_coefficients,
            w_offsets,
            w_shapes,
            math_dtype,
        )

        self.register_buffer(
            "tensor_w_offsets", torch.Tensor(w_offsets).to(torch.int32).contiguous()
        )

    def forward(
        self,
        tensor_in: torch.Tensor,
        tensor_w: torch.Tensor,
        tensor_w_id: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        weight_shared_mode = 1
        if tensor_w_id is None:
            if tensor_w.shape[0] == 1:
                weight_shared_mode = 0
            elif tensor_w.shape[0] == tensor_in.shape[0]:
                weight_shared_mode = 2
            else:
                raise AssertionError("Not valid weight shared mode.")

        return batch_linear(
            tensor_in,
            tensor_w,
            tensor_w_id,
            self.tensor_w_offsets,
            self.fwd_info.layouts,
            self.fwd_info.index_offsets,
            self.fwd_info.indices,
            self.fwd_info.alpha,
            self.grad_in_bwd_info.layouts,
            self.grad_in_bwd_info.index_offsets,
            self.grad_in_bwd_info.indices,
            self.grad_in_bwd_info.alpha,
            self.grad_w_bwd_info.layouts,
            self.grad_w_bwd_info.index_offsets,
            self.grad_w_bwd_info.indices,
            self.grad_w_bwd_info.alpha,
            self.grad_in_grad_w_bwd_bwd_info.layouts,
            self.grad_in_grad_w_bwd_bwd_info.index_offsets,
            self.grad_in_grad_w_bwd_bwd_info.indices,
            self.grad_in_grad_w_bwd_bwd_info.alpha,
            self.grad_in_grad_grad_out_bwd_bwd_info.layouts,
            self.grad_in_grad_grad_out_bwd_bwd_info.index_offsets,
            self.grad_in_grad_grad_out_bwd_bwd_info.indices,
            self.grad_in_grad_grad_out_bwd_bwd_info.alpha,
            self.grad_w_grad_in_bwd_bwd_info.layouts,
            self.grad_w_grad_in_bwd_bwd_info.index_offsets,
            self.grad_w_grad_in_bwd_bwd_info.indices,
            self.grad_w_grad_in_bwd_bwd_info.alpha,
            self.grad_w_grad_grad_out_bwd_bwd_info.layouts,
            self.grad_w_grad_grad_out_bwd_bwd_info.index_offsets,
            self.grad_w_grad_grad_out_bwd_bwd_info.indices,
            self.grad_w_grad_grad_out_bwd_bwd_info.alpha,
            self.op_mode,
            weight_shared_mode,
            self.tensor_in_stride,
            self.tensor_w_stride,
            self.tensor_out_stride,
            self.num_w_segments,
            self.align_in,
            self.align_out,
        )


__all__ = ["BatchLinear"]
