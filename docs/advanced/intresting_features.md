## Here we describe some features of toncli

0. All commands have well described `help` messages you can run any command with `-h` flag to see help
   1. `toncli -h` - as example
1. You can use `toncli f` / `toncli fift` instead of running `fift -I .../fift-libs`
2. You can use `toncli fc` / `toncli func` instead of running `func -SPA .../func-libs/stdlib.func `
3. You can use `toncli lc` / `toncli lite-client` instead of running `lite-client -C /usr/lib/testnet-global.config.json`
   1. Network configuration `--net` flag, you may want to see help message
4. You can convert string to integer `toncli tointeger TEST` to add text to your `func` files
5. You can auto build func files and then run own fift file E.g. `toncli run fift/load_c4.fif --build` in `external_data`
6. You can build all contracts in project by `toncli fc build`
7. You can pass data to stack of data.fif in your project (path is in `project.yaml`) by passing it in parameter `data-params` of `deploy` command. For example, `toncli deploy --data-params==hello_world`