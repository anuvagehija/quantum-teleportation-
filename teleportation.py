#quantum teleportation simulation 
#implement the 3 full qubit teleportation 

import numpy as np
import matplotlib.pyplot as plt 
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector, state_fidelity, random_statevector
from qiskit_aer import AerSimulator

#state prepareation -> check if the state is normalised and return it
def prepare_message_state(alpha: complex, beta: complex) -> np.ndarray:

    norm = np.sqrt(abs(alpha)**2 + abs(beta)**2)
    if norm < 1e-9:
        raise ValueError("State vector connot be zero.")
    return np.array([alpha/norm, beta/norm])

#teleportation circuit -> builds the quantum circuit that teleports Alice's qubit to Bob
#makes a 3 qubit teleportation circuit and returns quantum circuit
def build_teleportation_circuit(alpha: complex, beta: complex) -> QuantumCircuit:

    state = prepare_message_state(alpha, beta)

    q = QuantumRegister(3, 'q')
    c_alice = ClassicalRegister(2, 'alice_bits')
    c_bob = ClassicalRegister(1, 'bob_reslut')
    qc = QuantumCircuit(q, c_alice, c_bob)

    #stage 1 - initialise alice's message qubit
    qc.initialize(state, q[0])
    qc.barrier(label="init |ψ⟩")

    #stage 2 - entanglement
    qc.h(q[1])
    qc.cx(q[1],q[2])
    qc.barrier(label="entaglement")

    #stage3 - alice's bell measurement 
    qc.cx(q[0], q[1])
    qc.h(q[0])
    qc.barrier(label="alice ops")

    qc.measure(q[0], c_alice[0])
    qc.measure(q[1], c_alice[1])
    qc.barrier(label="classical comm")

    #stage 4
    with qc.if_test((c_alice[1], 1)):
        qc.x(q[2])
    with qc.if_test((c_alice[0], 1)):
        qc.z(q[2])
    qc.barrier(label="bob correction")

    qc.measure(q[2], c_bob[0])
    return qc        


# fidelity verification 
# Compare the original state Alice started with to the state Bob ends up with.
def compute_fidelity(alpha: complex, beta: complex) -> float:
    state = prepare_message_state(alpha, beta)
    q = QuantumRegister(3, 'q')
    qc = QuantumCircuit(q)

    qc.initialize(state, q[0])
    qc.h(q[1])
    qc.cx(q[1], q[2])
    qc.cx(q[0], q[1])
    qc.h(q[0])

    sv = Statevector(qc)

    amp_bob_0 = sv.data[0] 
    amp_bob_1 = sv.data[4]

    norm = np.sqrt(abs(amp_bob_0)**2 + abs(amp_bob_1)**2)
    bob_state = Statevector([amp_bob_0/ norm, amp_bob_1/norm])
    target_state = Statevector(state)

    return state_fidelity(target_state, bob_state)

#run the teleportation circuit 
def run_simulation(alpha: complex, beta: complex, shots: int = 4096) -> dict:
    
    qc = build_teleportation_circuit(alpha, beta)
    simulator = AerSimulator()
    job = simulator.run(qc, shots=shots)
    return job.result().get_counts()

#visualisation 
def draw_circuit(alpha: complex, beta: complex, save_path: str = "circuit.png"):
    """Draws and saves the teleportation circuit diagram."""
    qc = build_teleportation_circuit(alpha, beta)
    fig = qc.draw(output='mpl', style='iqp', fold=60)
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Circuit diagram saved → {save_path}")


