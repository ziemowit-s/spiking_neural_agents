from brian2 import *

MODEL = '''w : 1
           dApre/dt = -Apre / taupre : 1 (event-driven)
           dApost/dt = -Apost / taupost : 1 (event-driven)'''

ON_PRE = '''ge += w
            Apre += dApre
            w = clip(w + Apost, 0, gmax)'''
ON_POST = '''Apost += dApost
             w = clip(w + Apre, 0, gmax)'''

WEIGHT = 'rand() * gmax'

NEURON_EQUATION = '''
        dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
        dge/dt = -ge / taue : 1
        '''


class NetworkSTDP:
    def __init__(self, input_size, hidden_size, output_size):

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        N = 1000
        taum = 10 * ms
        taupre = 20 * ms
        taupost = taupre
        Ee = 0 * mV
        vt = -54 * mV
        vr = -60 * mV
        El = -74 * mV
        taue = 5 * ms
        F = 15 * Hz
        gmax = .01
        dApre = .01
        dApost = -dApre * taupre / taupost * 1.05
        dApost *= gmax
        dApre *= gmax

        self.input = NeuronGroup(2, NEURON_EQUATION, threshold='v>vt', reset='v = vr', method='exact')
        self.hidden = NeuronGroup(self.hidden_size, NEURON_EQUATION, threshold='v>vt', reset='v = vr', method='exact')
        self.output = NeuronGroup(self.output_size, NEURON_EQUATION, threshold='v>vt', reset='v = vr', method='exact')

        S1 = Synapses(self.input, self.hidden, MODEL, on_pre=ON_PRE, on_post=ON_POST)
        S1.connect()
        S1.w = WEIGHT

        S2 = Synapses(self.hidden, self.output, MODEL, on_pre=ON_PRE, on_post=ON_POST)
        S2.connect()
        S2.w = WEIGHT

        self.output_spikes = SpikeMonitor(self.output)
        self.output_states = StateMonitor(self.input, variables='v', record=True)

    def run(self, duration, input=None, report='text'):
        self.input[0].v = 3 * mV
        self.input[1].v = 3 * mV
        if input is not None:
            print('a')
        run(duration, report=report)

        plot(self.output_states.t / ms, self.output_states.v[0] / mV, '-b')

        return self.output_spikes


if __name__ == '__main__':
    net = NetworkSTDP(input_size=2500, hidden_size=100, output_size=2)
    net.run(50*ms, np.ones(2500))