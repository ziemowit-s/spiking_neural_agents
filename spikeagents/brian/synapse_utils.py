import abc

from brian2 import ms

RAND_GMAX_WEIGHT = 'rand() * gmax'


class Synapse:
    def __init__(self):
        pass

    @property
    @abc.abstractmethod
    def namespace(self) -> dict:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def on_pre(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def on_post(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def model(self):
        raise NotImplementedError()


class STDPSynapse(Synapse):
    """
    Spike-timing dependent plasticity Adapted from Song, Miller and Abbott (2000) and Song and Abbott (2001)

    ge need to be use as a gated variable on neural group side. See: GatedNeuron in neuron_utils.py
    """

    def __init__(self):
        super().__init__()
        self.gmax = .01

        self.taupre = 20 * ms
        self.taupost = self.taupre

        self.dApre = .01
        self.dApost = -self.dApre * self.taupre / self.taupost * 1.05

        self.dApost *= self.gmax
        self.dApre *= self.gmax

    @property
    def namespace(self) -> dict:
        return {
            'gmax': self.gmax,

            'taupre': self.taupre,
            'taupost': self.taupre,

            'dApre': self.dApre,
            'dApost': self.dApost,
        }

    @property
    def on_pre(self):
        return '''ge += w
            Apre += dApre
            w = clip(w + Apost, 0, gmax)'''

    @property
    def on_post(self):
        return '''Apost += dApost
             w = clip(w + Apre, 0, gmax)'''

    @property
    def model(self):
        return '''w : 1
                   dApre/dt = -Apre / taupre : 1 (event-driven)
                   dApost/dt = -Apost / taupost : 1 (event-driven)'''
