from brian2 import *

start_scope()

tau = 10 * ms

neuron = """
dv/dt = (v_drive-v) / tau : 1 (unless refractory)
v_drive : 1
"""
N = 100
n1 = NeuronGroup(N, model=neuron, method='euler', threshold='v>1', reset='v=0', refractory=5*ms)
n1.v_drive = [1.1 if rand(1)[0] > 0.8 else 0 for i in range(N)]
n1.v = rand(N)

s1 = Synapses(n1, n1, on_pre='v_post += 0.2', delay=2*ms)
s1.connect(condition='i!=j', p=0.2)

state = StateMonitor(n1, variables='v', record=True)
spike = SpikeMonitor(n1)

for i in range(100):
    if i % 10 == 0:
        n1[:50].v += 0.5
    run(1 * ms)

figure(figsize=(12,4))
subplot(121)
plot(state.t/ms, state.v[0])

subplot(122)
plot(spike.t/ms, spike.i, '.k')
