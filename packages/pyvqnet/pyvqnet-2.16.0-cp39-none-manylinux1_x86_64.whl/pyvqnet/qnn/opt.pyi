from _typeshed import Incomplete

__all__ = ['SPSA', 'QNG', 'insert_pauli_for_mt', 'get_metric_tensor', 'quantum_fisher', 'Gradient_Prune_Instance']

class SPSA:
    """
    Simultaneous Perturbation Stochastic Approximation (SPSA) optimizer.

    SPSA provides a stochastic method for approximating the gradient of a
    multivariate differentiable cost function. To accomplish this the cost 
    function is evaluated twice using perturbed parameter vectors: every 
    component of the original parameter vector is simultaneously shifted 
    with a randomly generated value.

    Many examples are presented at the `SPSA Web site <http://www.jhuapl.edu/SPSA>`__.


    """
    def __init__(self, maxiter: int = 1000, last_avg: int = 1, c0: float = ..., c1: float = 0.2, c2: float = 0.602, c3: float = 0.101, c4: float = 0, init_para: Incomplete | None = None, model: Incomplete | None = None, calibrate_flag: bool = False) -> None:
        '''

            :param maxiter: Maximum number of iterations to perform. Default: 1000.
            :param last_avg: Averaged parameters over the last_avg iterations.
                If last_avg = 1, only the last iteration is considered. Default: 1.
            :param c0: The initial a. Step size to update parameters. Default: 0.2*pi
            :param c1: The initial c. The step size used to approximate gradient. Default: 0.1.
            :param c2: The alpha in the paper, and it is used to adjust a (c0) at each iteration. Default: 0.602.
            :param c3: The gamma in the paper, and it is used to adjust c (c1) at each iteration. Default: 0.101.
            :param c4: The parameter used to control a as well. Default: 0.
            :param init_para: init param for sgd. Default: None.
            :param model: model. Default: None.
            :param calibrate_flag: if calibrate hpyerparameters a and c,default:False.

            Example::

                from pyvqnet.qnn import AngleEmbeddingCircuit, expval, QuantumLayerV2, SPSA
                from pyvqnet.qnn.template import BasicEntanglerTemplate
                import pyqpanda as pq

                class Model_spsa(Module):
                    def __init__(self):
                        super(Model_spsa, self).__init__()
                        #self.qvc = NoiseQuantumLayer(qvc_circuits, 24, "noise", 4,4)
                        self.qvc = QuantumLayerV2(layer_fn_spsa_pq, 3)
                        # self.linear1 = Linear(2, 5)
                        # self.linear2 = Linear(5, 2)

                    def forward(self, x):
                        y = self.qvc(x)
                        return y


                def layer_fn_spsa_pq(input, weights):
                    num_of_qubits = 1

                    m_machine = pq.CPUQVM()  # outside
                    m_machine.init_qvm()  # outside
                    qubits = m_machine.qAlloc_many(num_of_qubits)
                    c1 = AngleEmbeddingCircuit(input, qubits)
                    weights =weights.reshape([4,1])

                    bc_class = BasicEntanglerTemplate(weights, 1)
                    c2 = bc_class.create_circuit(qubits)
                    m_prog = pq.QProg()
                    m_prog.insert(c1)
                    m_prog.insert(c2)
                    pauli_dict = {\'Z0\': 1}
                    exp2 = expval(m_machine, m_prog, pauli_dict, qubits)

                    return exp2

                model = Model_spsa()

                optimizer = SPSA(maxiter=20,
                    init_para=model.parameters(),
                    model=model,
                )
                data = QTensor(np.array([[0.27507603]]))
                p = model.parameters()
                p[0].data = pyvqnet._core.Tensor( np.array([3.97507603, 3.12950603, 1.00854038,
                                1.25907603]))
                optimizer._step(input_data=data)
                y = model(data)
                print(y)

        '''
    def optimize(self, obj_fun, train_para, maxiter, save_steps: int = 5, last_avg: int = 1):
        """
            optimize for sapa optimizer
            """
    def calibrate(self, model_func, input_data, c: float = 0.2):
        """Calibrate SPSA parameters with a powerseries as learning rate and perturbation coeffs.
        """

class pyqpanda_config_wrapper:
    """
    A wrapper for pyqpanda config,including QVM machine, allocated qubits, classic bits.
    """
    def __init__(self, qubits_num) -> None: ...
    def __del__(self) -> None: ...

