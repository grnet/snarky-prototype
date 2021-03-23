# snarky-ceremonies

Python implementation of [Snarky Ceremonies](https://eprint.iacr.org/2021/219.pdf).

## Prerequisites

```commandline
apt-get install build-essential libssl-dev
pip3 install -r requirements.txt
```

Assuming you have Docker, you can alternatively run the dev container and work 
in a Debian environment with preinstalled prerequisites, where you can run
both demo and tests.

```commandline
./run-dev-container --help
```

## Demo

```commandline
python3 demo.py [--help]
```

## Installation

## Usage

```python
from snarky_ceremonies import create_context, \
	generate_trapdoor, QAP, setup, update, verify

# Specify context
ctx = create_context()					# p, G, H, pairing
trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)		# (α, β, δ, x) = (1, 1, 1, 1)
m, n, l = 50, 40, 30					# Specify QAP dimensions
qap = QAP.create_default(ctx, m, n, l)			# Initialize with constant polynomials

# Setup stage (SRS generation)
srs, trapdoor = setup(ctx, trapdoor, qap)

# Bunch of proofs
Q = [[], []]

# Phase 1 updates

srs, rho = update(ctx, qap, 1, srs, Q)
Q[0].append(rho)

...

# Phase 2 updates

srs, rho = update(ctx, qap, 2, srs, Q)
Q[1].append(rho)

...

# Verification stage
assert verify(ctx, qap, srs)
```

## Development

### Tests

```commandline
pip3 install -r requirements-dev.txt
```

```commandline
./test.sh
```
