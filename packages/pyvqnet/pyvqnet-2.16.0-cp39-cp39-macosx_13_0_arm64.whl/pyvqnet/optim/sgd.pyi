from _typeshed import Incomplete
from pyvqnet.backends import check_not_default_backend as check_not_default_backend, get_backend as get_backend
from pyvqnet.optim.optimizer import Optimizer as Optimizer
from pyvqnet.tensor import kfloat32 as kfloat32

vqnet_core: Incomplete

class SGD(Optimizer):
    """
    https://en.wikipedia.org/wiki/Stochastic_gradient_descent


    :param params: params of model which need to be optimized
    :param lr: learning_rate of model (default: 0.01)
    :param momentum: momentum factor (default: 0)
    :param nesterov: enables Nesterov momentum (default: False)
    :return: a SGD optimizer

    Example::

        from pyvqnet.optim import sgd
        import numpy as np
        from pyvqnet.tensor import QTensor
        w = np.arange(24).reshape(1,2,3,4).astype(np.float64)
        param = QTensor(w)
        param.grad = QTensor(np.arange(24).reshape(1,2,3,4).astype(np.float64))
        params = [param]
        opti = sgd.SGD(params)

        for i in range(1,3):
            opti.step()
    """
    t: int
    momentum: Incomplete
    nesterov: Incomplete
    def __init__(self, params, lr: float = 0.01, momentum: int = 0, nesterov: bool = False) -> None: ...
    def update_params(self) -> None: ...
