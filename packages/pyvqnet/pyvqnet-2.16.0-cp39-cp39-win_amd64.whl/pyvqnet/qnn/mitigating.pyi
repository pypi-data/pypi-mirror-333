from pyvqnet.qnn.pq_op_wrapper import PQ_1BIT_NONVQC_GATES as PQ_1BIT_NONVQC_GATES, PQ_1BIT_VQC_GATES as PQ_1BIT_VQC_GATES, PQ_2BIT_NONVQC_GATES as PQ_2BIT_NONVQC_GATES, PQ_MEASURE as PQ_MEASURE, QuantumTape as QuantumTape, QueuingManager as QueuingManager

def global_fold(q_node, scale_factors): ...
def zne_with_poly_extrapolate(q_node, scale_factors, qlists, machine, order: int = 2):
    '''
    This function implements the zero-noise extrapolation (ZNE) method with polynomial extrapolation.
    originally introduced by
    `Temme et al. <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.119.180509>`__ and
    `Li et al. <https://journals.aps.org/prx/abstract/10.1103/PhysRevX.7.021050>`__.
    It aims to lower the impact of noise when evaluating a circuit on a quantum device by
    evaluating multiple variations of the circuit and post-processing the results into a
    noise-reduced estimate. 
    The method works by assuming that the amount of noise present when a circuit is run on a
    noisy device is enumerated by a parameter :math:`\\gamma`. Suppose we have an input circuit
    that experiences an amount of noise equal to :math:`\\gamma = \\gamma_{0}` when executed.
    Ideally, we would like to evaluate the result of the circuit in the :math:`\\gamma = 0`
    noise-free setting.

    To do this, we create a family of equivalent circuits whose ideal noise-free value is the
    same as our input circuit. However, when run on a noisy device, each circuit experiences
    a noise equal to :math:`\\gamma = s \\gamma_{0}` for some scale factor :math:`s`. By
    evaluating the noisy outputs of each circuit, we can extrapolate to :math:`s=0` to estimate
    the result of running a noise-free circuit.

    :param q_node: a function with qnode python decorators , see exmaples below.
    :param scale_factors: the range of noise scale factors used.
    :param qlists: qlist used to estimate the noisy circuit.
    :param machine: NoisyQVM used to run the circuit.
    :param order: order of polynomial extrapolation used.

    :return:
            estimated result

    Exmaples::

        import pyqpanda as pq
        import numpy as np
        from pyvqnet.qnn.pq_op_wrapper import qnode

        from pyvqnet.utils.utils import default_noise_config
        import pyvqnet.qnn.pq_op_wrapper as pq_wrap

        machine = pq.CPUQVM()
        machine.init_qvm()
        qlists = machine.qAlloc_many(1)
        import pyvqnet.qnn.pq_op_wrapper as pq_wrap

        from pyvqnet.qnn import zne_with_poly_extrapolate

        ##########################################################

        ###########################
        shots = 1000
        @qnode()
        def cir_org(x, qlists, machine):
            cir = pq.QCircuit()
            cir.insert(pq_wrap.RY()(qlists, 0, x))
            cir.insert(pq_wrap.RX()(qlists, 0, x))
            cir.insert(pq_wrap.RZ()(qlists, 0, x))

            prog = pq.QProg()
            prog.insert(cir)
            
            result = pq_wrap.QuantumMeasure()([0], prog, machine, qlists, shots)
            counts = np.array(result)

            probabilities = counts / shots
            # Get state expectation
            result = probabilities[1] - probabilities[0]

            return result


        y = cir_org(0.5, qlists, machine)
        print("ideal")
        print(y)

        machine = pq.NoiseQVM()
        machine.init_qvm()
        qlists = machine.qAlloc_many(1)
        default_noise_config(machine, qlists)


        @qnode()
        def cir_noise(x, qlists, machine):
            cir = pq.QCircuit()
            cir.insert(pq_wrap.RY()(qlists, 0, x))
            cir.insert(pq_wrap.RX()(qlists, 0, x))
            cir.insert(pq_wrap.RZ()(qlists, 0, x))

            prog = pq.QProg()
            prog.insert(cir)

            result = pq_wrap.QuantumMeasure()([0], prog, machine, qlists, shots)
            counts = np.array(result)

            # Compute probabilities for each state
            probabilities = counts / shots
            # Get state expectation
            result = probabilities[1] - probabilities[0]
            return result

        print("noise")
        print(cir_noise(0.5, qlists, machine))
        result = zne_with_poly_extrapolate(
            cir_org,
            [1, 2, 3, 4, 5, 6],qlists,machine,
            2,
        )
        print(result)


    '''
def poly_extrapolate(x, y, order): ...
