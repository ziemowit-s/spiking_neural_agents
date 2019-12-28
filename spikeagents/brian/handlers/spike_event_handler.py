from spikeagents.brian.handlers.brian_event_handler import BrianEventHandler

from spikeagents.brian.utils import plot_spikes


class SpikeEventHandler(BrianEventHandler):

    def exec(self, *args, **kwargs):
        spike_monitor = kwargs['spike_monitor']
        spike_number = list(spike_monitor.count)[0]
        print('spike:', spike_number)
        self.output = spike_monitor.i

        if 'ax' in self.__dict__:
            plot_spikes(spike_monitor, "output spikes", ax=self.ax)

    def pop(self):
        result = self.output
        self.output = []
        return result
