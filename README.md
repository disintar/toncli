<p align="center">
   <a href="https://disintar.io/">
       <img
        src="https://raw.githubusercontent.com/disintar/toncli/master/docs/images/logo.png"
        alt="Superset"
        height="150"
      />
   </a>
</p>

# toncli

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/toncli.svg)](https://github.com/disintar/toncli)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8f4acbbba3a743f992062c377c48c675)](https://www.codacy.com/gh/disintar/toncli/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=disintar/toncli&amp;utm_campaign=Badge_Grade)
[![TON](https://img.shields.io/badge/%F0%9F%92%8E-TON-green)](https://ton.org)

The Open Network cross-platform smart contract command line interface.

Easy to deploy and interact with TON smart contracts.

## 🔧 Installation

Toncli support Windows / macOS (m1 / intel) / Linux / Docker, installation guide can be
found: [INSTALLATION.md](/INSTALLATION.md)

### 📚 Usage and docs

New to `toncli`?

Try: [Quick start guide](/docs/quick_start_guide.md)

All other documentation lists in `docs/`

### Lessons

[🇬🇧 Ton FunC lessons Eng](https://github.com/romanovichim/TonFunClessons_Eng)

[🇷🇺 Ton FunC lessons Rus](https://github.com/romanovichim/TonFunClessons_ru/)


## Contributor Guide

Interested in contributing? Feel free to create issues and pull requests.

We are trying to process all tasks through issues. You can take own one 🥳

## Features and status

| Feature                                                                                                   | Status |
|-----------------------------------------------------------------------------------------------------------|-------|
| `fift` / `func` / `lite-server` usage                                                                     | ✅     |
| Easy bootstrap project samples `wallet`                                                                   | ✅     |
| Deploy-wallet for auto send TON to contracts and tests                                                    | ✅     |
| Compile func to `build/` from `func/` with `files.yaml`                                                   | ✅     |
| Auto send TON to init contract address                                                                    | ✅     |
| Deploy to mainnet / testnet / ownnet                                                                      | ✅     |
| Project interact after deploy: easily send messages, run getmethods, run fift parsers on getmethods output | ✅     |
| Load from hard project structure (example: `src/projects/wallet`)                                         | ✅     |
| Run remote contracts locally (get cells from chain and run locally to get error / debug / etc.)           | ✅     |
| Get contract address by `toncli addrs`                                                                    | ✅     |
| Docs for contract creation for beginners                                                                  | ✅     |
| Project tests with `runvmcode`                                                                            | ✅     |
| Windows & Linux support                                                                                   | ✅     |
| Unit tests engine                                                                                         | ✅     |
| Add more project samples with advanced usage                                                              | ✅      |

## Commands

[List of all commands](/docs/advanced/commands.md)

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
3. Will run tests on `fift/data.fif` / `fift/message.fif` (if exist) / `fift/lib.fif` (if exist)  before creating deploy
   message
    1. This will check all files are correct
    2. Also, you can run custom logic - for example create keys in build/
4. Will calculate address of contract and display it to user
5. Will send money from deploy wallet
6. Will deploy your contract
    1. [External message](https://gist.github.com/tvorogme/fdb174ac0740b6a52d1dbdf85f4ddc63#file-generate-fif-L113) will
       be created
    2. Boc will generated
    3. Will invoke sendfile in lite-client (TODO: use native python lib, not lite-client)

## Development

```
git clone git@github.com:disintar/toncli.git
cd toncli && pip install -e .
```

If you wish to update toncli locally you can use ```pip install -e path/to/toncli/rootfolder/```
command anytime after you make changes to the toncli source code.

## Version migration

#### 0.24

Please, use `toncli update_libs`

#### 0.22

The easy migration method - remove `fift-libs`, `func-libs` from `~/.config/toncli` or delete whole
directory `~/.config/toncli`

## Help and questions

Feel free to ask questions and help in official telegram chats: [Russian](https://t.me/tondev)
/ [English](https://t.me/tondev_eng)
