import abc

from spikeagents.brian.handlers.brian_event_handler import BrianEventHandler
from brian2 import *

from spikeagents.brian.neuron_utils import Neuron
from spikeagents.brian.synapse_utils import Synapse
from spikeagents.core.agent import Agent


class BrianAgent(Agent, Network):

    def __init__(self, neuron_model: Neuron, synapse_model: Synapse, namespace: dict = None):
        Agent.__init__(self)
        Network.__init__(self)
        self.spike_monitors = {}
        self.spike_handlers = {}

        if namespace is None:
            namespace = {}
        self.namespace = namespace
        self.namespace.update(neuron_model.namespace)
        self.namespace.update(synapse_model.namespace)

        self.neuron_model = neuron_model
        self.synapse_model = synapse_model

        self.neuron_layers = []
        self.synalse_layers = []

    def build(self):
        start_scope()
        self._make_layers()
        self._make_synapses()
        self.store()

    def add_neuron_layer(self, **kwargs):
        n = NeuronGroup(**kwargs)
        self.add(n)
        self.neuron_layers.append(n)
        return n

    def add_synapse_layer(self, **kwargs):
        s = Synapses(**kwargs)
        self.add(s)
        self.synalse_layers.append(s)
        return s

    @abc.abstractmethod
    def _make_layers(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _make_synapses(self):
        raise NotImplementedError

    def init_network(self, duration=10 * ms, namespace=None):
        self._run_agent(duration, namespace=namespace)
        print('network init done')

    def _run_agent(self, duration=10 * ms, namespace=None):
        if namespace is None:
            namespace = self.namespace
        self.run(duration, namespace=namespace)

    def step(self, duration=1 * ms, observation=None, reward=None, namespace=None):
        if observation is not None:
            self.inp[:].v += observation

        self._run_agent(duration, namespace=namespace)

        self._exec_spike_handlers()

    def add_spike_handler(self, layer: NeuronGroup, handler: BrianEventHandler):
        """
        :param layer:
        :param handler:
            EventHandler object which accept "value" as param, which is dict of: dict[neuron_id] = time_of_occurence
        :return:
        """
        self.spike_handlers[layer.name] = (handler, layer)
        self._add_spike_monitor(layer)

    def _exec_spike_handlers(self):
        for name, (handler, layer) in self.spike_handlers.items():
            m = self.spike_monitors[name]

            if len(m.t[:]) > 0:  # if spike(s) occured
                handler.exec(spike_monitor=m)

                self.remove(m)
                del self.spike_monitors[layer.name]
                self._add_spike_monitor(layer)

    def _add_spike_monitor(self, layer: NeuronGroup):
        if layer.name not in self.spike_monitors:
            m = SpikeMonitor(layer)
            self.add(m)
            self.spike_monitors[layer.name] = m