def get_metric_tensor(py_qpanda_config, params, target_gate_type_lists, target_gate_bits_lists, qcir_lists, wires):
    """
        Use block-diagonal approximation to calculate the metric tensor described below:

    .. math::

        \\text{metric_tensor}_{i, j} = \\text{Re}\\left[ \\langle \\partial_i \\psi(\\bm{\\theta}) | \\partial_j \\psi(\\bm{\\theta}) \\rangle
        - \\langle \\partial_i \\psi(\\bm{\\theta}) | \\psi(\\bm{\\theta}) \\rangle \\langle \\psi(\\bm{\\theta}) | \\partial_j \\psi(\\bm{\\theta}) \\rangle \\right]

    with short notation :math:`| \\partial_j \\psi(\\bm{\\theta}) \\rangle := \\frac{\\partial}{\\partial \\theta_j}| \\psi(\\bm{\\theta}) \\rangle`.
     see `arxiv:2103.15191 <https://arxiv.org/abs/2103.15191>`_.

    .. note::

        Only RX,RY,RZ gate is supported currently.

    :param params: variable parameters in circuit.
    :param target_gate_type_lists: the target parametrized gate or gates in the circuit which can be regarded as a single layer. 'RX','RY','RZ' or lists is supported.
    :param target_gate_bits_lists: which qubit or qubits are the target parametrized gate act on.
    :param qcir_lists: the quantum cir list before the target parametrized gate to calculate metric tensor, see examples below.
    :param wires: the total qubits index of quantum circuits.

    Example::

        def target_circuit(
                q_input_features,
                params,
                qubits,
                cubits,
                machine):
            qcir = pq.QCircuit()
            qcir.insert(pq.RY(qubits[0], np.pi / 4))
            qcir.insert(pq.RY(qubits[1], np.pi / 3))
            qcir.insert(pq.RY(qubits[2], np.pi / 7))

            qcir.insert(pq.RZ(qubits[0], params[0]))
            qcir.insert(pq.RY(qubits[1], params[1]))

            qcir.insert(pq.CNOT(qubits[0], qubits[1]))
            qcir.insert(pq.CNOT(qubits[1], qubits[2]))
            qcir.insert(pq.RX(qubits[2], params[2]))

            qcir.insert(pq.CNOT(qubits[0], qubits[1]))
            qcir.insert(pq.CNOT(qubits[1], qubits[2]))
            m_prog = pq.QProg()
            m_prog.insert(qcir)

            return expval(machine, m_prog, {'Y0': 1}, qubits)

        # circuit before parametrized gates layer 0 in target_circuit

        def layer0_subcircuit(config: pyqpanda_config_wrapper, params):
            qcir = pq.QCircuit()
            qcir.insert(pq.RY(config._qubits[0], np.pi / 4))
            qcir.insert(pq.RY(config._qubits[1], np.pi / 3))
            return qcir

        def layer1_subcircuit(config: pyqpanda_config_wrapper, params):
            qcir = pq.QCircuit()
            qcir.insert(pq.RY(config._qubits[0], np.pi / 4))
            qcir.insert(pq.RY(config._qubits[1], np.pi / 3))
            qcir.insert(pq.RY(config._qubits[2], np.pi / 7))

            qcir.insert(pq.RZ(config._qubits[0], params[0]))
            qcir.insert(pq.RY(config._qubits[1], params[1]))

            qcir.insert(pq.CNOT(config._qubits[0], config._qubits[1]))
            qcir.insert(pq.CNOT(config._qubits[1], config._qubits[2]))

            return qcir

        def get_p01_diagonal_(config, params, target_gate_type, target_gate_bits,
                            wires):
            qcir = layer0_subcircuit(config, params)
            qcir2 = insert_pauli_for_mt(config._qubits, target_gate_type,
                                        target_gate_bits)
            qcir3 = pq.QCircuit()
            qcir3.insert(qcir)
            qcir3.insert(qcir2)
            m_prog = pq.QProg()
            m_prog.insert(qcir3)
            return ProbsMeasure(wires, m_prog, config._machine, config._qubits)

        def get_p1_diagonal_(config, params, target_gate_type, target_gate_bits,
                            wires):
            qcir = layer1_subcircuit(config, params)
            qcir2 = insert_pauli_for_mt(config._qubits, target_gate_type,
                                        target_gate_bits)
            qcir3 = pq.QCircuit()
            qcir3.insert(qcir)
            qcir3.insert(qcir2)
            m_prog = pq.QProg()
            m_prog.insert(qcir3)

            return ProbsMeasure(wires, m_prog, config._machine, config._qubits)

        config = pyqpanda_config_wrapper(3)
        qcir = []
        qcir.append(get_p01_diagonal_)
        qcir.append(get_p1_diagonal_)
        params2 = QTensor([0.432, 0.543, 0.233])

        mt = get_metric_tensor(config, params2, [['RZ', 'RY'], ['RX']],
                                [[0, 1], [2]], qcir, [0, 1, 2])

        print(mt)

    """
