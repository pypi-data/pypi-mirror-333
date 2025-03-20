# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from typing import Optional

import torch
from torch.onnx import symbolic_helper


@symbolic_helper.parse_args("v", "v", "b")
def symbolic_segmented_transpose_primitive(g, tensor, segment_info, contiguous):
    out_shape = symbolic_helper._get_tensor_sizes(tensor)
    output_type = tensor.type().with_sizes(out_shape)
    out = g.op(
        "cuequivariance_ops::segmented_transpose",
        tensor,
        segment_info,
        contiguous_i=contiguous,
    )
    out.setType(output_type)
    return out


torch.onnx.register_custom_op_symbolic(
    "cuequivariance_ops_torch::segmented_transpose_primitive",
    symbolic_segmented_transpose_primitive,
    1,
)


def is_none_value(value):
    if value is None:
        return True
    return (
        isinstance(value, torch._C.Value)
        and value.node().kind() == "prim::Constant"
        and isinstance(value.type(), torch._C.NoneType)
    )


def symbolic_fused_tensor_product_fwd_primitive(
    g,
    in0: torch.Tensor,
    in1: torch.Tensor,
    in2: Optional[torch.Tensor],
    tp_path_csr_offsets_fwd: torch.Tensor,
    tp_path_csr_offsets_dgrad_in0: torch.Tensor,
    tp_path_csr_offsets_dgrad_in1: torch.Tensor,
    tp_path_csr_offsets_dgrad_in2: torch.Tensor,
    tp_path_offsets_fwd: torch.Tensor,
    tp_path_offsets_dgrad_in0: torch.Tensor,
    tp_path_offsets_dgrad_in1: torch.Tensor,
    tp_path_offsets_dgrad_in2: torch.Tensor,
    tp_path_cg_values_fwd: torch.Tensor,
    tp_path_cg_values_dgrad_in0: torch.Tensor,
    tp_path_cg_values_dgrad_in1: torch.Tensor,
    tp_path_cg_values_dgrad_in2: torch.Tensor,
    connection_mode: int,
    output_stride: int,
):
    # print(f"connection_mode={connection_mode}, in2.type()={in2.type()}")
    out_shape = symbolic_helper._get_tensor_sizes(in0)
    sz = symbolic_helper._parse_arg(output_stride, "i")
    mode = symbolic_helper._parse_arg(connection_mode, "i")
    output_type = in0.type().with_sizes(out_shape[:1] + [sz])

    output = g.op(
        "cuequivariance_ops::fused_tensor_product",
        in0,
        in1,
        in0 if is_none_value(in2) else in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
        connection_mode_i=mode,
        output_stride_i=sz,
    )
    output.setType(output_type)
    return output


torch.onnx.register_custom_op_symbolic(
    "cuequivariance_ops_torch::fused_tensor_product_fwd_primitive",
    symbolic_fused_tensor_product_fwd_primitive,
    1,
)


def symbolic_tensor_product_uniform_4x1d_fwd_primitive(
    g, in0, in1, in2, noos, nop, data, math_data
):
    in0_shape = symbolic_helper._get_tensor_sizes(in0)
    in1_shape = symbolic_helper._get_tensor_sizes(in1)
    in2_shape = symbolic_helper._get_tensor_sizes(in2)
    number_of_output_segments = symbolic_helper._parse_arg(noos, "i")
    number_of_paths = symbolic_helper._parse_arg(nop, "i")
    math_code = symbolic_helper._parse_arg(math_data, "i")

    out_shape = (
        max(in0_shape[0], in1_shape[0], in2_shape[0]),
        number_of_output_segments,
        max(
            in0_shape[2],
            in1_shape[2],
            in2_shape[2] if len(in2_shape) >= 3 else in1_shape[2],
        ),
    )

    output_type = in0.type().with_sizes(out_shape)

    output = g.op(
        "cuequivariance_ops::tensor_product_uniform_4x1d",
        in0,
        in1,
        in2,
        data,
        number_of_output_segments_i=number_of_output_segments,
        number_of_paths_i=number_of_paths,
        math_code_i=math_code,
    )
    output.setType(output_type)
    return output


