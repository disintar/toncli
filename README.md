# Fift-cli

## Installation and Configuration

1. Compile `fift`, `func`, `lite-client` from [ton](https://github.com/newton-blockchain/ton) and add them to `PATH` env
   or move to `/usr/bin`, docs can be founded [here](https://ton.org/docs/#/howto/getting-started)
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

| Feature                                                       | Status |
|---------------------------------------------------------------|--------|
| Custom definition of `fift` / `func` / `lite-server` bin path | ✅      |
| Easy bootstrap project samples `wallet`                       | ❌      |
| ... `hello world`                                             | ❌      |
| Auto compile func & hot reload into `/tmp`                    | ❌      |
| Auto send TON to init contract address                        | ❌      |
| Deploy to mainnet / testnet                                   | ❌      |
| Run get methods of contract                                   | ❌      |
| Send messages with comment and TON to deployed contract       | ❌      |
| Gas auto calculation for store & deploy                       | ❌      |
| Load from hard structure `code / data / lib / message`        | ❌      |
| Project debugging with `runvmcode`                            | ❌      |
| Library support                                               | ❌      |

### Configuration

Config folder will create on first deploy, all fift / func libs will copy to it, also deploy wallet contract will be
created

## License

[WTFPL](https://github.com/dtf0/wtfpl) v3.1

Completely free to use.
