# NFT Item example project

This project allows you to:

1.  Build basic nft item contract
2.  Aims to *hopefully* test any nft item contract for compliance with[NFT Standard](https://github.com/ton-blockchain/TIPs/issues/62)
3.  Deploy collection-less nft item contract via `toncli deploy`

## Building

  Just run `toncli build`
  Depending on your fift/func build you may want
  to uncomment some of the *func/helpers*

## Testing

  Same here `toncli run_test` 
  If you encounter **error 6** during *run_tests*
  make shure that your binaries are built according to:
  [this manual](https://github.com/disintar/toncli/blob/master/docs/advanced/func_tests_new.md)


  
## Deploying item contract

  To deploy collection-less nft you should edit
  "fift/nft-data.fif.  
  This project is aimed mostly at testing and development of your own
  nft item contrat to be then used with *nft_collection*.  

  However, deploying collection-less NFT is still posslibe.

-   Set *coll_raw* address to *addr_none*.
  `0 2 u,` instead of `coll_raw Addr,` would be the
  simpest way to do it.  

-   Set *nft_json* to the full url pointing to your item metadata json

  If you aim to deploy item within collection please *use nft_collection project*

  There is nothing special in deploy command:
  `toncli deploy -n testnet nft_item`.  
  
