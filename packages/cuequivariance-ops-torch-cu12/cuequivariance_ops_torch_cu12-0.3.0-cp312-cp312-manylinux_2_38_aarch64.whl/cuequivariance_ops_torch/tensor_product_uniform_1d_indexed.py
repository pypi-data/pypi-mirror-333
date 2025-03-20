# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


import logging
from typing import Optional

import torch

import cuequivariance_ops_torch._ext as ext

from .tensor_product_uniform_1d import TensorProductUniform1d, _is_empty

logger = logging.getLogger(__name__)


def _indexed_fwd_fake(
    ins: list[torch.Tensor],
    number_of_output_rows: int,
    number_of_output_segments: int,
    set_zero: bool,
) -> torch.Tensor:
    if set_zero:
        return torch.zeros(
            number_of_output_rows,
            number_of_output_segments,
            max(i.shape[2] for i in ins if i is not None and not _is_empty(i)),
            dtype=ins[0].dtype,
            device=ins[0].device,
            requires_grad=True,
        )

    return torch.empty(
        number_of_output_rows,
        number_of_output_segments,
        max(i.shape[2] for i in ins if i is not None and not _is_empty(i)),
        dtype=ins[0].dtype,
        device=ins[0].device,
        requires_grad=True,
    )


def _indexed_fwd_impl(
    ins: list[torch.Tensor],
    number_of_output_rows: int,
    number_of_output_segments: int,
    number_of_paths: int,
    data: torch.Tensor,
    op_indices: list[torch.Tensor],
    math_code: int,
) -> torch.Tensor:
    op_indices = [o if o is not None and not _is_empty(o) else None for o in op_indices]
    out = _indexed_fwd_fake(
        ins,
        number_of_output_rows,
        number_of_output_segments,
        op_indices[-1] is not None,
    )

    if ins[2] is None or _is_empty(ins[2]):
        ext.tensor_product_uniform_1d_indexed_fwd(
            number_of_paths,
            data.detach().contiguous(),
            math_code,
            [ins[i].detach().contiguous() for i in [0, 1]],
            out,
            [op_indices[i] for i in [0, 1, 3]],
            torch.cuda.current_stream().cuda_stream,
        )
    else:
        ext.tensor_product_uniform_1d_indexed_fwd(
            number_of_paths,
            data.detach().contiguous(),
            math_code,
            [ins[i].detach().contiguous() for i in [0, 1, 2]],
            out,
            [op_indices[i] for i in [0, 1, 2, 3]],
            torch.cuda.current_stream().cuda_stream,
        )

    return out


def _indexed_bwd_fake(
    ins: list[torch.Tensor], ngs: list[bool], op_indices: list[torch.Tensor]
) -> list[torch.Tensor]:
    return tuple(
        [
            (torch.empty_like(inp) if (ng and not _is_empty(inp)) else None)
            if (op_indices[i] is None and inp.size(0) > 1)
            else (torch.zeros_like(inp) if (ng and not _is_empty(inp)) else None)
            for i, (inp, ng) in enumerate(zip(ins, ngs))
        ]
    )


def _indexed_bwd_impl(
    ins: list[torch.Tensor],
    ngs: list[bool],
    number_of_paths: int,
    data: torch.Tensor,
    op_indices: list[torch.Tensor],
    math_code: int,
) -> list[torch.Tensor]:
    op_indices = [o if not _is_empty(o) else None for o in op_indices]
    outs = _indexed_bwd_fake(ins, ngs, op_indices)

    if _is_empty(ins[2]):
        ext.tensor_product_uniform_1d_indexed_bwd(
            number_of_paths,
            data.detach().contiguous(),
            math_code,
            [ins[i].detach().contiguous() for i in [0, 1, 3]],
            [outs[i] for i in [0, 1]],
            [op_indices[i] for i in [0, 1, 3]],
            torch.cuda.current_stream().cuda_stream,
        )
    else:
        ext.tensor_product_uniform_1d_indexed_bwd(
            number_of_paths,
            data.detach().contiguous(),
            math_code,
            [ins[i].detach().contiguous() for i in [0, 1, 2, 3]],
            [outs[i] for i in [0, 1, 2]],
            [op_indices[i] for i in [0, 1, 2, 3]],
            torch.cuda.current_stream().cuda_stream,
        )

    return outs


