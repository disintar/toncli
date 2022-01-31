# Simple wallet project

Deployed by [fift-cli](https://github.com/disintar/fift-cli)

### Usage

- `fift-cli run data.fif`
- `fift-cli run func/code.fc`
- `fift-cli deploy -n tesnet -wc 0`

### Project structure

```
.
├── build # func will compile here
│   └── boc # final boc files will store here
├── data.fif # data cell
├── lib.fif # library cell (if needed)
├── message.fif # message cell (if needed)
├── func
│   ├── code.fc # main func code
│   └── files.yaml # func code structure - in big projects you want define custom build orded
└── README.md # this readme :)
```