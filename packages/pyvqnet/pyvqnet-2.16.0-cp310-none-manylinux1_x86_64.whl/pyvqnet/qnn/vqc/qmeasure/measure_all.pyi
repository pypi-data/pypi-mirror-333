from .... import tensor as tensor
from ....tensor import no_grad as no_grad
from ..qcircuit import I as I, QUnitary as QUnitary, op_class_dict as op_class_dict, qgate_op_creator as qgate_op_creator, save_op_history as save_op_history
from ..qmachine import QMachine as QMachine, not_just_define_op as not_just_define_op, not_save_op_history as not_save_op_history
from ..qop import Observable as Observable
from ..utils.utils import all_wires as all_wires, construct_modules_from_ops as construct_modules_from_ops, get_sum_mat as get_sum_mat, helper_parse_paulisum as helper_parse_paulisum
from .measure_name_dict import get_measure_name_dict as get_measure_name_dict
from .qmeasure import Measurements as Measurements
from .utils import Hermitian_expval as Hermitian_expval, append_measure_proc as append_measure_proc
from _typeshed import Incomplete

def expval(q_machine: QMachine, wires: int | list[int], observables: Observable | list[Observable]): ...

class MeasureAll(Measurements):
    """
    Obtain the expectation value of all the qubits based on Pauli opearators.
    
    If measure the observable like:
        PauliZ(0)@PauliX(0)*0.23+PauliY(1)@PauliZ(0)*-3.5
    use:
        obs = {'Z0 X0': 0.23,'Y1 Z0':-3.5}
    
    If measure the multiple observables like :
        [PauliX(0)*1+PauliY(2)*0.5+PauliZ(3)*0.4,
                PauliX(0)*1+PauliY(1)*0.5+PauliZ(2)*0.4],
    use:
        obs = [{
        'wires': [0, 2, 3],
        'observables': ['X', 'Y', 'Z'],
        'coefficient': [1, 0.5, 0.4]
    }, {
        'wires': [0, 1, 2],
        'observables': ['X', 'Y', 'Z'],
        'coefficient': [1, 0.5, 0.4]
    }]
    
    If measure the multiple observables like :
        [PauliX(0)*0.23+PauliY(1)*-3.5,
                PauliX(0)*1+PauliY(1)*0.5+PauliZ(2)*0.4],

    use:
        obs = [{'Z0 X0': 0.23,'Y1 Z0':-3.5},
         {
        'wires': [0, 1, 2],
        'observables': ['X', 'Y', 'Z'],
        'coefficient': [1, 0.5, 0.4]
    }]
    
    """
    q_machine: Incomplete
    def __init__(self, obs, name: str = '') -> None: ...
    def measure_fun_complex_ob(self, q_machine: QMachine, obs):
        """
        deal with pauli string dict or lsit of pauli string
        """
    def measure_fun_simple_basis(self, q_machine: QMachine, obs): ...
    def forward(self, q_machine: QMachine): ...
    def run_multi_or_single_measure(self, q_machine): ...
    def __call__(self, *args, **kwargs): ...