torch.onnx.register_custom_op_symbolic(
    "cuequivariance_ops_torch::tensor_product_uniform_4x1d_fwd_primitive",
    symbolic_tensor_product_uniform_4x1d_fwd_primitive,
    1,
)


def symbolic_symmetric_tensor_contraction_fwd_primitive(
    g,
    in0,
    in1,
    in2,
    path_vals,
    path_indices,
    path_offsets,
    c0,
    c1,
    c2,
    c3,
    c4,
    c5,
    c6,
    c7,
    c8,
    c9,
    c10,
    c11,
    c12,
    c13,
    c14,
    c15,
    c16,
    c17,
    c18,
    c19,
    c20,
    num_in_segments,
    num_out_segments,
    num_coupling_paths,
    corr,
):
    in0_shape = symbolic_helper._get_tensor_sizes(in0)
    number_of_output_segments = symbolic_helper._parse_arg(num_out_segments, "i")
    correlation = symbolic_helper._parse_arg(corr, "i")

    out_shape = (in0_shape[0], number_of_output_segments, in0_shape[2])
    output_type = in0.type().with_sizes(out_shape)

    output = g.op(
        "cuequivariance_ops::symmetric_tensor_contraction",
        in0,
        in1,
        in2,
        path_vals,
        path_indices,
        path_offsets,
        number_of_output_segments_i=number_of_output_segments,
        correlation_i=correlation,
    )
    output.setType(output_type)
    return output


torch.onnx.register_custom_op_symbolic(
    "cuequivariance_ops_torch::symmetric_tensor_contraction_fwd_primitive",
    symbolic_symmetric_tensor_contraction_fwd_primitive,
    1,
)


def symbolic_batch_linear_fwd_primitive(
    g,
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
):
    op_mode_ = symbolic_helper._parse_arg(op_mode, "i")
    weight_shared_mode_ = symbolic_helper._parse_arg(weight_shared_mode, "i")
    tensor_in_stride_ = symbolic_helper._parse_arg(tensor_in_stride, "i")
    tensor_w_stride_ = symbolic_helper._parse_arg(tensor_w_stride, "i")
    tensor_out_stride_ = symbolic_helper._parse_arg(tensor_out_stride, "i")
    num_w_segments_ = symbolic_helper._parse_arg(num_w_segments, "i")
    align_in_ = symbolic_helper._parse_arg(align_in, "i")
    align_out_ = symbolic_helper._parse_arg(align_out, "i")

    in_shape = symbolic_helper._get_tensor_sizes(tensor_in)

    out_shape = (in_shape[0], tensor_out_stride_)
    output_type = tensor_in.type().with_sizes(out_shape)

    tensor_out = g.op(
        "cuequivariance_ops::batch_linear",
        tensor_in,
        tensor_w,
        tensor_w_offsets if is_none_value(tensor_w_id) else tensor_w_id,
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
        op_mode_i=op_mode_,
        weight_shared_mode_i=weight_shared_mode_,
        tensor_in_stride_i=tensor_in_stride_,
        tensor_w_stride_i=tensor_w_stride_,
        tensor_out_stride_i=tensor_out_stride_,
        num_w_segments_i=num_w_segments_,
        align_in_i=align_in_,
        align_out_i=align_out_,
    )
    tensor_out.setType(output_type)
    return tensor_out


torch.onnx.register_custom_op_symbolic(
    "cuequivariance_ops_torch::batch_linear_fwd_primitive",
    symbolic_batch_linear_fwd_primitive,
    1,
)

