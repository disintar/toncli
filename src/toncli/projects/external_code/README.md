# Example of loading data from account

Deployed by [toncli](https://github.com/disintar/toncli)

Based on external_data - this is example of running external code based on external data but with own arguments to
functions. For example `receive_external` in wallet v3

This example is not easy to understand, it's only for pro usage of ton features.

### Usage

1. Create and deploy wallet (`toncli start wallet && cd wallet && toncli deploy`)
2. Copy private key of wallet to build folder of this project `cp wallet/build/contract.pk build/`
3. Save contract data to this project
   1. `toncli lc saveaccountdata ./build/boc/c4.boc <smc_address>` save account data to
     boc
   2. `toncli lc saveaccountcode ./build/boc/c3.boc <smc_address>` save account code to
  boc
4. Run `recv_external` locally: `toncli run fift/load_c3_and_c4.fif`