def _indexed_bwd_bwd_impl(
    ins: list[torch.Tensor],
    dins: list[torch.Tensor],
    ngs: list[torch.Tensor],
    number_of_paths: int,
    data: torch.Tensor,
    op_indices: list[torch.Tensor],
    math_code: int,
):
    op_indices = [o if not _is_empty(o) else None for o in op_indices]
    outs = _indexed_bwd_fake(ins, ngs, op_indices)

    if _is_empty(ins[2]):
        ext.tensor_product_uniform_1d_indexed_bwd_bwd(
            number_of_paths,
            data.detach().contiguous(),
            math_code,
            [ins[i].detach().contiguous() for i in [0, 1, 3]],
            [dins[i].detach().contiguous() for i in [0, 1]],
            [outs[i] for i in [0, 1, 3]],
            [op_indices[i] for i in [0, 1, 3]],
            torch.cuda.current_stream().cuda_stream,
        )
    else:
        ext.tensor_product_uniform_1d_indexed_bwd_bwd(
            number_of_paths,
            data.detach().contiguous(),
            math_code,
            [ins[i].detach().contiguous() for i in [0, 1, 2, 3]],
            [dins[i].detach().contiguous() for i in [0, 1, 2]],
            [outs[i] for i in [0, 1, 2, 3]],
            [op_indices[i] for i in [0, 1, 2, 3]],
            torch.cuda.current_stream().cuda_stream,
        )

    return outs


def _indexed_fwd_primitive_setup_context(ctx, inputs, output):
    *ins, _, _, num_paths, data, op_idx0, op_idx1, op_idx2, op_idxo, math_code = inputs
    ctx.num_paths = num_paths
    ctx.math_code = math_code
    ctx.save_for_backward(*ins, data, op_idx0, op_idx1, op_idx2, op_idxo)


def _indexed_fwd_primitive_backward(ctx, in3):
    *ins, data, op_idx0, op_idx1, op_idx2, op_idxo = ctx.saved_tensors
    ngs = ctx.needs_input_grad[: len(ins)]
    args = []
    for i, n in zip(ins, ngs):
        args.append(i)
        args.append(n)
    outs = torch.ops.cuequivariance_ops_torch.tensor_product_uniform_4x1d_indexed_bwd_primitive(
        *args,
        in3,
        ctx.num_paths,
        data,
        op_idx0,
        op_idx1,
        op_idx2,
        op_idxo,
        ctx.math_code,
    )
    result = list(outs) + [None, None, None, None, None, None, None, None, None]
    return tuple(result)


def _indexed_bwd_primitive_setup_context(ctx, inputs, output):
    *ins, num_paths, data, op_idx0, op_idx1, op_idx2, op_idxo, math_code = inputs
    ctx.num_paths = num_paths
    ctx.math_code = math_code
    ctx.save_for_backward(*ins[::2], data, op_idx0, op_idx1, op_idx2, op_idxo)


def _indexed_bwd_primitive_backward(ctx, *grads):
    *ins, data, op_idx0, op_idx1, op_idx2, op_idxo = ctx.saved_tensors
    ngs = ctx.needs_input_grad[::2][: len(ins)]
    assert len(ins) == len(grads) + 1
    assert len(ngs) == len(grads) + 1
    args = []
    for i, g, n in zip(ins, grads, ngs):
        args.append(i)
        args.append(g)
        args.append(n)
    args.append(ins[-1])
    args.append(True)  # grad-output always requires grad
    outs = torch.ops.cuequivariance_ops_torch.tensor_product_uniform_4x1d_indexed_bwd_bwd_primitive(
        *args,
        ctx.num_paths,
        data,
        op_idx0,
        op_idx1,
        op_idx2,
        op_idxo,
        ctx.math_code,
    )
    result = []
    for o in outs:
        result.append(o)
        result.append(None)
    # gradients for op-indices, math_code, and data
    for _ in range(6):
        result.append(None)
    return tuple(result)


torch.library.define(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_fwd_primitive",
    (
        "(Tensor in0, Tensor in1, Tensor in2, int nrows, int noos, int nop,"
        "Tensor data, Tensor op_idx0, Tensor op_idx1, Tensor op_idx2, Tensor op_idxo,"
        "int math_code)"
        " -> Tensor"
    ),
)

torch.library.define(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_bwd_primitive",
    (
        "(Tensor in0, bool ng0, Tensor in1, bool ng1,"
        "Tensor in2, bool ng2, Tensor in3, int nop,"
        "Tensor data, Tensor op_idx0, Tensor op_idx1, Tensor op_idx2, Tensor op_idxo,"
        "int math_code)"
        " -> "
        "(Tensor? out0, Tensor? out1, Tensor? out2)"
    ),
)

