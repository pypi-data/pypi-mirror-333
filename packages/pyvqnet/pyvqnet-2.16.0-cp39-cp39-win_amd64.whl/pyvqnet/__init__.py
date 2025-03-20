# Copyright (c) 2017-2023 Origin Quantum Computing. All Right Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#pylint:disable=too-many-lines
#pylint:disable=unsubscriptable-object
#pylint:disable=no-name-in-module
#pylint:disable=bare-except
#pylint:disable=unnecessary-lambda
#pylint:disable=wrong-import-position
"""
pyvqnet init
"""
from ._core.vqnet import maybe_set_cuda_lazy_init
maybe_set_cuda_lazy_init()

from . import nn, optim, qnn, tensor, utils, data, _core, dtype, device,backends
from .utils import compare_torch_result
from .dtype import kbool, kcomplex128, kcomplex64, kfloat32, kfloat64, \
    kint16, kint32, kint64, kint8, kuint8, C_DTYPE, Z_DTYPE,\
    get_default_dtype,kcomplex32,kfloat16
from .summary import model_summary, summary

from .tensor import QTensor,no_grad,\
    _tensordot as tensordot,reshape,permute,transpose,einsum#this import is use for opt_einsum,which need this function from pyvqnet
from .config import get_if_show_bp_info, set_if_show_bp_info
from .device import DEV_CPU
from .device import DEV_GPU
from .device import DEV_GPU_0
from .device import DEV_GPU_1
from .device import DEV_GPU_2
from .device import DEV_GPU_3
from .device import DEV_GPU_4
from .device import DEV_GPU_5
from .device import DEV_GPU_6
from .device import DEV_GPU_7
from .device import DEV_GPU_MAX
from .device import if_gpu_compiled, if_nccl_compiled, if_mpi_compiled,\
    get_gpu_free_mem
from .types import _size_type


from .logger import get_should_pyvqnet_use_this_log,set_should_pyvqnet_use_this_log
