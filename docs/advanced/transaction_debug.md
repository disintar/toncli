## How to debug transactions with toncli?

Sometimes when you send your message to network - it's not working like you planned. So what you can do?

First of all - you need to find out 3 constants. Lt (logical_time), transaction hash and smart contract address in which
you send this transaction. Those constants could be found in any ton scaner.

Tncli provides ease to use command:

`!WARNING!` Before running this command you should run `toncli deploy...` once to create wallet config.

`usage: toncli run_transaction [-h] [--net {testnet,mainnet}] [--function FUNCTION] [--save SAVE] logical_time transaction_hash smc_address
`

`--function` is by default `-1` it's runvm function selector, if your transaction is internal you need to use `0`

e.g.

```
(base) tvorogme in ~ λ toncli run_transaction 8705051000001 0EcnuZxjp5EWxRrOH7IG2nXdXT1UD5Ef+F+4fxhMz/M= EQB36_EfYjFYMV8p_cxSYX61bA0FZ4B65ZNN6L8INY-5gL6w
disintar.io NFT owners today say: 🙈 🙉 🙊
execute SETCP 0
execute DUP
execute IFNOTRET
execute DUP
execute PUSHINT 85143
execute EQUAL
execute OVER
execute PUSHINT 78748
execute EQUAL
execute OR
execute PUSHCONT x71B0ED44D0D31FD31F31D70BFFE304
execute IFJMP
execute INC
execute THROWIF 32
execute PUSHPOW2 9
execute LDSLICEX
execute DUP
execute LDU 32
execute LDU 32
execute LDU 32
execute NOW
execute XCHG s1,s3
execute LEQ
execute THROWIF 35
execute PUSH c4
execute CTOS
execute LDU 32
execute LDU 32
execute LDU 256
execute ENDS
execute XCPU s3,s2
execute EQUAL
execute THROWIFNOT 33
execute XCPU s4,s4
execute EQUAL
execute THROWIFNOT 34
execute XCHG s4
execute HASHSU
execute XC2PU s0,s5,s5
execute CHKSIGNU
execute THROWIFNOT 35
execute ACCEPT
changing gas limit to 9223372036854775807
execute PUSHCONT x20D74A
execute PUSHCONT xD307D402FB00
execute WHILE
execute DUP
execute SREFS
execute implicit RET
while loop condition end
execute LDU 8
execute LDREF
execute XCHG s2
execute SENDRAWMSG
installing an output action
execute implicit RET
while loop body end
execute DUP
execute SREFS
execute implicit RET
while loop condition end
while loop terminated
execute ENDS
execute SWAP
execute INC
execute NEWC
execute STU 32
execute STU 32
execute STU 256
execute ENDC
execute POP c4
execute implicit RET
[ 3][t 0][2022-02-08 12:47:32.264377027][vm.cpp:558]	steps: 66 gas: used=2994, max=9223372036854775807, limit=9223372036854775807, credit=0
124711402 0 C{5BAFD857675E049DC1CE4F726A4116A04FD6F16A2F8D86EC0E54316D5CC004B4} 
```

This command creates locally configurated VM on time of transaction was made. It's quite easy to get errors from it. As
you see all TVM operations are printed and you can see stack (it's quite needed for transaction debuging).

Also if you want to change `runvm` parameters on your own you can save generated fif file by `--save location` flag:

`toncli run_transaction 8705051000001 0EcnuZxjp5EWxRrOH7IG2nXdXT1UD5Ef+F+4fxhMz/M= EQB36_EfYjFYMV8p_cxSYX61bA0FZ4B65ZNN6L8INY-5gL6w --save test.fif`

Then run `test.fif` by `toncli f run ./test.fif`