torch.library.define(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_bwd_bwd_primitive",
    (
        "(Tensor in0, Tensor din0, bool ng0, Tensor in1, Tensor din1, bool ng1,"
        "Tensor in2, Tensor din2, bool ng2, Tensor in3, bool ng3,"
        "int nop, Tensor data, Tensor op_idx0, Tensor op_idx1, Tensor op_idx2, Tensor op_idxo,"
        "int math_code)"
        " -> "
        "(Tensor? out0, Tensor? out1, Tensor? out2, Tensor? out3)"
    ),
)


@torch.library.impl(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_fwd_primitive",
    "cuda",
)
def _(
    in0: torch.Tensor,
    in1: torch.Tensor,
    in2: torch.Tensor,
    number_of_output_rows: int,
    number_of_output_segments: int,
    number_of_paths: int,
    data: torch.Tensor,
    op_idx0: torch.Tensor,
    op_idx1: torch.Tensor,
    op_idx2: torch.Tensor,
    op_idxo: torch.Tensor,
    math_code: int,
) -> torch.Tensor:
    return _indexed_fwd_impl(
        [in0, in1, in2],
        number_of_output_rows,
        number_of_output_segments,
        number_of_paths,
        data,
        [op_idx0, op_idx1, op_idx2, op_idxo],
        math_code,
    )


@torch.library.impl(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_bwd_primitive",
    "cuda",
)
def _(
    in0: torch.Tensor,
    ng0: bool,
    in1: torch.Tensor,
    ng1: bool,
    in2: torch.Tensor,
    ng2: bool,
    in3: torch.Tensor,
    number_of_paths: int,
    data: torch.Tensor,
    op_idx0: torch.Tensor,
    op_idx1: torch.Tensor,
    op_idx2: torch.Tensor,
    op_idxo: torch.Tensor,
    math_code: int,
) -> (torch.Tensor, torch.Tensor, torch.Tensor):
    return _indexed_bwd_impl(
        [in0, in1, in2, in3],
        [ng0, ng1, ng2],
        number_of_paths,
        data,
        [op_idx0, op_idx1, op_idx2, op_idxo],
        math_code,
    )


@torch.library.impl(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_bwd_bwd_primitive",
    "cuda",
)
def _(
    in0: torch.Tensor,
    din0: torch.Tensor,
    ng0: bool,
    in1: torch.Tensor,
    din1: torch.Tensor,
    ng1: bool,
    in2: torch.Tensor,
    din2: torch.Tensor,
    ng2: bool,
    in3: torch.Tensor,
    ng3: bool,
    number_of_paths: int,
    data: torch.Tensor,
    op_idx0: torch.Tensor,
    op_idx1: torch.Tensor,
    op_idx2: torch.Tensor,
    op_idxo: torch.Tensor,
    math_code: int,
) -> (torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor):
    return _indexed_bwd_bwd_impl(
        [in0, in1, in2, in3],
        [din0, din1, din2],
        [ng0, ng1, ng2, ng3],
        number_of_paths,
        data,
        [op_idx0, op_idx1, op_idx2, op_idxo],
        math_code,
    )


@torch.library.register_fake(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_fwd_primitive"
)
def _(
    in0: torch.Tensor,
    in1: torch.Tensor,
    in2: torch.Tensor,
    number_of_output_rows: int,
    number_of_output_segments: int,
    number_of_paths: int,
    data: torch.Tensor,
    op_idx0: torch.Tensor,
    op_idx1: torch.Tensor,
    op_idx2: torch.Tensor,
    op_idxo: torch.Tensor,
    math_code: int,
) -> torch.Tensor:
    return _indexed_fwd_fake(
        [in0, in1, in2],
        number_of_output_rows,
        number_of_output_segments,
        op_idxo is not None,
    )


@torch.library.register_fake(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_bwd_primitive"
)
def _(
    in0: torch.Tensor,
    ng0: bool,
    in1: torch.Tensor,
    ng1: bool,
    in2: torch.Tensor,
    ng2: bool,
    in3: torch.Tensor,
    number_of_paths: int,
    data: torch.Tensor,
    op_idx0: torch.Tensor,
    op_idx1: torch.Tensor,
    op_idx2: torch.Tensor,
    op_idxo: torch.Tensor,
    math_code: int,
) -> (torch.Tensor, torch.Tensor, torch.Tensor):
    return _indexed_bwd_fake(
        [in0, in1, in2, in3], [ng0, ng1, ng2], [None, None, None, None]
    )


