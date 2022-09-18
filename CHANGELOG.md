## Change Log

### 0.0.4

Most work was supported by Ton Foundation and done by contributors, thanks.

- [x] Massive refactoring, special thanks to [miroslav-tashonov](https://github.com/miroslav-tashonov)
- [x] New tests engine (this is very awesome), special thanks to [BorysMinaiev](https://github.com/BorysMinaiev)
  , [SpyCheese](https://github.com/SpyCheese), [EmelyanenkoK](https://github.com/EmelyanenkoK)
- [x] Tests helpers with a lot of examples of parsing most of usable cells (could be found in `lib/tests-libs/`),
  special thanks to [miroslav-tashonov](https://github.com/miroslav-tashonov)
  and [Trinketer22](https://github.com/Trinketer22/)
- [x] NFT, Jettons project example with a lot of tests on new engine, special thanks
  to [Trinketer22](https://github.com/Trinketer22)

### 0.0.32

- [x] Add `sendboc` command, so if `.boc` file pass - will send it via lite-cliente, if `.fif` file pass - will
  invoke `tncli fift sendboc` so fift script will be run, and then boc file on output will be sended
- [x] Add `--data-params` to build command, to auto-generate data cells
- [x] Update `stdlib.fc` to support nft
- [x] Critical fix: `self.wait_for_deploy(contracts=real_contracts)` instead
  of `self.wait_for_deploy(contracts=contracts)`
- [x] Add `.gitignore` to protect contract keys leaks
- [x] Add cell slice parser in lite-client
- [x] Add parse address to `TonUtils.fif`
- [x] Fix custom path to `fift` / `func` / `lite-client` on startup
- [x] Add command wallet to check wallets addresses
- [x] Force `fift` / `func` libs update
- [x] More stability in lite-client interaction
- [x] Send `exteranal_message` to contract without need to provide wrapper of `external_message`, just pass body bytes (
  with support of multiple contracts)
- [x] Send `internal_message` from deploy wallet in one command
- [x] NFT Example deploy
- [x] Add retry parameter to `lite-client`, try several times to do query
- [x] Add windows support
- [x] Func tests
- [x] Custom `stdlib-tests.fc` and `asm-tests.fif` for tests
- [x] Documentation update
- [x] Stdlib fixes

---

### 0.0.16

**Minor fixes**

- [x] Add `help_action` for example projects (e.g. `wallet` project -> `toncli deploy`)
- [x] Remove network configuration download

**Deploy improvment**

- [x] Check `func` / `fift` / `lite-client` on start
- [x] Update yaml project structure
- [x] Add support of multiple contracts in one project
- [x] Add support to deploy one specific contract when you have multiple of them in one project
- [x] Remove `sleep` in project deployment and check true `lite-client`

**New features**

- [x] Run `getmethod` on contract without need to pass contract addr (with support of multiple contracts)
- [x] Add local debug of external messages problem: pass lt hash addr, start `external_code` and receive real error in
  stack
- [x] Add support of running `fift` scripts on get method output, to parse cell outputs :)
- [x] Add `tointeger` command so you can easily convert string to int (needed for func strings)
- [x] Force update of CLI to user
- [x] Rename to `toncli`

**Documentation improvements**

- [x] Provide documentation for `Easy contract manipulation`
- [x] Provide documentation for `Advanced contract manipulation`
