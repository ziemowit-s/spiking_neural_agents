from brian2 import *


def plot_spikes(monitor, title=None, ax=None):
    if title:
        ax.set_title(title)

    ax.plot(monitor.t / ms, monitor.i, '.k')
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("spike")


def plot_states(monitor, title=None, ax=None):
    if title:
        ax.set_title(title)

    for i, v in enumerate(monitor.v):
        ax.plot(monitor.t / ms, v/mV)
        ax.set_xlabel("time (ms)")
        ax.set_ylabel("voltage (mV)")
