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
from typing import List, Optional

import torch
import torch.nn as nn

import cuequivariance_ops_torch._ext as ext

logger = logging.getLogger(__name__)


def _setup_context(ctx, inputs, output):
    ctx.inputs = inputs[:-1]
    ctx.save_for_backward(*inputs[-1])


# batch_dim: 0 shared, 1 batched, -1 indexed
BATCH_DIM_SHARED = 0
BATCH_DIM_BATCHED = 1
BATCH_DIM_INDEXED = -1
BATCH_DIM_AUTO = -2


def _handle_batch_dim_auto(batch_size, batch_dim, tensors):
    new_batch_size = batch_size
    new_batch_dim = list(batch_dim)
    for idx, (bd, t) in enumerate(zip(batch_dim, tensors)):
        if bd == BATCH_DIM_SHARED:
            torch._assert(t.shape[0] == 1, "shared batch dim must be 1")
        elif bd == BATCH_DIM_INDEXED:
            continue
        elif bd == BATCH_DIM_BATCHED:
            if new_batch_size == BATCH_DIM_AUTO:
                new_batch_size = t.shape[0]
            else:
                torch._assert(new_batch_size == t.shape[0], "batch dim mismatch")
        elif bd == BATCH_DIM_AUTO:
            if t.shape[0] == 1:
                new_batch_dim[idx] = BATCH_DIM_SHARED
            else:
                if new_batch_size == BATCH_DIM_AUTO:
                    new_batch_size = t.shape[0]
                else:
                    torch._assert(new_batch_size == t.shape[0], "batch dim mismatch")
                new_batch_dim[idx] = BATCH_DIM_BATCHED
        else:
            raise ValueError(f"Unknown batch dim kind {bd}")

    # Handle outputs
    for idx in range(len(tensors), len(batch_dim)):
        bd = batch_dim[idx]
        if bd == BATCH_DIM_AUTO:
            new_batch_dim[idx] = BATCH_DIM_BATCHED

    if new_batch_size == BATCH_DIM_AUTO:
        new_batch_size = 1

    if new_batch_size == 1:
        for idx in range(len(new_batch_dim)):
            if new_batch_dim[idx] == BATCH_DIM_SHARED:
                new_batch_dim[idx] = BATCH_DIM_BATCHED

    assert new_batch_size != BATCH_DIM_AUTO
    assert all(bs != BATCH_DIM_AUTO for bs in new_batch_dim)
    return new_batch_size, new_batch_dim


