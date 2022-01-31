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
| Auto compile func & hot reload into `build/`                  | ❌      |
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

### Deploy process (how it's actually work)

1. Check network (testnet, mainnet) configuration locally (in config user folder)
   1. If no config found - download from URL in config.ini
2. Check deploy wallet locally (in config user folder)
   1. If it's first time - simple wallet will be created in config folder
   2. Message with wallet address and tips will be displayed (user need to send some TON coin on it)
   3. If there is no TON in deploy contract - script will exit and notify user to update deployer balance
3. Will run `data.fif` / `message.fif` (if exist) / `lib.fif` (if exist)  before creating deploy message
   1. This will check all files are correct
   2. Also, you can run custom logic - for example create keys in build/
4. Will calculate address of contract and display it to user
5. Will send money from deploy wallet
6. Will deploy your contract
   1. [External message](https://gist.github.com/tvorogme/fdb174ac0740b6a52d1dbdf85f4ddc63#file-generate-fif-L113) will be created
   2. Boc will generated
   3. Will invoke sendfile in lite-client (TODO: use native python lib, not lite-client)

## License

[WTFPL](https://github.com/dtf0/wtfpl) v3.1

Completely free to use.