@torch.library.register_fake(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_bwd_bwd_primitive"
)
def _(
    in0: torch.Tensor,
    din0: torch.Tensor,
    ng0: bool,
    in1: torch.Tensor,
    din1: torch.Tensor,
    ng1: bool,
    in2: torch.Tensor,
    din2: torch.Tensor,
    ng2: bool,
    in3: torch.Tensor,
    ng3: bool,
    number_of_paths: int,
    data: torch.Tensor,
    op_idx0: torch.Tensor,
    op_idx1: torch.Tensor,
    op_idx2: torch.Tensor,
    op_idxo: torch.Tensor,
    math_code: int,
) -> (torch.Tensor, torch.Tensor, torch.Tensor):
    return _indexed_bwd_fake(
        [in0, in1, in2, in3], [ng0, ng1, ng2, ng3], [None, None, None, None]
    )


torch.library.register_autograd(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_fwd_primitive",
    _indexed_fwd_primitive_backward,
    setup_context=_indexed_fwd_primitive_setup_context,
)

torch.library.register_autograd(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_indexed_bwd_primitive",
    _indexed_bwd_primitive_backward,
    setup_context=_indexed_bwd_primitive_setup_context,
)


class TensorProductUniform4x1dIndexed(TensorProductUniform1d):
    def forward(
        self,
        in0: torch.Tensor,
        in1: torch.Tensor,
        in2: torch.Tensor,
        idx_in0: Optional[torch.Tensor],
        idx_in1: Optional[torch.Tensor],
        idx_in2: Optional[torch.Tensor],
        idx_out: Optional[torch.Tensor],
        num_rows_out: int,
    ) -> torch.Tensor:
        """
        Execute the TensorProductUniform1d kernel.

        Each operand is a torch tensor with two dimensions. Eeach
        operand also can be optionally indexed with an index tensor into
        its first dimension. Index tensors must have the same shape or
        be passed as None. The shape of the index tensor corresponds to
        the batch dimension of the un-indexed case. Indices into inputs
        indicate which input rows are contracted and the index into the
        output indicates into which output row the result is written.
        Generally, a sufficiently large batch dimension is required for good
        performance.
        The last tensor dimension contains all the segments of the
        operand packed together, so it is of size
        ``operand_num_segments[i] * operand_extent`` for vector operands (i.e.,
        where ``operand_dim[i] == 1``) or just ``operand_num_segments[i]`` for
        scalar operands.

        Parameters
        ----------
        in0: torch.Tensor
            The first operand of the tensor product.
        in1: torch.Tensor
            The second operand of the tensor product.
        in2: torch.Tensor
            The third operand of the tensor product. Required for 4-dimensional
            tensor products, ignored for 3-dimensional tensor products.
        idx_in0: torch.Tensor, optional
            An index into the batch dimension of the first input, ignored if None.
        idx_in1: torch.Tensor, optional
            An index into the batch dimension of the second input, ignored if None.
        idx_in2: torch.Tensor, optional
            An index into the batch dimension of the third input, ignored if None.
        idx_out: torch.Tensor, optional
            An index into the batch dimension of the output, ignored if None.
        num_rows_out: int
            The number of output rows, should correspond to max(idx_out) + 1.

        Returns
        -------
        torch.Tensor
            The last (output) operand of the tensor product.
        """
        if in2 is None:
            in2 = torch.empty((0,), dtype=in0.dtype, device=in0.device)

        if idx_in0 is None:
            idx_in0 = torch.empty((0,), dtype=torch.int64, device=in0.device)
        if idx_in1 is None:
            idx_in1 = torch.empty((0,), dtype=torch.int64, device=in0.device)
        if idx_in2 is None:
            idx_in2 = torch.empty((0,), dtype=torch.int64, device=in0.device)
        if idx_out is None:
            idx_out = torch.empty((0,), dtype=torch.int64, device=in0.device)

        ins = [
            in0,
            in1,
            in2,
        ]

        for i in range(len(self.operand_dim) - 1):
            ins[i] = ins[i].reshape(
                ins[i].shape[0], self.operand_num_segments[i], self.segment_len[i]
            )

        for i in ins:
            torch._assert(ins[0].dtype == i.dtype, "tensors must have same type")
        out = torch.ops.cuequivariance_ops_torch.tensor_product_uniform_4x1d_indexed_fwd_primitive(
            ins[0],
            ins[1],
            ins[2],
            num_rows_out,
            self.number_of_output_segments,
            self.number_of_paths,
            self.data,
            idx_in0,
            idx_in1,
            idx_in2,
            idx_out,
            self.math_code,
        )
        if not torch.jit.is_scripting() and not torch.compiler.is_compiling():
            logger.debug(
                "TensorProductUniform4x1dIndexed.forward("
                + f"in0.shape={in0.shape}, in0.dtype={in0.dtype}, "
                + f"in1.shape={in1.shape}, in1.dtype={in1.dtype}, "
                + f"in2.shape={in2.shape}, "
                + f"in2.dtype={in2.dtype}, "
                + f"out.shape={out.shape}, out.dtype={out.dtype})"
            )
        return out.reshape(out.shape[0], self.out_last_dim)