# dtypes: determines from which dtype to take that output buffer's dtype
# may be -1, which is the math_dtype
# index_buffer: the index buffer to use for the given tensor. ignored for non-indexed tensors. for index buffers, it contains the max value + 1, i.e. the size that is needed from the tensor
@torch.library.custom_op(
    "cuequivariance_ops::tensor_product_uniform_1d_jit",
    mutates_args=(),
    device_types="cuda",
)
def _(
    name: str,
    math_dtype: torch.dtype,
    operand_extent: int,
    num_inputs: int,
    num_outputs: int,
    num_index: int,
    buffer_dim: List[int],
    buffer_num_segments: List[int],
    batch_dim: List[int],
    index_buffer: List[int],
    dtypes: List[int],
    num_operations: int,
    num_operands: List[int],
    operations: List[int],
    num_paths: List[int],
    path_indices_start: List[int],
    path_coefficients_start: List[int],
    path_indices: List[int],
    path_coefficients: List[float],
    batch_size: int,
    tensors: List[torch.Tensor],
) -> List[torch.Tensor]:
    batch_size, batch_dim = _handle_batch_dim_auto(batch_size, batch_dim, tensors)
    outputs = []
    for i in range(num_inputs, num_inputs + num_outputs):
        if batch_dim[i] == BATCH_DIM_SHARED:
            size_0 = 1
        elif batch_dim[i] == BATCH_DIM_BATCHED:
            size_0 = batch_size
        elif batch_dim[i] == BATCH_DIM_INDEXED:
            size_0 = index_buffer[index_buffer[i]]
        if buffer_dim[i] == 0:
            size_1 = buffer_num_segments[i]
        if buffer_dim[i] == 1:
            size_1 = operand_extent * buffer_num_segments[i]
        if dtypes[i] == -1:
            dtype = math_dtype
        else:
            dtype = tensors[dtypes[i]].dtype
        outputs.append(
            torch.empty((size_0, size_1), dtype=dtype, device=tensors[0].device)
        )

    for i in range(num_inputs, num_outputs):
        if batch_dim[i] == BATCH_DIM_SHARED or batch_dim[i] == BATCH_DIM_INDEXED:
            outputs[i - num_inputs].zero_()

    jit = ext.tensor_product_uniform_1d_jit

    def map_dtype(t):
        if t == torch.float64:
            return jit.Datatype.kFloat64
        if t == torch.float32:
            return jit.Datatype.kFloat32
        if t == torch.float16:
            return jit.Datatype.kFloat16
        if t == torch.bfloat16:
            return jit.Datatype.kBFloat16

    def map_buffer_dim(o):
        if o == 0:
            return jit.Dimension.kScalar
        if o == 1:
            return jit.Dimension.kOneDimensional
        raise ValueError(f"Unknown dimension {o}")

    def map_batch_dim(o):
        if o == BATCH_DIM_BATCHED:
            return jit.BatchDimension.kBatched
        if o == BATCH_DIM_SHARED:
            return jit.BatchDimension.kShared
        if o == BATCH_DIM_INDEXED:
            return jit.BatchDimension.kIndexed
        raise ValueError(f"Unknown batch dimension {o}")

    operation_index = 0
    ops = []
    for i in range(num_operations):
        ops.append(operations[operation_index : operation_index + num_operands[i]])
        operation_index += num_operands[i]

    tensors = [t.contiguous() for t in tensors]
    jit.run(
        name,
        map_dtype(math_dtype),
        operand_extent,
        num_inputs,
        num_outputs,
        num_index,
        [map_buffer_dim(b) for b in buffer_dim],
        buffer_num_segments,
        [map_batch_dim(b) for b in batch_dim],
        index_buffer[: num_inputs + num_outputs],
        [map_dtype(t.dtype) for t in tensors[:num_inputs] + outputs],
        ops,
        num_paths,
        path_indices_start,
        path_coefficients_start,
        path_indices,
        path_coefficients,
        batch_size,
        tensors[:num_inputs] + outputs + tensors[num_inputs:],
        torch.cuda.current_stream().cuda_stream,
    )
    return outputs


@torch.library.register_fake(
    "cuequivariance_ops::tensor_product_uniform_1d_jit",
)
def _(
    name: str,
    math_dtype: torch.dtype,
    operand_extent: int,
    num_inputs: int,
    num_outputs: int,
    num_index: int,
    buffer_dim: List[int],
    buffer_num_segments: List[int],
    batch_dim: List[int],
    index_buffer: List[int],
    dtypes: List[int],
    num_operations: int,
    num_operands: List[int],
    operations: List[int],
    num_paths: List[int],
    path_indices_start: List[int],
    path_coefficients_start: List[int],
    path_indices: List[int],
    path_coefficients: List[float],
    batch_size: int,
    tensors: List[torch.Tensor],
) -> List[torch.Tensor]:
    batch_size, batch_dim = _handle_batch_dim_auto(batch_size, batch_dim, tensors)
    outputs = []
    for i in range(num_inputs, num_inputs + num_outputs):
        if batch_dim[i] == BATCH_DIM_SHARED:
            size_0 = 1
        elif batch_dim[i] == BATCH_DIM_BATCHED:
            size_0 = batch_size
        elif batch_dim[i] == BATCH_DIM_INDEXED:
            size_0 = index_buffer[index_buffer[i]]
        if buffer_dim[i] == 0:
            size_1 = buffer_num_segments[i]
        if buffer_dim[i] == 1:
            size_1 = operand_extent * buffer_num_segments[i]
        if dtypes[i] == -1:
            dtype = math_dtype
        else:
            dtype = tensors[dtypes[i]].dtype
        outputs.append(
            torch.empty((size_0, size_1), dtype=dtype, device=tensors[0].device)
        )
    return outputs


