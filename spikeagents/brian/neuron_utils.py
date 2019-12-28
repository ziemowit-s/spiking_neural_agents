import abc

from brian2 import ms, mV, Hz


class Neuron:

    @property
    @abc.abstractmethod
    def threshold(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def reset(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def namespace(self) -> dict:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def model(self):
        raise NotImplementedError()


class LIFNeuron(Neuron):
    @property
    def threshold(self):
        return 'v>1'

    @property
    def reset(self):
        return 'v = 0'

    @property
    def namespace(self) -> dict:
        return {}

    @property
    def model(self):
        return 'dv/dt = -v/tau: volt'


class LIFWithStochasticCurrentNeuron(Neuron):
    @property
    def threshold(self):
        return 'v>1'

    @property
    def reset(self):
        return 'v = 0'

    @property
    def namespace(self) -> dict:
        return {}

    @property
    def model(self):
        return 'dv/dt = -v/tau + sigma*sqrt(2/tau)*xi : volt'


class GatedNeuron(Neuron):
    """
    Spike-timing dependent plasticity Adapted from Song, Miller and Abbott (2000) and Song and Abbott (2001)

    ge is a gated variable which is set on synapse side. See: STDPSynapse in synapse_utils.py
    """

    @property
    def threshold(self):
        return 'v>v_threshold'

    @property
    def reset(self):
        return 'v = v_rest'

    @property
    def namespace(self) -> dict:
        return {
            'taum': 10 * ms,
            'taue': 5 * ms,

            'Ee': 0 * mV,
            'v_threshold': -54 * mV,
            'v_rest': -60 * mV,
            'El': -74 * mV,

            'F': 15 * Hz,
        }

    @property
    def model(self):
        return '''
            dv/dt = (ge * (Ee-v_rest) + El - v) / taum : volt
            dge/dt = -ge / taue : 1
            '''

