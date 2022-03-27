## So I want to manage many smart contracts and have them all in one project

`toncli` support multiple smart contracts structure.

I'll try to explain it on `wallet` example:

## Step 1

`toncli start wallet -n multi-wallet`
`cd multi-wallet`

So, first you need to change `project.yaml`

Add `test` smart contract to file, so it'll look like this:

```
contract:
  data: fift/data.fif
  func:
    - func/code.func

test:
  data: fift/test.fif
  func:
    - func/code.func
```

About project structure you can read in `advanced/project_structure.md`.

Now we need to create `test.fif` data file:

`cp fift/data.fif fift/test.fif`

Now you can change `subwallet-id` in `fift/test.fif` e.g. it looks like this:

```
"TonUtil.fif" include
"Asm.fif" include

"build/contract.pk" load-generate-keypair // generate key pair
constant private_key  // save private to constant
constant public_key // save public to constant

<b
  0 32 u, // seqno
  1 32 u, // subwallet-id
  public_key B, // add bin public key to cell
b>
```

## Step 2

Now you can deploy both contracts: `toncli deploy`. If you want to deploy only one contract you can
use: `toncli deploy test`

## Step 3

Now you can run get method:

```
(base) tvorogme in /tmp/multi-wallet λ toncli get seqno                                           
disintar.io NFT owners today say: 🙈 🙉 🙊
INFO: 🚀 You want to interact with your contracts ['contract', 'test'] in testnet - that's grate!
INFO: 🦘 Found existing deploy-wallet [kQDl5ZpiwlFCb4Bj4sKIvU15rh9Bq2MmCQmw5FrNSPj-9YQ-] (Balance: 4.717844264💎, Is inited: True) in /home/tvorogme/.config/toncli
INFO: 👯 [contract] [kQA7sZBAxviytnMgyzXO02LSHfbOx4LB50UDfx9Ldnv1D9gt] runmethod ['seqno']
INFO: 🧐 Output: [ 0  ]
ERROR: 🧐 Can't auto parse string
INFO: 👯 [test] [kQCuGN4Varstnk0serOGa2yhBG39sY7ToG8xsxK3FhEAPAeE] runmethod ['seqno']
INFO: 🧐 Output: [ 0  ]
ERROR: 🧐 Can't auto parse string
```

Or for one contract only:

```
(base) tvorogme in /tmp/multi-wallet λ toncli get seqno --contracts test
disintar.io NFT owners today say: 🙈 🙉 🙊
INFO: 🚀 You want to interact with your contracts ['contract', 'test'] in testnet - that's grate!
INFO: 🦘 Found existing deploy-wallet [kQDl5ZpiwlFCb4Bj4sKIvU15rh9Bq2MmCQmw5FrNSPj-9YQ-] (Balance: 4.717844264💎, Is inited: True) in /home/tvorogme/.config/toncli
INFO: 👯 [test] [kQCuGN4Varstnk0serOGa2yhBG39sY7ToG8xsxK3FhEAPAeE] runmethod ['seqno']
INFO: 🧐 Output: [ 0  ]
ERROR: 🧐 Can't auto parse strin
```