def _do_bwd_jit(ctx, grad):
    (
        orig_name,
        orig_math_dtype,
        orig_operand_extent,
        orig_num_inputs,
        orig_num_outputs,
        orig_num_index,
        orig_buffer_dim,
        orig_buffer_num_segments,
        orig_batch_dim,
        orig_index_buffer,
        orig_dtypes,
        orig_num_operations,
        orig_num_operands,
        orig_operations,
        orig_num_paths,
        orig_path_indices_start,
        orig_path_coefficients_start,
        orig_path_indices,
        orig_path_coefficients,
        orig_batch_size,
    ) = ctx.inputs

    orig_tensors = ctx.saved_tensors

    orig_batch_size, orig_batch_dim = _handle_batch_dim_auto(
        orig_batch_size, orig_batch_dim, orig_tensors
    )

    if "_fwd" in orig_name:
        # last arg to replace() is maxreplace
        bwd_name = orig_name.replace("_fwd", "_bwd", 1)
    elif "_bwd" in orig_name:
        bwd_name = orig_name.replace("_bwd", "_bwd_bwd", 1)
    else:
        bwd_name = orig_name + "_bwd"

    bwd_math_dtype = orig_math_dtype
    bwd_operand_extent = orig_operand_extent
    bwd_num_inputs = orig_num_inputs + orig_num_outputs
    bwd_num_outputs = sum(1 if ng else 0 for ng in ctx.needs_input_grad[-1])
    bwd_num_index = orig_num_index
    bwd_buffer_dim = orig_buffer_dim + [
        orig_buffer_dim[idx] for idx, ng in enumerate(ctx.needs_input_grad[-1]) if ng
    ]
    bwd_buffer_num_segments = orig_buffer_num_segments + [
        orig_buffer_num_segments[idx]
        for idx, ng in enumerate(ctx.needs_input_grad[-1])
        if ng
    ]
    bwd_batch_dim = orig_batch_dim + [
        orig_batch_dim[idx] for idx, ng in enumerate(ctx.needs_input_grad[-1]) if ng
    ]
    bwd_index_buffer = (
        orig_index_buffer[: orig_num_inputs + orig_num_outputs]
        + [
            orig_index_buffer[idx]
            for idx, ng in enumerate(ctx.needs_input_grad[-1])
            if ng
        ]
        + orig_index_buffer[orig_num_inputs + orig_num_outputs :]
    )
    bwd_dtypes = orig_dtypes + [
        orig_dtypes[idx] for idx, ng in enumerate(ctx.needs_input_grad[-1]) if ng
    ]

    operation_index = 0
    orig_ops = []
    for i in range(orig_num_operations):
        orig_ops.append(
            orig_operations[operation_index : operation_index + orig_num_operands[i]]
        )
        operation_index += orig_num_operands[i]

    bwd_ops = []
    bwd_num_paths = []
    bwd_path_indices_start = []
    bwd_path_coefficients_start = []
    output_idx = bwd_num_inputs
    for ng_idx, ng in enumerate(ctx.needs_input_grad[-1]):
        if not ng:
            continue
        # we want the derivative of input operand "idx"
        # and store it into output operand bwd_num_input_operands + output_idx
        # we have the gradients of the previous outputs in buffers orig_num_inputs ... orig_num_inputs + orig_num_outputs
        #   i.e. we can keep them as is!
        for ops_idx, op in enumerate(orig_ops):
            # for a given operation, if it uses "idx" at a position k:
            #   we replace "idx" at that position k with the output operand
            #   we replace the output operand with its gradient
            #   we add that to the list of operations
            #   we also have to replicate num_paths, num_indices_start, num_coefficients_start
            for op_idx, k in enumerate(op):
                if k == ng_idx:
                    bwd_op = list(op)
                    bwd_op[op_idx] = output_idx
                    bwd_ops.append(bwd_op)
                    bwd_num_paths.append(orig_num_paths[ops_idx])
                    bwd_path_indices_start.append(orig_path_indices_start[ops_idx])
                    bwd_path_coefficients_start.append(
                        orig_path_coefficients_start[ops_idx]
                    )

        output_idx += 1

    bwd_num_operations = len(bwd_ops)
    bwd_num_operands = [len(o) for o in bwd_ops]
    bwd_operations = [e for o in bwd_ops for e in o]

    bwd_path_indices = orig_path_indices
    bwd_path_coefficients = orig_path_coefficients
    bwd_batch_size = orig_batch_size

    bwd_tensors = (
        list(orig_tensors[:orig_num_inputs])
        + list(grad)
        + list(orig_tensors[orig_num_inputs:])
    )

    bwd_output = torch.ops.cuequivariance_ops.tensor_product_uniform_1d_jit(
        bwd_name,
        bwd_math_dtype,
        bwd_operand_extent,
        bwd_num_inputs,
        bwd_num_outputs,
        bwd_num_index,
        bwd_buffer_dim,
        bwd_buffer_num_segments,
        bwd_batch_dim,
        bwd_index_buffer,
        bwd_dtypes,
        bwd_num_operations,
        bwd_num_operands,
        bwd_operations,
        bwd_num_paths,
        bwd_path_indices_start,
        bwd_path_coefficients_start,
        bwd_path_indices,
        bwd_path_coefficients,
        bwd_batch_size,
        bwd_tensors,
    )

    grad_list = []
    output_idx = 0
    for ng_idx, ng in enumerate(ctx.needs_input_grad[-1]):
        if not ng:
            grad_list.append(None)
        else:
            grad_list.append(bwd_output[output_idx])
            output_idx += 1

    grad_input = [None] * len(ctx.inputs)
    return *grad_input, grad_list


