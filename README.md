# snarky-ceremonies

Python implementation of [Snarky Ceremonies](https://eprint.iacr.org/2021/219.pdf).

## Prerequisites

```commandline
apt-get install build-essential libssl-dev
pip3 install -r requirements.txt
```

**Note**: [`bplib`](https://github.com/gdanezis/bplib) is used, which builds upon 
[`openssl`](https://github.com/openssl/openssl).

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
