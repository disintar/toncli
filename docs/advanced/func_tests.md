## How func tests works?

Example of using func tests could be founded [here](https://github.com/disintar/func-tests-playground/blob/master/tests/example.func).

But how it works and how to run it without toncli if needed?

To compile test func code we use [this](https://github.com/disintar/toncli/blob/master/src/toncli/lib/func-libs/tests-helpers.func) mini library.

To run `run_tests.fif` we use special `AsmTests.fif` from [here](https://github.com/disintar/toncli/blob/master/src/toncli/lib/fift-libs/AsmTests.fif)

Let's start with a point where contract code and tests code successfully compiled into Fift ASM. 

Toncli gets paths to those files and paste them to `run_tests.fif` [here](https://github.com/disintar/toncli/blob/5accd1562296b25c73efcae410c76905d18176be/src/toncli/modules/fift/run_test.fif.template#L4) and [here](https://github.com/disintar/toncli/blob/5accd1562296b25c73efcae410c76905d18176be/src/toncli/modules/fift/run_test.fif.template#L8)

Also, it parse verbose level and pass it [here](https://github.com/disintar/toncli/blob/5accd1562296b25c73efcae410c76905d18176be/src/toncli/modules/fift/run_test.fif.template#L12)

`run_test.fif` parse function declaration from compiled Fift ASM and invoke running VM 3 times. 

- First time [run](https://github.com/disintar/toncli/blob/5accd1562296b25c73efcae410c76905d18176be/src/toncli/modules/fift/run_test.fif.template#L95): run [get_data](https://github.com/disintar/func-tests-playground/blob/a9810ff4c1c639fb4e9cc6541de83c6ad351b921/tests/example.func#L13) function and collect `gas-limit` / `c7` / `c4` / `stack` / `function selector`
- Second time [run](https://github.com/disintar/toncli/blob/5accd1562296b25c73efcae410c76905d18176be/src/toncli/modules/fift/run_test.fif.template#L127): run contract `code` with all needed params from step (1)
- Third time [run](https://github.com/disintar/toncli/blob/5accd1562296b25c73efcae410c76905d18176be/src/toncli/modules/fift/run_test.fif.template#L142): get `c4` / `c5` / `gas-used` / `stack` / `exit-code` params from step (2) and pass them to actual [test](https://github.com/disintar/func-tests-playground/blob/a9810ff4c1c639fb4e9cc6541de83c6ad351b921/tests/example.func#L52) 

### Hints

1. If you want to create working functions in tests code, please use `inline method_id` 
2. If you want to get `c4` / `c5` from previous tests - use `get_prev_c4` / `get_prev_c5`
3. You may use `dump_stack();` for debugging
4. You may use `-v 1` / `-v 2`  for debugging when running tests
   1. If `-v 2` is used - stack will be dumped, but it's buggy function, so do not panic if something go wrong, jus try to use `-v 1`
5. You can use special `get_prev_c4` / `get_prev_c5` functions to get `c4` / `c5` cells from prev tests