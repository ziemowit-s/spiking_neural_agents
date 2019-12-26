# Prerequisites

* Install requirements.txt
* Install NEURON from the instruction: https://github.com/ziemowit-s/neuron_netpyne_get_started

# Test

## Brian2

```python
import brian2
brian2.test()
```

## NEURON

```python
from neuron import h, gui
import matplotlib.pyplot as plt

soma = h.Section(name='soma')
soma.L = 20
soma.diam = 20
soma.insert('hh')

iclamp = h.IClamp(soma(0.5))
iclamp.delay = 10
iclamp.dur = 1
iclamp.amp = 0.9

v = h.Vector().record(soma(0.5)._ref_v) # Membrane potential vector
t = h.Vector().record(h._ref_t) # Time stamp vector

h.finitialize(-65)
h.continuerun(40)

plt.plot(t, v)
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.show()
```