try:
    import onnxscript
    from onnxscript import opset18 as op

    _onnx_opset = onnxscript.values.Opset("cuequivariance_ops", version=1)

    @onnxscript.script(_onnx_opset, default_opset=op)
    def onnxscript_segmented_transpose_primitive(
        tensor,
        segment_info,
        input_contiguous_as_info: bool,
    ):
        return _onnx_opset.segmented_transpose(
            tensor,
            segment_info,
            contiguous=input_contiguous_as_info,
        )

    @onnxscript.script(_onnx_opset, default_opset=op)
    def onnxscript_fused_tensor_product_fwd_primitive(
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
        connection_mode: int,
        output_stride: int,
    ):
        return _onnx_opset.fused_tensor_product(
            in0,
            in1,
            in2,
            tp_path_csr_offsets_fwd,
            tp_path_csr_offsets_dgrad_in0,
            tp_path_csr_offsets_dgrad_in1,
            tp_path_csr_offsets_dgrad_in2,
            tp_path_offsets_fwd,
            tp_path_offsets_dgrad_in0,
            tp_path_offsets_dgrad_in1,
            tp_path_offsets_dgrad_in2,
            tp_path_cg_values_fwd,
            tp_path_cg_values_dgrad_in0,
            tp_path_cg_values_dgrad_in1,
            tp_path_cg_values_dgrad_in2,
            connection_mode=connection_mode,
            output_stride=output_stride,
        )

    @onnxscript.script(_onnx_opset, default_opset=op)
    def onnxscript_tensor_product_uniform_4x1d_fwd_primitive(
        in0,
        in1,
        in2,
        number_of_output_segments: int,
        number_of_paths: int,
        data,
        math_code: int,
    ):
        return _onnx_opset.tensor_product_uniform_4x1d(
            in0,
            in1,
            in2,
            data,
            number_of_output_segments=number_of_output_segments,
            number_of_paths=number_of_paths,
            math_code=math_code,
        )

    @onnxscript.script(_onnx_opset, default_opset=op)
    def onnxscript_symmetric_tensor_contraction_primitive(
        in0,
        in1,
        in2,
        path_vals,
        path_indices,
        path_offsets,
        c0,
        c1,
        c2,
        c3,
        c4,
        c5,
        c6,
        c7,
        c8,
        c9,
        c10,
        c11,
        c12,
        c13,
        c14,
        c15,
        c16,
        c17,
        c18,
        c19,
        c20,
        number_of_input_segments: int,
        number_of_output_segments: int,
        num_coupling_paths: int,
        correlation: int,
    ):
        return _onnx_opset.symmetric_tensor_contraction(
            in0,
            in1,
            in2,
            path_vals,
            path_indices,
            path_offsets,
            number_of_output_segments=number_of_output_segments,
            correlation=correlation,
        )

    @onnxscript.script(_onnx_opset, default_opset=op)
    def onnxscript_batch_linear_fwd_primitive(
        tensor_in,
        tensor_w,
        tensor_w_id: Optional[torch.Tensor],
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
        op_mode: int,
        weight_shared_mode: int,
        tensor_in_stride: int,
        tensor_w_stride: int,
        tensor_out_stride: int,
        num_w_segments: int,
        align_in: int,
        align_out: int,
    ):
        return _onnx_opset.batch_linear(
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
            op_mode=op_mode,
            weight_shared_mode=weight_shared_mode,
            tensor_in_stride=tensor_in_stride,
            tensor_w_stride=tensor_w_stride,
            tensor_out_stride=tensor_out_stride,
            num_w_segments=num_w_segments,
            align_in=align_in,
            align_out=align_out,
        )

    cuequivariance_ops_torch_onnx_registry = torch.onnx.OnnxRegistry()

    cuequivariance_ops_torch_onnx_registry.register_op(
        namespace="cuequivariance_ops_torch",
        op_name="segmented_transpose_primitive",
        overload="default",
        function=onnxscript_segmented_transpose_primitive,
    )

    cuequivariance_ops_torch_onnx_registry.register_op(
        namespace="cuequivariance_ops_torch",
        op_name="fused_tensor_product_fwd_primitive",
        overload="default",
        function=onnxscript_fused_tensor_product_fwd_primitive,
    )

    cuequivariance_ops_torch_onnx_registry.register_op(
        namespace="cuequivariance_ops_torch",
        op_name="tensor_product_uniform_4x1d_fwd_primitive",
        overload="default",
        function=onnxscript_tensor_product_uniform_4x1d_fwd_primitive,
    )

    cuequivariance_ops_torch_onnx_registry.register_op(
        namespace="cuequivariance_ops_torch",
        op_name="symmetric_tensor_contraction_fwd_primitive",
        overload="default",
        function=onnxscript_symmetric_tensor_contraction_primitive,
    )

    cuequivariance_ops_torch_onnx_registry.register_op(
        namespace="cuequivariance_ops_torch",
        op_name="batch_linear_fwd_primitive",
        overload="default",
        function=onnxscript_batch_linear_fwd_primitive,
    )