class TensorProductUniform3x1dIndexed(TensorProductUniform4x1dIndexed):
    def forward(
        self,
        in0: torch.Tensor,
        in1: torch.Tensor,
        idx_in0: Optional[torch.Tensor],
        idx_in1: Optional[torch.Tensor],
        idx_out: Optional[torch.Tensor],
        num_rows_out: int,
    ) -> torch.Tensor:
        """
        Execute the TensorProductUniform1d kernel.

        Each operand is a torch tensor with two dimensions. Eeach
        operand also can be optionally indexed with an index tensor into
        its first dimension. Index tensors must have the same shape or
        be passed as None. The shape of the index tensor corresponds to
        the batch dimension of the un-indexed case. Indices into inputs
        indicate which input rows are contracted and the index into the
        output indicates into which output row the result is written.
        Generally, a sufficiently large batch dimension is required for good
        performance.
        The last tensor dimension contains all the segments of the
        operand packed together, so it is of size
        ``operand_num_segments[i] * operand_extent`` for vector operands (i.e.,
        where ``operand_dim[i] == 1``) or just ``operand_num_segments[i]`` for
        scalar operands.

        Parameters
        ----------
        in0: torch.Tensor
            The first operand of the tensor product.
        in1: torch.Tensor
            The second operand of the tensor product.
        idx_in0: torch.Tensor, optional
            An index into the batch dimension of the first input, ignored if None.
        idx_in1: torch.Tensor, optional
            An index into the batch dimension of the second input, ignored if None.
        idx_out: torch.Tensor, optional
            An index into the batch dimension of the output, ignored if None.
        num_rows_out: int
            The number of output rows, should correspond to max(idx_out) + 1.

        Returns
        -------
        torch.Tensor
            The last (output) operand of the tensor product.
        """

        if idx_in0 is None:
            idx_in0 = torch.empty((0,), dtype=torch.int64, device=in0.device)
        if idx_in1 is None:
            idx_in1 = torch.empty((0,), dtype=torch.int64, device=in0.device)
        idx_in2 = torch.empty((0,), dtype=torch.int64, device=in0.device)
        in2 = torch.empty((0,), dtype=in0.dtype, device=in0.device)
        if idx_out is None:
            idx_out = torch.empty((0,), dtype=torch.int64, device=in0.device)

        ins = [
            in0,
            in1,
            in2,
        ]

        for i in range(len(self.operand_dim) - 1):
            ins[i] = ins[i].reshape(
                ins[i].shape[0], self.operand_num_segments[i], self.segment_len[i]
            )

        for i in ins:
            torch._assert(ins[0].dtype == i.dtype, "tensors must have same type")
        out = torch.ops.cuequivariance_ops_torch.tensor_product_uniform_4x1d_indexed_fwd_primitive(
            ins[0],
            ins[1],
            ins[2],
            num_rows_out,
            self.number_of_output_segments,
            self.number_of_paths,
            self.data,
            idx_in0,
            idx_in1,
            idx_in2,
            idx_out,
            self.math_code,
        )
        if not torch.jit.is_scripting() and not torch.compiler.is_compiling():
            logger.debug(
                "TensorProductUniform4x1dIndexed.forward("
                + f"in0.shape={in0.shape}, in0.dtype={in0.dtype}, "
                + f"in1.shape={in1.shape}, in1.dtype={in1.dtype}, "
                + f"out.shape={out.shape}, out.dtype={out.dtype})"
            )
        return out.reshape(out.shape[0], self.out_last_dim)


__all__ = ["TensorProductUniform4x1dIndexed", "TensorProductUniform3x1dIndexed"]