def quantum_fisher(py_qpanda_config, params, target_gate_type_lists, target_gate_bits_lists, qcir_lists, wires):
    """
        Returns a function that computes the quantum fisher information matrix (QFIM).
        
        .. math::

        \\text{QFIM}_{i, j} = 4 \\text{Re}\\left[ \\langle \\partial_i \\psi(\\bm{\\theta}) | \\partial_j \\psi(\\bm{\\theta}) \\rangle
        - \\langle \\partial_i \\psi(\\bm{\\theta}) | \\psi(\\bm{\\theta}) \\rangle \\langle \\psi(\\bm{\\theta}) | \\partial_j \\psi(\\bm{\\theta}) \\rangle \\right]

    with short notation :math:`| \\partial_j \\psi(\\bm{\\theta}) \\rangle := \\frac{\\partial}{\\partial \\theta_j}| \\psi(\\bm{\\theta}) \\rangle`.

    .. note::

        Only RX,RY,RZ gate is supported currently.

    :param params: variable parameters in circuit.
    :param target_gate_type_lists: the target parametrized gate or gates in the circuit which can be regarded as a single layer. 'RX','RY','RZ' or lists is supported.
    :param target_gate_bits_lists: which qubit or qubits are the target parametrized gate act on.
    :param qcir_lists: the quantum cir list before the target parametrized gate to calculate metric tensor, see examples below.
    :param wires: the total qubits index of quantum circuits.
    
    Example::
    
        import pyqpanda as pq

        from pyvqnet import *
        from pyvqnet.qnn.opt import pyqpanda_config_wrapper, insert_pauli_for_mt, quantum_fisher
        from pyvqnet.qnn import ProbsMeasure
        import numpy as np
        import pennylane as qml
        import pennylane.numpy as pnp

        n_wires = 4
        def layer_subcircuit_new(config: pyqpanda_config_wrapper, params):
            qcir = pq.QCircuit()
            qcir.insert(pq.RX(config._qubits[0], params[0]))
            qcir.insert(pq.RY(config._qubits[1], params[1]))
            
            qcir.insert(pq.CNOT(config._qubits[0], config._qubits[1]))
            
            qcir.insert(pq.RZ(config._qubits[2], params[2]))
            qcir.insert(pq.RZ(config._qubits[3], params[3]))
            return qcir


        def get_p1_diagonal_new(config, params, target_gate_type, target_gate_bits,
                            wires):
            qcir = layer_subcircuit_new(config, params)
            qcir2 = insert_pauli_for_mt(config._qubits, target_gate_type,
                                        target_gate_bits)
            qcir3 = pq.QCircuit()
            qcir3.insert(qcir)
            qcir3.insert(qcir2)
            
            m_prog = pq.QProg()
            m_prog.insert(qcir3)
            return ProbsMeasure(wires, m_prog, config._machine, config._qubits)

        config = pyqpanda_config_wrapper(n_wires)
        qcir = []
        
        qcir.append(get_p1_diagonal_new)

        params2 = QTensor([0.5, 0.5, 0.5, 0.25], requires_grad=True)

        mt = quantum_fisher(config, params2, [['RX', 'RY', 'RZ', 'RZ']],
                                [[0, 1, 2, 3]], qcir, [0, 1, 2, 3])

        # The above example shows that there are no identical gates in the same layer, 
        # but in the same layer you need to modify the logic gates according to the following example.
        
        n_wires = 3
        def layer_subcircuit_01(config: pyqpanda_config_wrapper, params):
            qcir = pq.QCircuit()
            qcir.insert(pq.RX(config._qubits[0], params[0]))
            qcir.insert(pq.RY(config._qubits[1], params[1]))
            qcir.insert(pq.CNOT(config._qubits[0], config._qubits[1]))
            
            return qcir

        def layer_subcircuit_02(config: pyqpanda_config_wrapper, params):
            qcir = pq.QCircuit()
            qcir.insert(pq.RX(config._qubits[0], params[0]))
            qcir.insert(pq.RY(config._qubits[1], params[1]))
            qcir.insert(pq.CNOT(config._qubits[0], config._qubits[1]))
            qcir.insert(pq.RZ(config._qubits[1], params[2]))
            return qcir

        def layer_subcircuit_03(config: pyqpanda_config_wrapper, params):
            qcir = pq.QCircuit()
            qcir.insert(pq.RX(config._qubits[0], params[0]))
            qcir.insert(pq.RY(config._qubits[1], params[1]))
            qcir.insert(pq.CNOT(config._qubits[0], config._qubits[1])) #  01 part
            
            qcir.insert(pq.RZ(config._qubits[1], params[2]))  #  02 part
            
            qcir.insert(pq.RZ(config._qubits[1], params[3]))
            return qcir

        def get_p1_diagonal_01(config, params, target_gate_type, target_gate_bits,
                            wires):
            qcir = layer_subcircuit_01(config, params)
            qcir2 = insert_pauli_for_mt(config._qubits, target_gate_type,
                                        target_gate_bits)
            qcir3 = pq.QCircuit()
            qcir3.insert(qcir)
            qcir3.insert(qcir2)
            
            m_prog = pq.QProg()
            m_prog.insert(qcir3)
            return ProbsMeasure(wires, m_prog, config._machine, config._qubits)
        
        def get_p1_diagonal_02(config, params, target_gate_type, target_gate_bits,
                            wires):
            qcir = layer_subcircuit_02(config, params)
            qcir2 = insert_pauli_for_mt(config._qubits, target_gate_type,
                                        target_gate_bits)
            qcir3 = pq.QCircuit()
            qcir3.insert(qcir)
            qcir3.insert(qcir2)
            
            m_prog = pq.QProg()
            m_prog.insert(qcir3)
            return ProbsMeasure(wires, m_prog, config._machine, config._qubits)
        
        def get_p1_diagonal_03(config, params, target_gate_type, target_gate_bits,
                            wires):
            qcir = layer_subcircuit_03(config, params)
            qcir2 = insert_pauli_for_mt(config._qubits, target_gate_type,
                                        target_gate_bits)
            qcir3 = pq.QCircuit()
            qcir3.insert(qcir)
            qcir3.insert(qcir2)
            
            m_prog = pq.QProg()
            m_prog.insert(qcir3)
            return ProbsMeasure(wires, m_prog, config._machine, config._qubits)
        
        config = pyqpanda_config_wrapper(n_wires)
        qcir = []
        
        qcir.append(get_p1_diagonal_01)
        qcir.append(get_p1_diagonal_02)
        qcir.append(get_p1_diagonal_03)
        
        params2 = QTensor([0.5, 0.5, 0.5, 0.25], requires_grad=True)

        mt = quantum_fisher(config, params2, [['RX', 'RY'], ['RZ'], ['RZ']], # rx,ry counts as layer one, first rz as layer two, second rz as layer three.
                                [[0, 1], [1], [1]], qcir, [0, 1])
    """
