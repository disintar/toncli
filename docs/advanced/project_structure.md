### Project structure

```
.
├── build # func will compile here
│   └── boc # final boc files will store here
├── fift
│   ├── data.fif # data cell
├── func
│   ├── code.func # main func code
├── tests # all tests on smart contract goes here
└── project.yaml # project structure description
```

`project.yaml` must use this structure:

```
contract:
  data: fift/data.fif
  lib: fift/lib.fif (if needed)
  message: fift/message.fif (if needed)
  func:
    - func/code.func
    - ...

contract2:
  data: fift/contract2_data.fif
  lib: fift/contract2_lib.fif (if needed)
  message: fift/contract2_message.fif (if needed)
  func:
    - func/code.func
    - ...

...
```

1. Func take files from `func` block in contract in exec same order
2. Func must build files to `build`