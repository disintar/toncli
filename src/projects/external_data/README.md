# Example of loading data from account

This is an example that shows developers that any information stored in a smart contract can be parsed. Here I take out the seqno of my wallet in testnet

Deployed by [tncli](https://github.com/disintar/tncli)



### Usage

- `tncli lc saveaccount ./build/boc/c4.boc EQB36_EfYjFYMV8p_cxSYX61bA0FZ4B65ZNN6L8INY-5gL6w` save account data
- `tncli lc saveconfig ./build/boc/config.boc` save network config
- `tncli run fift/load_c4.fif -fa "-v 5" --build` build func and run load_c4.fif
