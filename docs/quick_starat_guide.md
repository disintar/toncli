# toncli Quick start guide
Provided by [disintar.io](https://disintar.io) team

This quide contains simple steps how-to deploy example smart contract to TON.

## 1. Install ton / toncli

Please, follow [INSTALLATION.md](/INSTALLATION.md)

## 2. Create simple project

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
8. [Send internal fift messages](/docs/advanced/send_fift_internal.md)
8. [How func tests works?](/docs/advanced/func_tests.md)
