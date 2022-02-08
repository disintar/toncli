# Simple wallet project

Deployed by [toncli](https://github.com/disintar/toncli)

### Usage

- `toncli run fift/data.fif`
- `toncli run func/code.fc`
- `toncli deploy -n tesnet -wc 0`

### Project structure

```
.
├── build # func will compile here
│   └── boc # final boc files will store here
├── fift
│   ├── data.fif # data cell
│   ├──  lib.fif # library cell (if needed)
│   ├── message.fif # message cell (if needed)
├── func
│   ├── code.fc # main func code
│   └── files.yaml # func code structure - in big projects you want define custom build orded
├── tests # all tests on smart contract goes here
└── README.md # this readme :)
```