torch.library.register_autograd(
    "cuequivariance_ops::tensor_product_uniform_1d_jit",
    _do_bwd_jit,
    setup_context=_setup_context,
)


class TensorProductUniform1dJit(nn.Module):
    SUPPORTED_DIMS = [3, 4]
    SUPPORTED_EXTENT_MULTIPLE = 32
    SUPPORTED_TOTAL_SEGMENTS = 256

    @classmethod
    def is_supported(
        cls,
        operand_dim: list[int],
        operand_extent: int,
        operand_num_segments: list[int],
    ):
        """
        Check if the kernel supports operations with the given parameters.

        See ``__init__`` for a description of the paramters.
        """
        num_operands = len(operand_num_segments)
        try:
            assert num_operands in cls.SUPPORTED_DIMS
            assert len(operand_dim) == num_operands
            # assert operand_extent % cls.SUPPORTED_EXTENT_MULTIPLE == 0
            # assert sum(operand_num_segments) <= cls.SUPPORTED_TOTAL_SEGMENTS
        except AssertionError:
            return False
        return True

    def __init__(
        self,
        operand_dim: list[int],
        operand_extent: int,
        operand_num_segments: list[int],
        path_indices: list[list[int]],
        path_coefficients: list[float],
        math_dtype: torch.dtype = torch.float32,
    ):
        """
        A tensor product implementation for scalar and vector operands where
        all vectors have the same length.

        Parameters
        ----------
        operand_dim: list[int]
            ``operand_dim[i]`` may be either 0 or 1, and indicates whether that
            operand ``i`` has scalar (0-dimensional) or vector (1-dimensional)
            segments.
        operand_extent: int
            The extent (number of elements) of each vector operand segment. Must
            be a multiple of ``SUPPORTED_EXTENT_MULTIPLE``.
        operand_num_segments: list[int]
            The number of segments for each operand.
        path_indices: list[list[int]]
            Each element of this list is a single computation, i.e. which input
            operands get multiplied together and then and added to which output
            segment.
        path_coefficients: list[float]
            The scaling factor for each entry in ``path_indices``.
        math_dtype: torch.dtype
            The data type used for internal computation. May be FP32 or FP64.
            All inputs will be cast to this type, and all multiplications and
            additions will be performed at this precision (except for atomic
            output accumulation, which occurs at input precision).

        Example
        -------
        For this example, let's say that we use this kernel to implement
        complex-complex multiplication, i.e. two inputs, one output
        (three operands total) and two segments each (real and imaginary).
        Then, this would encode the multiplication rule:

        >>> m = TensorProductUniform1d(
        ...        [1, 1, 1], 32, [2, 2, 2],
        ...        [[0, 0, 0], [1, 1, 0], [1, 0, 1], [0, 1, 1]],
        ...        [1.0, -1.0, 1.0, 1.0])

        This encodes the following operation with plain torch:

        >>> input_0_segment_0 = torch.randn((batch, 32,))
        >>> input_0_segment_1 = torch.randn((batch, 32,))
        >>> input_1_segment_0 = torch.randn((batch, 32,))
        >>> input_1_segment_1 = torch.randn((batch, 32,))
        >>> output_segment_0 = input_0_segment_0 * input_1_segment_0 - \
        ...     input_0_segment_1 * input_1_segment_1
        >>> output_segment_1 = input_0_segment_0 * input_1_segment_1 + \
        ...     input_0_segment_1 * input_1_segment_0

        Or, using our kernel:

        >>> input_0 = torch.randn((batch, 2*32), device='cuda')
        >>> input_1 = torch.randn((batch, 2*32), device='cuda')
        >>> m = m.to('cuda')
        >>> output = m(input_0, input_1)

        """
        assert self.is_supported(operand_dim, operand_extent, operand_num_segments)
        assert len(path_indices) == len(path_coefficients)
        assert len(path_coefficients) > 0
        self.num_operands = len(operand_num_segments)
        assert all(
            len(path_indices[i]) == self.num_operands
            for i, _ in enumerate(path_indices)
        )
        logger.debug(
            "TensorProductUniform4x1d.__init__("
            + f"operand_dim={operand_dim}, operand_extent={operand_extent}, "
            + f"operand_num_segments={operand_num_segments}, path_indices=..., "
            + f"path_coefficients=..., math_dtype={math_dtype})"
        )
        logger.debug(
            f"TensorProductUniform4x1d.__init__(path_indices={path_indices}, "
            + f"path_coefficients={path_coefficients})"
        )

        super().__init__()

        self.number_of_output_segments = operand_num_segments[-1]
        self.number_of_paths = len(path_indices)
        self.math_dtype = math_dtype

        self.operand_dim = operand_dim
        self.operand_extent = operand_extent
        self.operand_num_segments = operand_num_segments
        self.path_indices = path_indices
        self.path_indices_flat = [pi for p in path_indices for pi in p]
        self.path_coefficients = path_coefficients

        self.batch_dim_auto = BATCH_DIM_AUTO

    def forward(
        # Torch FX strongly dislikes *args usage here
        self,
        in0: torch.Tensor,
        in1: torch.Tensor,
        in2: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Execute the TensorProductUniform1d kernel.

        For an example, see ``__init__``.

        Each operand is a torch tensor with one or two dimensions. If it is two-
        dimensional, the first dimension is the batch dimension and must match
        across all input tensors that have a batch dimension. It will also be
        the first dimension of the returned tensor.
        Generally, a sufficiently large batch dimension is required for good
        performance. The last tensor dimension contains all the segments of the
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

        Returns
        -------
        torch.Tensor
            The last (output) operand of the tensor product.
        """

        if in2 is not None:
            ins = [in0, in1, in2]
            torch._assert(len(self.operand_dim) == 4, "Must pass three tensors")
        else:
            ins = [in0, in1]
            torch._assert(len(self.operand_dim) == 3, "Must pass two tensors")
        return torch.ops.cuequivariance_ops.tensor_product_uniform_1d_jit(
            "kernel_fwd",
            self.math_dtype,
            self.operand_extent,
            len(self.operand_dim) - 1,
            1,
            0,
            self.operand_dim,
            self.operand_num_segments,
            [self.batch_dim_auto] * len(self.operand_dim),
            [-1] * len(self.operand_dim),
            list(range(len(self.operand_dim) - 1)) + [0],
            1,
            [len(self.operand_dim)],
            list(range(len(self.operand_dim))),
            [len(self.path_coefficients)],
            [0],
            [0],
            self.path_indices_flat,
            self.path_coefficients,
            self.batch_dim_auto,
            ins,
        )[0]


__all__ = ["TensorProductUniform1dJit"]
