from brian2 import *

from brian.neuron_utils import GatedNeuron
from brian.synapse_utils import STDPSynapse, RAND_GMAX_WEIGHT


class NetworkSTDP:
    def __init__(self, neuron, synapse, input_size, hidden_size, output_size):

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.input = NeuronGroup(self.input_size, neuron, threshold='v>v_threshold', reset='v = v_rest', method='exact')
        self.hidden = NeuronGroup(self.hidden_size, neuron, threshold='v>v_threshold', reset='v = v_rest', method='exact')
        self.output = NeuronGroup(self.output_size, neuron, threshold='v>v_threshold', reset='v = v_rest', method='exact')

        S1 = Synapses(self.input, self.hidden, synapse.model, on_pre=synapse.on_pre, on_post=synapse.on_post)
        S1.connect()
        S1.w = RAND_GMAX_WEIGHT

        S2 = Synapses(self.hidden, self.output, synapse.model, on_pre=synapse.on_pre, on_post=synapse.on_post)
        S2.connect()
        S2.w = RAND_GMAX_WEIGHT

        self.output_spikes = SpikeMonitor(self.output)
        self.output_states = StateMonitor(self.output, variables='v', record=True)

    def run(self, duration, input=None, report='text'):
        self.input[0].v = 3 * mV
        self.input[1].v = 3 * mV

        run(duration, report=report)
        plot(self.output_states.t / ms, self.output_states.v[0] / mV, '-b')
        return self.output_spikes


if __name__ == '__main__':

    net = NetworkSTDP(neuron=GatedNeuron(),
                      synapse=STDPSynapse(),
                      input_size=2500,
                      hidden_size=100,
                      output_size=2)

    net.run(50*ms, np.ones(2500))
