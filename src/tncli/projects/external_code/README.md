# Example of loading data from account

Deployed by [tncli](https://github.com/disintar/tncli)

Based on external_data - this is example of running external code based on external data but with own arguments to
functions. For example `receive_external` in wallet v3

This example is not easy to understand, it's only for pro usage of ton features.

### Usage

1. Create and deploy wallet (`tncli start wallet && cd wallet && tncli deploy`)
2. Copy private key of wallet to build folder of this project `cp wallet/build/contract.pk build/`
3. Save contract data to this project
   1. `tncli lc saveaccountdata ./build/boc/c4.boc <smc_address>` save account data to
     boc
   2. `tncli lc saveaccountcode ./build/boc/c3.boc <smc_address>` save account code to
  boc
4. Run `recv_external` locally: `tncli run fift/load_c3_and_c4.fif`