except ImportError:
    cuequivariance_ops_torch_onnx_registry = None

"""
This section defines run-time plugins, used when running exported ONNX graph with ONNXruntime
"""

try:
    from onnxruntime import SessionOptions
    from onnxruntime_extensions import PyCustomOpDef, get_library_path, onnx_op

    def ort_fused_tensor_product(*args, **kwargs):
        connection_mode = kwargs["connection_mode"]
        output_stride = kwargs["output_stride"]
        cargs = [torch.from_numpy(i).cuda() for i in args]
        return torch.ops.cuequivariance_ops_torch.fused_tensor_product_fwd_primitive(
            *cargs, connection_mode, output_stride
        )

    @onnx_op(
        op_type="cuequivariance_ops::fused_tensor_product",
        inputs=[
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
        ],
        attrs={
            "connection_mode": PyCustomOpDef.dt_int64,
            "output_stride": PyCustomOpDef.dt_int64,
        },
    )
    def ort_fused_tensor_product_fp32(*args, **kwargs):
        return ort_fused_tensor_product(*args, **kwargs)

    @onnx_op(
        op_type="cuequivariance_ops::fused_tensor_product",
        inputs=[
            PyCustomOpDef.dt_float16,
            PyCustomOpDef.dt_float16,
            PyCustomOpDef.dt_float16,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
        ],
        attrs={
            "connection_mode": PyCustomOpDef.dt_int64,
            "output_stride": PyCustomOpDef.dt_int64,
        },
    )
    def ort_fused_tensor_product_fp16(*args, **kwargs):
        return ort_fused_tensor_product(*args, **kwargs)

    def ort_segmented_transpose(in1, in2, **kwargs):
        contiguous = kwargs["contiguous"]
        return torch.ops.cuequivariance_ops_torch.segmented_transpose_primitive(
            torch.from_numpy(in1).cuda(), torch.from_numpy(in2).cuda(), contiguous
        )

    @onnx_op(
        op_type="cuequivariance_ops::segmented_transpose",
        inputs=[PyCustomOpDef.dt_float, PyCustomOpDef.dt_int32],
        attrs={
            "contiguous": PyCustomOpDef.dt_int64,
        },
    )
    def ort_segmented_transpose_fp32(in1, in2, **kwargs):
        return ort_segmented_transpose(in1, in2, **kwargs)

    @onnx_op(
        op_type="cuequivariance_ops::segmented_transpose",
        inputs=[PyCustomOpDef.dt_float16, PyCustomOpDef.dt_int32],
        outputs=[PyCustomOpDef.dt_float16],
        attrs={
            "contiguous": PyCustomOpDef.dt_int64,
        },
    )
    def ort_segmented_transpose_fp16(in1, in2, **kwargs):
        return ort_segmented_transpose(in1, in2, **kwargs)

    @onnx_op(
        op_type="cuequivariance_ops::tensor_product_uniform_4x1d",
        inputs=[
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_int32,
        ],
        attrs={
            "number_of_output_segments": PyCustomOpDef.dt_int64,
            "number_of_paths": PyCustomOpDef.dt_int64,
            "math_code": PyCustomOpDef.dt_int64,
        },
    )
    def ort_tensor_product_uniform_4x1d(*args, **kwargs):
        number_of_output_segments = kwargs["number_of_output_segments"]
        number_of_paths = kwargs["number_of_paths"]
        math_code = kwargs["math_code"]
        cargs = [torch.from_numpy(i).cuda() for i in args]
        return torch.ops.cuequivariance_ops_torch.tensor_product_uniform_4x1d_fwd_primitive(
            cargs[0],
            cargs[1],
            cargs[2],
            number_of_output_segments,
            number_of_paths,
            cargs[3],
            math_code,
        )

    def ort_symmetric_tensor_contraction(*args, **kwargs):
        number_of_output_segments = kwargs["number_of_output_segments"]
        correlation = kwargs["correlation"]
        cargs = [torch.from_numpy(i).cuda() for i in args]
        from cuequivariance_ops_torch.symmetric_tensor_contraction import (
            _symmetric_tensor_contraction_fwd,
        )

        return _symmetric_tensor_contraction_fwd(
            None,
            *cargs,
            number_of_output_segments,
            correlation,
        )

    @onnx_op(
        op_type="cuequivariance_ops::symmetric_tensor_contraction",
        inputs=[
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
        ],
        attrs={
            "number_of_output_segments": PyCustomOpDef.dt_int64,
            "correlation": PyCustomOpDef.dt_int64,
        },
    )
    def _(*args, **kwargs):
        return ort_symmetric_tensor_contraction(*args, **kwargs)

    @onnx_op(
        op_type="cuequivariance_ops::symmetric_tensor_contraction",
        inputs=[
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int64,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
        ],
        attrs={
            "number_of_output_segments": PyCustomOpDef.dt_int64,
            "correlation": PyCustomOpDef.dt_int64,
        },
    )
    def _(*args, **kwargs):
        return ort_symmetric_tensor_contraction(*args, **kwargs)

    def ort_batch_linear(*args, **kwargs):
        op_mode = kwargs["op_mode"]
        weight_shared_mode = kwargs["weight_shared_mode"]
        tensor_in_stride = kwargs["tensor_in_stride"]
        tensor_w_stride = kwargs["tensor_w_stride"]
        tensor_out_stride = kwargs["tensor_out_stride"]
        num_w_segments = kwargs["num_w_segments"]
        align_in = kwargs["align_in"]
        align_out = kwargs["align_out"]
        cargs = [torch.from_numpy(i).cuda() for i in args]
        return torch.ops.cuequivariance_ops_torch.batch_linear_fwd_primitive(
            *cargs,
            op_mode,
            weight_shared_mode,
            tensor_in_stride,
            tensor_w_stride,
            tensor_out_stride,
            num_w_segments,
            align_in,
            align_out,
        )

    @onnx_op(
        op_type="cuequivariance_ops::batch_linear",
        inputs=[
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_float,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
        ],
        attrs={
            "op_mode": PyCustomOpDef.dt_int64,
            "weight_shared_mode": PyCustomOpDef.dt_int64,
            "tensor_in_stride": PyCustomOpDef.dt_int64,
            "tensor_w_stride": PyCustomOpDef.dt_int64,
            "tensor_out_stride": PyCustomOpDef.dt_int64,
            "num_w_segments": PyCustomOpDef.dt_int64,
            "align_in": PyCustomOpDef.dt_int64,
            "align_out": PyCustomOpDef.dt_int64,
        },
    )
    def ort_batch_linear_fp32_fp32(*args, **kwargs):
        return ort_batch_linear(*args, **kwargs)

    @onnx_op(
        op_type="cuequivariance_ops::batch_linear",
        inputs=[
            PyCustomOpDef.dt_float16,
            PyCustomOpDef.dt_float16,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
            PyCustomOpDef.dt_int32,
        ],
        attrs={
            "op_mode": PyCustomOpDef.dt_int64,
            "weight_shared_mode": PyCustomOpDef.dt_int64,
            "tensor_in_stride": PyCustomOpDef.dt_int64,
            "tensor_w_stride": PyCustomOpDef.dt_int64,
            "tensor_out_stride": PyCustomOpDef.dt_int64,
            "num_w_segments": PyCustomOpDef.dt_int64,
            "align_in": PyCustomOpDef.dt_int64,
            "align_out": PyCustomOpDef.dt_int64,
        },
    )
    def ort_batch_linear_fp16_fp32(*args, **kwargs):
        return ort_batch_linear(*args, **kwargs)

    # This function register ORT implementations on runtime side
    def register_custom_ops_library():
        ops = SessionOptions()
        ops.register_custom_ops_library(get_library_path())
        return ops

except ImportError:
    pass

__all__ = ["cuequivariance_ops_torch_onnx_registry"]