def insert_pauli_for_mt(qubits, target_gate_type, target_gate_bits):
    """
    Insert Pauli Operator for calculate metric tensor.
    If target parametric gates type is RX, a H gates should be inserted.
    If target parametric gates type is RY, Z, S, H gates should be inserted.
    If target parametric gates type is RZ, no gate should be inserted.

    :param qubits: allocated qubits from pyqpanda qvm.
    :param target_gate_type: lists containing several layers of parametric gates type.
    :param target_gate_bits: lists containing several layers of qubits index which parametric gates act on.
    :return a pyqpanda circuit
    """

class QNG:
    '''
    Quantum Nature Gradient Optimizer, described in `Quantum Natural Gradient. <https://doi.org/10.22331/q-2020-05-25-269>`_, 2020.
    
    Optimizer with adaptive learning rate, via calculation
    of the diagonal or block-diagonal approximation to the Fubini-Study metric tensor.
    A quantum generalization of natural gradient descent.

    The QNG optimizer uses a step- and parameter-dependent learning rate,
    with the learning rate dependent on the pseudo-inverse
    of the Fubini-Study metric tensor :math:`g`:

    .. math::
        x^{(t+1)} = x^{(t)} - \\eta g(f(x^{(t)}))^{-1} \\nabla f(x^{(t)}),

    where :math:`f(x^{(t)}) = \\langle 0 | U(x^{(t)})^\\dagger \\hat{B} U(x^{(t)}) | 0 \\rangle`
    is an expectation value of some observable measured on the variational
    quantum circuit :math:`U(x^{(t)})`.

    Consider a quantum node represented by the variational quantum circuit

    .. math::

        U(\\mathbf{\\theta}) = W(\\theta_{i+1}, \\dots, \\theta_{N})X(\\theta_{i})
        V(\\theta_1, \\dots, \\theta_{i-1}),

    For each parametric layer :math:`\\ell` in the variational quantum circuit
    containing :math:`n` parameters, the :math:`n\\times n` block-diagonal submatrix
    of the Fubini-Study tensor :math:`g_{ij}^{(\\ell)}` is calculated directly on the
    quantum device in a single evaluation:

    .. math::

        g_{ij}^{(\\ell)} = \\langle \\psi_\\ell | K_i K_j | \\psi_\\ell \\rangle
        - \\langle \\psi_\\ell | K_i | \\psi_\\ell\\rangle
        \\langle \\psi_\\ell |K_j | \\psi_\\ell\\rangle

    where :math:`|\\psi_\\ell\\rangle =  V(\\theta_1, \\dots, \\theta_{i-1})|0\\rangle`
    (that is, :math:`|\\psi_\\ell\\rangle` is the quantum state prior to the application
    of parameterized layer :math:`\\ell`).

    .. note::

        Only Support VQC contains RX, RY, RZ.

        Only Support pure variational quantum circuit.

        Need to calculate metric tensor for each variational parameters .

    :param config: config for pyqpanda init config contains qubits,machine,etc..
    :param circuit_func: target variational quantum circuit.
    :param target_gate_type_lists: target parametric gates type. Several gates are in same layer should be in same list.
    :param target_gate_bits_lists: target parametric gates act on qubit index.
    :param wires: target variational quantum circuit qubits index.
    :return a Quantum Nature Gradient Optimizer instance.
    
    Example::


        def layer0_subcircuit(config: pyqpanda_config_wrapper, params):
            qcir = pq.QCircuit()
            qcir.insert(pq.RY(config._qubits[0], np.pi / 4))
            qcir.insert(pq.RY(config._qubits[1], np.pi / 3))
            return qcir

        def get_p01_diagonal_(config, params, target_gate_type, target_gate_bits,
                            wires):
            qcir = layer0_subcircuit(config, params)
            qcir2 = insert_pauli_for_mt(config._qubits, target_gate_type,
                                        target_gate_bits)
            qcir3 = pq.QCircuit()
            qcir3.insert(qcir)
            qcir3.insert(qcir2)
            m_prog = pq.QProg()
            m_prog.insert(qcir3)
            return ProbsMeasure(wires, m_prog, config._machine, config._qubits)

        def layer1_subcircuit(config: pyqpanda_config_wrapper, params):
            qcir = pq.QCircuit()
            qcir.insert(pq.RY(config._qubits[0], np.pi / 4))
            qcir.insert(pq.RY(config._qubits[1], np.pi / 3))
            qcir.insert(pq.RY(config._qubits[2], np.pi / 7))

            qcir.insert(pq.RZ(config._qubits[0], params[0]))
            qcir.insert(pq.RY(config._qubits[1], params[1]))

            qcir.insert(pq.CNOT(config._qubits[0], config._qubits[1]))
            qcir.insert(pq.CNOT(config._qubits[1], config._qubits[2]))

            return qcir
        def get_p1_diagonal_(config, params, target_gate_type, target_gate_bits,
                            wires):
            qcir = layer1_subcircuit(config, params)
            qcir2 = insert_pauli_for_mt(config._qubits, target_gate_type,
                                        target_gate_bits)
            qcir3 = pq.QCircuit()
            qcir3.insert(qcir)
            qcir3.insert(qcir2)
            m_prog = pq.QProg()
            m_prog.insert(qcir3)

            return ProbsMeasure(wires, m_prog, config._machine, config._qubits)


        # calculate metric tensor
        config = pyqpanda_config_wrapper(3)
        qcir = []
        qcir.append(get_p01_diagonal_)
        qcir.append(get_p1_diagonal_)
        params2 = QTensor([0.432, 0.543, 0.233])

        config = pyqpanda_config_wrapper(3)

        # use quantum nature gradient optimzer to optimize circuit quantum_net
        steps = 200

        def quantum_net(
                q_input_features,
                params,
                qubits,
                cubits,
                machine):
            qcir = pq.QCircuit()
            qcir.insert(pq.RY(qubits[0], np.pi / 4))
            qcir.insert(pq.RY(qubits[1], np.pi / 3))
            qcir.insert(pq.RY(qubits[2], np.pi / 7))

            qcir.insert(pq.RZ(qubits[0], params[0]))
            qcir.insert(pq.RY(qubits[1], params[1]))

            qcir.insert(pq.CNOT(qubits[0], qubits[1]))
            qcir.insert(pq.CNOT(qubits[1], qubits[2]))
            qcir.insert(pq.RX(qubits[2], params[2]))

            qcir.insert(pq.CNOT(qubits[0], qubits[1]))
            qcir.insert(pq.CNOT(qubits[1], qubits[2]))
            m_prog = pq.QProg()
            m_prog.insert(qcir)

            return expval(machine, m_prog, {\'Y0\': 1}, qubits)

        # define QNG optimzer
        opt = QNG(config, quantum_net, 0.02, [[\'RZ\', \'RY\'], [\'RX\']], [[0, 1], [2]],
                qcir, [0, 1, 2])
        qng_cost = []
        theta2 = QTensor([0.432, 0.543, 0.233])

        # iteration
        for _ in range(steps):
            theta2 = opt.step(None, theta2)

            qng_cost.append(
                quantum_net(None, theta2, config._qubits, config._cubits,
                            config._machine))

        # use gradient descent as the baseline
        sgd_cost = []
        qlayer = QuantumLayer(quantum_net, 3, \'cpu\', 3)

        temp = _core.Tensor([0.432, 0.543, 0.233])
        _core.vqnet.copyTensor(temp, qlayer.m_para.data)
        opti = SGD(qlayer.parameters())

        for i in range(steps):
            opti.zero_grad()
            loss = qlayer(QTensor([[1]]))
            print(f\'step {i}\')
            print(f\'q param before {qlayer.m_para}\')
            loss.backward()
            sgd_cost.append(loss.item())
            opti._step()
            print(f\'q param after{qlayer.m_para}\')
            
        plt.style.use("seaborn")
        plt.plot(qng_cost, "b", label="Quantum natural gradient descent")
        plt.plot(sgd_cost, "g", label="Vanilla gradient descent")

        plt.ylabel("Cost function value")
        plt.xlabel("Optimization steps")
        plt.legend()
        plt.show()
    '''
    stepsize: Incomplete
    def __init__(self, config, circuit_func, stepsize, target_gate_type_lists, target_gate_bits_lists, qcir_lists, wires) -> None: ...
    def step(self, x, param): ...

class Gradient_Prune_Instance:
    """
    A helper class to do gradient based prune algorithm described in `Towards 
    Efficient On-Chip Training of Quantum Neural Networks <https://openreview.net/forum?id=vKefw-zKOft>`_
    
    :param param_num: quantum param number.
    :param prune_ratio: parameter ratio which keep unchanged,default:0.5
    :param accumulation_window_size: accumulation step size of gradient,default:4.
    :param pruning_window_size: pruning step size, default:2.
    """
    param_num: Incomplete
    is_accumulation: bool
    accumulation_steps: int
    sum_abs_grad: Incomplete
    last_abs_grad: Incomplete
    mask_of_shift_parmams: Incomplete
    accumulation_window_size: Incomplete
    pruning_window_size: Incomplete
    count1: int
    count2: int
    pruning_steps: int
    sampling_ratio: Incomplete
    def __init__(self, param_num, prune_ratio: float = 0.5, accumulation_window_size: int = 4, pruning_window_size: int = 2) -> None: ...
    def step(self, cur_params) -> None:
        """
        Step function in training steps.This function should run before optimzer steps()

        :param: Modules parameters, could be list of quantum parameters of type Parameters.
        """
