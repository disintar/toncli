# Downloading and compiling TON modules on computers with Apple M1
Compiling TON modules on Apple M1 can be a tricky task, so we decided to create this guide
## 1. Clone sources from official repository
```
git clone --recursive https://github.com/newton-blockchain/ton
cd ton
```
Cloning recursively to get all needed repos automatically

## 2. Fixing rocksdb
```
cd third-party/rocksdb
git checkout v6.27.3
```
Change rocksdb branch to branch, where Apple M1 is supported (maybe it can be master)

## 3. Building
Execute from root repository directory
```
mkdir build
cd build
CC="clang -mcpu=apple-a14" CXX="clang++ -mcpu=apple-a14" cmake .. -DCMAKE_BUILD_TYPE=Release -DTON_ARCH= -Wno-dev -DOPENSSL_ROOT_DIR=/opt/homebrew/opt/openssl@3 -DCMAKE_OSX_SYSROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX12.1.sdk/
cmake --build .
```
## 4. Results
If building was successful, needed binary files will be in their directories:
1. func: `build/crypto/func`
2. fift: `build/crypto/fift`
3. lite-client `build/lite-client/lite-client`

You can link or copy them to `/usr/local/bin` and toncli will find them automatically