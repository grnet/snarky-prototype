# snarky-ceremonies

Python implementation of [Snarky Ceremonies](https://eprint.iacr.org/2021/219.pdf).

## Prerequisites

```commandline
apt-get install build-essential libssl-dev
pip3 install -r requirements.txt
```

Assuming you have Docker, you can alternatively run the dev container and work 
in a Debian environment with preinstalled prerequisites:

```commandline
./run-dev-container --help
```

## Demo

```commandline
python3 demo.py
```

## Development

### Tests

```commandline
pip3 install -r requirements-dev.txt
```

```commandline
./test.sh
```
