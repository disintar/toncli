## Change Log

### 0.0.15

**Minor fixes**

- [x] Add `help_action` for example projects (e.g. `wallet` project -> `tncli deploy`)
- [x] Remove network configuration download

**Deploy improvment**

- [x] Check `func` / `fift` / `lite-client` on start
- [x] Update yaml project structure
- [x] Add support of multiple contracts in one project
- [x] Add support to deploy one specific contract when you have multiple of them in one project
- [x] Remove `sleep` in project deployment and check true `lite-client`

**New features**

- [x] Run `getmethod` on contract without need to pass contract addr (with support of multiple contracts)
- [ ] Send `exteranal_message` to contract without need to provide wrapper of `external_message`, just pass body bytes (
  with support of multiple contracts)
- [x]  Add local debug of external messages problem: pass lt hash addr, start `external_code` and receive real error in
  stack
- [x] Add support of running `fift` scripts on get method output, to parse cell outputs :)
- [x] Add `tointeger` command so you can easily convert string to int (needed for func strings)
- [x] Force update of CLI to user

**Documentation improvements**

- [ ] Provide documentation for `Easy contract manipulation`
- [ ] Provide documentation for `Advanced contract manipulation`
