# Quantum Teleportation Simulator

A simulation of the quantum teleportation protocol using Qiskit. This project demonstrates how an arbitrary quantum state can be transferred from one qubit to another using quantum entanglement and classical communication, without physically transmitting the original qubit.

## Overview

Quantum teleportation is one of the most important protocols in quantum information science. It enables the transfer of an unknown quantum state from a sender (Alice) to a receiver (Bob) using three key resources:

* An arbitrary quantum state to be transmitted
* A shared entangled Bell pair
* Two bits of classical communication

Although the protocol is called "teleportation", no particle is physically transported. Instead, the quantum information encoded in the state is reconstructed on Bob's qubit.

## Protocol

### 1. Preparing the Message State

The protocol begins with an arbitrary single-qubit state:

```text
|ψ⟩ = α|0⟩ + β|1⟩
```

where α and β are complex amplitudes that satisfy:

```text
|α|² + |β|² = 1
```

This state represents the quantum information Alice wishes to transmit.

### 2. Creating an Entangled Bell Pair

Alice and Bob share an entangled pair of qubits prepared in the Bell state:

```text
(|00⟩ + |11⟩) / √2
```

Entanglement is the key resource that makes teleportation possible. Neither qubit individually contains useful information, but together they form a correlated quantum system.

### 3. Alice Performs a Bell Measurement

Alice combines her message qubit with her half of the Bell pair and performs a Bell-basis measurement.

After this operation, the original quantum information is no longer localized on Alice's qubit. Instead, Bob's qubit becomes related to the original state through one of four possible outcomes:

```text
|ψ⟩
X|ψ⟩
Z|ψ⟩
XZ|ψ⟩
```

The specific outcome depends on Alice's measurement result.

### 4. Classical Communication

Alice measures her two qubits and obtains two classical bits.

These bits are sent to Bob through a conventional communication channel.

The need for classical communication is important because it prevents faster-than-light transfer of information. Bob cannot recover the original state until he receives Alice's measurement results.

### 5. Bob Applies Corrections

Using the two classical bits received from Alice, Bob applies the appropriate correction operation:

| Alice's Result | Bob's Operation |
| -------------- | --------------- |
| 00             | Identity        |
| 01             | X               |
| 10             | Z               |
| 11             | XZ              |

After applying the correction, Bob's qubit becomes:

```text
|ψ⟩
```

which is identical to the original state prepared by Alice.

## Verification

To verify successful teleportation, the simulator computes the state fidelity between the original state and the recovered state.

Fidelity measures how similar two quantum states are:

```text
F = |<ψ|φ>|²
```

where:

* |ψ⟩ is the original state
* |φ⟩ is the teleported state

A fidelity of 1 indicates that the two states are identical.

The simulator also performs repeated measurements and compares Bob's observed probabilities with the theoretical probabilities predicted by the original quantum state.

## Results

The project generates:

* A complete teleportation circuit diagram
* Measurement statistics for Bob's qubit
* A comparison between expected and measured probabilities
* A fidelity visualization showing teleportation accuracy

Successful teleportation is demonstrated when Bob's measurement probabilities match the theoretical values and the fidelity approaches 1.

## Why Quantum Teleportation Does Not Violate Physics

Quantum teleportation does not enable faster-than-light communication.

Although entanglement is used to correlate Alice and Bob's qubits, Bob cannot reconstruct the state until he receives Alice's two classical bits. Since classical information is limited by the speed of light, causality is preserved.

The protocol also does not violate the no-cloning theorem. Alice's measurement destroys the original quantum state, meaning the state is transferred rather than copied.

* NumPy
* Matplotlib
