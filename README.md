# snarky-ceremonies

Python implementation of [Snarky Ceremonies](https://eprint.iacr.org/2021/219.pdf).

## Prerequisites

```commandline
apt-get install build-essential libssl-dev
pip3 install -r requirements.txt
```

Assuming you have Docker, you can alternatively enter the provided container and
work in a Debian environment with preinstalled prerequisites.

```commandline
./run-container.sh
```

## Demo

```commandline
$ python3 demo.py
$ python3 demo.py --m=7 --n=4 --l=6 --phases 30 20
$ python3 demo.py --help
```

## Installation

## Usage

```python
from snarky_ceremonies import create_context, \
	generate_trapdoor, QAP, setup, update, verify

ctx = create_context()					# p, G, H, pairing
trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)		# (α, β, δ, x) = (1, 1, 1, 1)
m, n, l = 50, 40, 30					# Specify QAP dimensions
qap = QAP.create_default(ctx, m, n, l)			# Initialize with constant polynomials

srs, trapdoor = setup(ctx, trapdoor, qap)		# Setup (SRS initialization)
Q = [[], []]						# Bunch of proofs

srs, rho = update(ctx, qap, 1, srs)			# Phase 1 update
Q[0].append(rho)

srs, rho = update(ctx, qap, 2, srs)			# Phase 2 update
Q[1].append(rho)

assert verify(ctx, qap, srs)				# Verification
```

## Development

```commandline
pip3 install -r requirements-dev.txt
```

You can alternatively work in the provided Debian container with all prerequisites
preinstalled.

```
./run-container.sh [--help]
```

### Tests

```commandline
./test.sh
```

### Benchmarks

```commandline
./benchmark.sh
```
