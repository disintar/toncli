# toncli Quick start guide

This quide contains simple steps how-to deploy example smart contract to TON.

## 1. Clone repository

```
git clone --recursive https://github.com/newton-blockchain/ton
cd ton
```

## 2. Build from sources

1. Compile `fift`, `func`, `lite-client` from [ton](https://github.com/newton-blockchain/ton), official docs can be
   founded [here](https://ton.org/docs/#/howto/getting-started)
    1. For Arch Linux we have [AUR package](https://aur.archlinux.org/packages/ton-git/) of ton
    2. For Apple computers on M1 we have a guide "How to compile them from official
       repo" [M1 Guide](/docs/apple_m1_compile_fix.md)

2. Add binary files to `PATH` env variable or add them to `/usr/bin`

## 3. Install toncli package

`pip install toncli` needed `Python 3.8` or higher

## 4. Create simple project

### 1. start project

```
toncli start wallet
cd wallet
```

"wallet" is a project and folder name.

### 2. deploy example contract

```
toncli deploy -n testnet
```

It this case contract is deploying to testnet, you can switch it to mainnet if you want

### 3. Call a method of contract

To call a GET method of your contract you can use this command:
`toncli get hello_world` in the directory of your contract, where hello world is the name of a GET method

## Other types of projects
1. External data
    1. To use this function you need to run `toncli start external_data`
    2. It loads data of another smart-contract
    3. For detailed usage info you can read [Example](/src/toncli/projects/external_data/README.md)
2. External code
    1. To use this function you need to run `toncli start external_code`
    2. Using this function you can load code and data of another contract
    3. For detailed usage info you can read [Example](/src/toncli/projects/external_code/README.md)

# Other docs

1. [All commands of cli](/docs/advanced/commands.md)
2. [Run get methods](/docs/advanced/get_methods.md)
3. [Multiple contracts](/docs/advanced/multiple_contracts.md)
4. [Send boc with fift](/docs/advanced/send_boc_with_fift.md)
5. [Transaction debug](/docs/advanced/transaction_debug.md)
6. [Project structure](/docs/advanced/project_structure.md)
7. [Interesting features](/docs/advanced/intresting_features.md)
