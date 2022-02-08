## How to work with get methods of contract?

Get methods defined in smart contract code and looks like this:

```
int hello_world() method_id {
    ;; Ok now you need to add integer of your text
    ;; But soon TON Foundation will add string literals to func
    ;; And you will not need to do this
    ;; hi as integer, try toncli tointeger hi
    return 26729;
}
```

So this is method from quick start guide and you can easily get this message by running `toncli get hello_world`

But sometimes it's necessary to run custom code upon get message output. `toncli` provides interface for it. 

Let's say we have get method that returned cell:

```
(int, cell) get_hi_from_cell() method_id {
    ;; This is for example of tnlci get --fift usage
    ;; We will return cell here, and it will be loaded in our fift script
    ;; So we can do something intresting with it

    int seqno = get_data().begin_parse().preload_uint(32);

    cell test_inside = begin_cell()
                    .store_uint(26729, 64) ;; set hi to ref cell to test toncli works with refs in get methods
                    .end_cell();

    return (seqno, begin_cell()
                        .store_uint(seqno, 32)
                        .store_ref(test_inside)
                        .end_cell());
}
```

This is tricky one. It's return seqno as integer, cell with data seqno and ref to another cell with another message. How we can parse it?

In default wallet project we provide `fift/examples/parse_get_cell.fif` that looks like this:

```
"Color.fif" include
.s // prints stack

// you will see that integer and cell slice are in stack

// print seqno (it is just int in stack)
."🤗 Seqno as int from " ^green ."GET" ^reset ." method is: "

swap // get seqno as int on top of stack
(dump) // dump to string
type // print it to output
cr // print endline

<s dup 32 i@ // get seqno from cell
swap ref@ // get ref on first cell
<s 64 i@ // get message from second cell
swap // get seqno from cell to top

."🤗 Seqno as int from cell from " ^green ."GET" ^reset ." method is: " (dump) type cr

."🥳 Message from ref cell: " (dump) type cr
```

So we can run get method `get_hi_from_cell` and then parse output using this fift script: `toncli get get_hi_from_cell --fift fift/examples/parse_get_cell.fif`

Output may look like this:

```
INFO: 🚀 You want to interact with your contracts ['contract'] in testnet - that's grate!
INFO: 🦘 Found existing deploy-wallet [kQDl5ZpiwlFCb4Bj4sKIvU15rh9Bq2MmCQmw5FrNSPj-9YQ-] (Balance: 4.939916988💎, Is inited: True) in /home/tvorogme/.config/toncli
INFO: 👯 [contract] [kQA33B83t67G8nuxLvU7RrWL7kK08Uf-SVVrYvamGgwrb8Qj] runmethod ['get_hi_from_cell']
INFO: 🧐 Output: [ 0 C{BC4CA942A6A9CDD5C6CDB4AD1A6844D117E93ED49C7CBAEFEAAB6DC1A84975F3}  ]
0 C{BC4CA942A6A9CDD5C6CDB4AD1A6844D117E93ED49C7CBAEFEAAB6DC1A84975F3} 
🤗 Seqno as int from GET method is: 0
🤗 Seqno as int from cell from GET method is: 0
🥳 Message from ref cell: 26729
```