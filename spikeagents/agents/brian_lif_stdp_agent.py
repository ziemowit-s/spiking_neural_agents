from spikeagents.brian.brian_agent import BrianAgent
from spikeagents.brian.handlers.spike_event_handler import SpikeEventHandler
from spikeagents.brian.neuron_utils import GatedNeuron
from spikeagents.brian.synapse_utils import STDPSynapse
from spikeagents.brian.utils import plot_states
from brian2 import *


class BrianLIFAgent(BrianAgent):

    def __init__(self, neuron_model, synapse_model, input_size, output_size, namespace: dict = None):
        BrianAgent.__init__(self, neuron_model=neuron_model, synapse_model=synapse_model, namespace=namespace)
        self.input_size = input_size
        self.output_size = output_size

    def _make_layers(self):
        self.inp = NeuronGroup(self.input_size, model=self.neuron_model.model, method='linear',
                               threshold='v>v_threshold', reset='v = v_rest', namespace=self.namespace)
        self.output = NeuronGroup(self.output_size, model=self.neuron_model.model, method='linear',
                                  threshold='v>v_threshold', reset='v = v_rest', namespace=self.namespace)
        self.add(self.inp)
        self.add(self.output)

    def _make_synapses(self):
        input_output = Synapses(self.inp, self.output,
                                model=self.synapse_model.model,
                                on_pre=self.synapse_model.on_pre,
                                on_post=self.synapse_model.on_post,
                                delay=1 * ms,
                                namespace=self.namespace)
        input_output.connect(p=1.0)
        input_output.w = 'gmax'
        self.add(input_output)


if __name__ == '__main__':
    INPUT_SIZE = 13
    OUTPUT_SIZE = 1

    neuron_model = GatedNeuron()
    syn_model = STDPSynapse()
    syn_model.gmax = 1.315

    nn = BrianLIFAgent(neuron_model=neuron_model,
                       synapse_model=syn_model,
                       input_size=INPUT_SIZE,
                       output_size=OUTPUT_SIZE)
    nn.build()
    state_in = StateMonitor(nn.inp, variables='v', record=True)
    nn.add(state_in)
    state_out = StateMonitor(nn.output, variables='v', record=True)
    nn.add(state_out)

    fig, axs = plt.subplots(3, clear=True)
    fig.show()
    handler = SpikeEventHandler(ax=axs[0], output=[])
    nn.add_spike_handler(layer=nn.output, handler=handler)

    nn.init_network(duration=10 * ms)

    # Main loop
    for i in range(1000):
        observ = np.ones(INPUT_SIZE) * 100 * mV
        nn.step(duration=50 * ms, observation=observ)

        plot_states(state_in, "input states", ax=axs[1])
        plot_states(state_out, "outputs states", ax=axs[2])
        moves = handler.pop()
        plt.pause(0.1)