## How to send BOC with fift?

Answer is - no way. But you can use `toncli` to do it for you.

For example - the basic example of wallet use `wallet.fif` to generate `boc` files, then they will be pushed to network with lite-client.

In `wallet` example you can find `fift/usage.fif` file. This is `wallet.fif` but we added one feature there. 

You can see that last line is `saveboc`. It's needed for saving `boc` file in `build/boc` location (or `/tmp` if you run command not in project root) and then our CLI tool can catch it and send to network.

E.g.:

```toncli fift sendboc ./fift/usage.fif build/contract EQB36_EfYjFYMV8p_cxSYX61bA0FZ4B65ZNN6L8INY-5gL6w 0 0 0.01```

Usage.fif takes some arguments to generate boc file, those are: file_base, wallet, subwallet_id, seqno, ammount. 

Seqno can be founded by get method `seqno`:

```
(base) tvorogme in /tmp/wallet λ toncli get seqno                                                   
disintar.io NFT owners today say: 🙈 🙉 🙊
INFO: 🚀 You want to interact with your contracts ['contract'] in testnet - that's grate!
INFO: 🦘 Found existing deploy-wallet [kQDl5ZpiwlFCb4Bj4sKIvU15rh9Bq2MmCQmw5FrNSPj-9YQ-] (Balance: 4.939916988💎, Is inited: True) in /home/tvorogme/.config/toncli
INFO: 👯 [contract] [kQA33B83t67G8nuxLvU7RrWL7kK08Uf-SVVrYvamGgwrb8Qj] runmethod ['seqno']
INFO: 🧐 Output: [ 0  ]
ERROR: 🧐 Can't auto parse string
```

Seqno is `0` in this example.

If you run `sendboc` command in `wallet` project, and pass all arguments right you will see that boc file will be sent with lite-client. 

E.g.:

```
(base) tvorogme in /tmp/wallet λ toncli fift sendboc ./fift/usage.fif build/contract EQB36_EfYjFYMV8p_cxSYX61bA0FZ4B65ZNN6L8INY-5gL6w 0 0 0.01 
disintar.io NFT owners today say: 🙈 🙉 🙊
INFO: 💾 Will save BOC to /tmp/wallet/build/boc/usage.boc
INFO: 🍿 Loading fift CLI lib
INFO: 👀 Source wallet address = kQA33B83t67G8nuxLvU7RrWL7kK08Uf-SVVrYvamGgwrb8Qj
Loading private key from file build/contract.pk
INFO: 👋 Send kQB36_EfYjFYMV8p_cxSYX61bA0FZ4B65ZNN6L8INY-5gAU6 = subwallet_id=0x0 seqno=0x0 bounce=-1 
INFO: 🧟 Body of transfer message is x{}
INFO: 🥰  Save boc
INFO: 💾 (Saved to file /tmp/wallet/build/boc/usage.boc)
using liteserver 1 with addr [135.181.73.112:7208]
zerostate set to -1:58FB12D488918D3D0C483E97BF2B38418421EEBADCF71D326F35E88F0278807D:07381F469160C8D8C723B691E4A421AB85ADAF6C0DFAC5F32DA5BEADF1EF3F90
[ 1][t 1][2022-02-08 13:05:45.104156765][lite-client.h:362][!testnode]	conn ready
[ 2][t 1][2022-02-08 13:05:45.159063692][lite-client.cpp:363][!testnode]	server version is 1.1, capabilities 7
latest masterchain block known to server is (-1,8000000000000000,8354392):7514052006FEFA8D07A93FAFB603A103205B2BA99FD7A47163A581F8B5E22D45:CE4F90D0AC6B67AC61A46E91DAF9094D3E1E8F9FA3A10F71DFB59F3B96646531 created at 1644325540 (5 seconds ago)
BLK#1 = (-1,8000000000000000,8354392):7514052006FEFA8D07A93FAFB603A103205B2BA99FD7A47163A581F8B5E22D45:CE4F90D0AC6B67AC61A46E91DAF9094D3E1E8F9FA3A10F71DFB59F3B96646531
BLK#2 = (-1,8000000000000000,0):58FB12D488918D3D0C483E97BF2B38418421EEBADCF71D326F35E88F0278807D:07381F469160C8D8C723B691E4A421AB85ADAF6C0DFAC5F32DA5BEADF1EF3F90
[ 1][t 1][2022-02-08 13:05:45.713451483][lite-client.cpp:1150][!testnode]	sending query from file /tmp/wallet/build/boc/usage.boc
```