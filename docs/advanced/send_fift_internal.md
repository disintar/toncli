## Internal messages

If you develop smart contract - you may see that most of the actions are internal, so toncli provide easy way to send internal messages from your toncli deployment wallet:

1. Create simple Internal message (in my example i'll use NFT transfer method)

```
"TonUtil.fif" include
"Asm.fif" include

"EQCsCSLisPZ6xUtkgi_Tn5c-kipelVHRCxGdPu9x1gaVTfVC" false parse-load-address drop .s 2=: new_owner // parse new owner
"EQCsCSLisPZ6xUtkgi_Tn5c-kipelVHRCxGdPu9x1gaVTfVC" false parse-load-address drop .s 2=: response_destination // parse response distanation

<b
  x{5fcc3d14} s, // op code
  0 64 u, // query id
  new_owner Addr, // new owner
  response_destination Addr, // notification distanation
  b{0} s, // payload
  10 16 u, // forward_amount
b>
```

2. Run `send` command

```
toncli send -n mainnet -a 0.03 --address "0:6f8cfe3953348974eb6980b3541003ecd17781d70386156c8741df0ee8f43805" --body ./fift/usage/transfer.fif
```

Also you may use `--contract` / `-c` selector and pass contract name from `project.yaml` instead of `--address`

`-a` / `--ammount` here is how much TON coins need to send