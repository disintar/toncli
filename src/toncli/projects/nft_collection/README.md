# NFT Collection example project

This project allows you to:

1. Build basic nft collection contract
2. Aims to *hopefully* test any nftcollection contract for compliance with[NFT Standard](https://github.com/ton-blockchain/TIPs/issues/62)
3. Deploy collection contract via `toncli deploy`
4. Manually deploy NFT item to the collection

## Building

  Just run `toncli build`
  Depending on your fift/func build you may want
  to uncomment some of the *func/helpers*

## Testing

  Same here `toncli run_test`  
  
## Deploying collection contract

  This projec consists of two sub-projects **nft_item** and **nft_collection**
  You can see that in the *project.yml*
  **BOTH** of those have to be built.
  However it makes sense to deploy only *nft_collection*.  
  Prior to deployment you need to check out *fift/collection-data.fif*
  and change all mock configuration values like collection_content,
  owner_address Etc.  
  There is nothing special in deploy command:
  `toncli deploy -n testnet nft_collection`.  
  
## Deploying individual items

  To deploy your own NFT item to the already deployed collection
  you will need:  
  
-   Configure *fift/deploy.fif* script with your own values:
[Take a look](https://github.com/ton-blockchain/TIPs/issues/64)  

-   Get address of previously deployed collection 

-   Make yourself familiar with process of sending
[internal messages from toncli](https://github.com/disintar/toncli/blob/master/docs/advanced/send_fift_internal.md) 

`toncli send -n testnet -a 0.05 --address 
"kQAaHefuZCu6inUqWYSd2YGUt7qW6ssqt__Y0VFS2AdLEAF5"  --body fift/deploy.fif`  
Every next item deployment you should make sure to
change item index in the *fift/deploy.fif* file ( Yes. Manually for now ).
