import abc

from brian2 import ms, mV, Hz


class Neuron:
    @property
    @abc.abstractmethod
    def model(self):
        raise NotImplementedError()


class LIFNeuron(Neuron):
    @property
    def model(self):
        return 'dv/dt = -v/tau: volt'


class LIFWithStochasticCurrentNeuron(Neuron):
    @property
    def model(self):
        return 'dv/dt = -v/tau + sigma*sqrt(2/tau)*xi : volt'


class GatedNeuron(Neuron):
    def __init__(self):
        taum = 10 * ms
        taue = 5 * ms

        Ee = 0 * mV
        v_threshold = -54 * mV
        v_rest = -60 * mV
        El = -74 * mV

        F = 15 * Hz

    @property
    def model(self):
        return '''
            dv/dt = (ge * (Ee-v_rest) + El - v) / taum : volt
            dge/dt = -ge / taue : 1
            '''