def plot_results(counts: dict, alpha: complex, beta: complex,
                 fidelity: float, save_path: str = "results.png"):

    state = prepare_message_state(alpha, beta)
    expected_p0 = abs(state[0])**2
    expected_p1 = abs(state[1])**2

    bob_0 = bob_1 = 0
    for bitstring, count in counts.items():
        bob_bit = bitstring[0]   
        if bob_bit == '0':
            bob_0 += count
        else:
            bob_1 += count

    total = bob_0 + bob_1
    measured_p0 = bob_0 / total
    measured_p1 = bob_1 / total

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        f"Quantum Teleportation Results\n"
        f"|ψ⟩ = ({alpha:.2f})|0⟩ + ({beta:.2f})|1⟩   |   "
        f"Fidelity = {fidelity:.6f}",
        fontsize=13, fontweight='bold'
    )

    # Left: bar comparison
    ax = axes[0]
    x = np.arange(2)
    width = 0.35
    bars_exp = ax.bar(x - width/2, [expected_p0, expected_p1],
                      width, label='Expected |ψ⟩', color='steelblue', alpha=0.85)
    bars_meas = ax.bar(x + width/2, [measured_p0, measured_p1],
                       width, label="Bob's measurement", color='tomato', alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(['|0⟩', '|1⟩'], fontsize=13)
    ax.set_ylabel('Probability')
    ax.set_title("Expected vs. Measured Probabilities")
    ax.legend()
    ax.set_ylim(0, 1.1)
    for bar in bars_exp:
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.02, f'{bar.get_height():.3f}',
                ha='center', va='bottom', fontsize=9)
    for bar in bars_meas:
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.02, f'{bar.get_height():.3f}',
                ha='center', va='bottom', fontsize=9)

    # Right: fidelity gauge
    ax2 = axes[1]
    ax2.set_aspect('equal')
    theta = np.linspace(0, np.pi, 300)
    ax2.plot(np.cos(theta), np.sin(theta), 'lightgrey', lw=8)
    needle_angle = np.pi * fidelity
    ax2.annotate('', xy=(0.75 * np.cos(needle_angle), 0.75 * np.sin(needle_angle)),
                 xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='tomato', lw=3))
    ax2.text(0, -0.2, f'Fidelity\n{fidelity:.6f}',
             ha='center', va='center', fontsize=14, fontweight='bold')
    ax2.text(-1.05, -0.15, '0.0', ha='center', fontsize=10)
    ax2.text(1.05, -0.15, '1.0', ha='center', fontsize=10)
    ax2.set_xlim(-1.3, 1.3)
    ax2.set_ylim(-0.4, 1.2)
    ax2.axis('off')
    ax2.set_title("Teleportation Fidelity")

    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Results plot saved → {save_path}")

#run the entire thing
def run_teleportation(alpha: complex, beta: complex,
                      shots: int = 4096, verbose: bool = True):
    
    state = prepare_message_state(alpha, beta)
    alpha_n, beta_n = state[0], state[1]

    if verbose:
        print("=" * 55)
        print("  QUANTUM TELEPORTATION SIMULATOR")
        print("=" * 55)
        print(f"  Input state:  |ψ⟩ = ({alpha_n:.4f})|0⟩ + ({beta_n:.4f})|1⟩")
        print(f"  |α|² = {abs(alpha_n)**2:.4f}  (P(Bob measures |0⟩))")
        print(f"  |β|² = {abs(beta_n)**2:.4f}  (P(Bob measures |1⟩))")
        print("-" * 55)

    fidelity = compute_fidelity(alpha_n, beta_n)
    if verbose:
        print(f"  Statevector fidelity: {fidelity:.8f}")
        if fidelity > 0.9999:
            print("  ✓ Teleportation verified — fidelity ≈ 1.0")
        else:
            print("  ✗ Warning: fidelity below threshold")

    counts = run_simulation(alpha_n, beta_n, shots=shots)
    if verbose:
        print(f"\n  Shot simulation ({shots} shots) complete.")

    draw_circuit(alpha_n, beta_n, save_path="circuit.png")
    plot_results(counts, alpha_n, beta_n, fidelity, save_path="results.png")

    if verbose:
        print("=" * 55)

    return fidelity, counts

#example run 
if __name__ == "__main__":
    print("\n── Test 1: |+⟩ state (equal superposition) ──")
    run_teleportation(1/np.sqrt(2), 1/np.sqrt(2))

    print("\n── Test 2: Arbitrary state ──")
    run_teleportation(alpha=0.6, beta=0.8)

    print("\n── Test 3: Random state ──")
    rand = random_statevector(2)
    run_teleportation(rand.data[0], rand.data[1])