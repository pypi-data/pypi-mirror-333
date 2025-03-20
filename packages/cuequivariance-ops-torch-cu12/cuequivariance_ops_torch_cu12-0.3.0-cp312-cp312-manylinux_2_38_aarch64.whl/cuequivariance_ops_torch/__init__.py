# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import torch

from cuequivariance_ops_torch._version import __git_commit__, __version__

from cuequivariance_ops_torch import _ext


from cuequivariance_ops_torch.segmented_transpose import (
    segmented_transpose,
)


from cuequivariance_ops_torch.fused_tensor_product import (
    fused_tensor_product,
    FusedTensorProductOp3,
    FusedTensorProductOp4,
    tensor_product_info_as_ctype,
    int_mappings_to_mode,
)


from cuequivariance_ops_torch.symmetric_tensor_contraction import (
    SymmetricTensorContraction,
)

from cuequivariance_ops_torch.batch_linear import (
    BatchLinear,
    batch_linear_info,
)

import os
if os.environ.get('CUEQUIVARIANCE_OPS_USE_JIT', '0') == '1':
    from cuequivariance_ops_torch.tensor_product_uniform_1d_jit import (
        TensorProductUniform1dJit,
    )

    TensorProductUniform4x1d = TensorProductUniform1dJit
    TensorProductUniform1d = TensorProductUniform1dJit
else:
    from cuequivariance_ops_torch.tensor_product_uniform_1d import (
        TensorProductUniform4x1d,
        TensorProductUniform1d,
    )

from cuequivariance_ops_torch.tensor_product_uniform_1d_indexed import (
    TensorProductUniform4x1dIndexed,
    TensorProductUniform3x1dIndexed,
)

__all__ = [
    "segmented_transpose",
    "fused_tensor_product",
    "FusedTensorProductOp3",
    "FusedTensorProductOp4",
    "tensor_product_info_as_ctype",
    "int_mappings_to_mode",
    "SymmetricTensorContraction",
    "TensorProductUniform4x1d",
    "BatchLinear",
    "TensorProductUniform1d",
    "TensorProductUniform4x1dIndexed",
    "TensorProductUniform3x1dIndexed",
]
