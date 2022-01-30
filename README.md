# Fift-cli

## Installation and Configuration

1. Compile `fift` and `func` from [ton](https://github.com/newton-blockchain/ton) and add them to `PATH` env or move
   to `/usr/bin`
    1. For Arch Linux we have [AUR package](https://aur.archlinux.org/packages/ton-git/) of ton
2. Clone repo and install it with pip

```
git clone git@github.com:disintar/fift-cli.git
cd fift-cli && pip install .
```

Now you can access `CLI` tool by typing in terminal `fift-cli`

### Usage example

```
fift-cli startproject wallet -n my-wallet
cd my-wallet
fift-cli deploy
```

## Contributor Guide

Interested in contributing? Feel free to create issues and pull requests.

## Features and status

| Feature                                              | Status |
|------------------------------------------------------|--------|
| Auto compile func & hot reload                       | ❌      |
| Load from hard structure `code / data / lib`         | ❌      |
| Easy bootstrap project samples `wallet, hello world` | ❌      |
| Project debugging with `runvmcode`                   | ❌      |
| Gas auto calculation for store & deploy              | ❌      |
| Auto send TON to init contract address               | ❌      |

## License

[WTFPL](https://github.com/dtf0/wtfpl) v3.1

Completely free to use.
