


## Installation from pre-build

### Linux / macOS (intel)

1. Download needed prebuild for your system from [here](https://github.com/newton-blockchain/ton/actions?query=branch%3Amaster+is%3Acompleted)
2. Install `Python3.9` or higher
3. Run `pip install toncli` or `pip3 install toncli`
   1. If you see `WARNING: The script toncli is installed in '/bla/bla/bla/Python/3.9/bin' which is not on PATH.` please manually add absolute `bin` path to PATH env
4. Run `toncli` and pass absolute path to `func` / `fift` / `lite-client` from first step

### Windows

1. You need to download the latest version of python (3.9+) from the official website, you can do this [here](https://www.python.org/downloads/)
   1. Please, **don't** install Microsoft Store version. It will not work.
2. During installation, on the first screen, you need to click the "Add Python to PATH" checkbox, this is very important!

![image](https://user-images.githubusercontent.com/19264196/160259049-8ed99862-a765-4653-84cb-b6818c0aa0b3.png)

3. After successful installation, open the console (you can do this by pressing `Win+X`, selecting `Windows Terminal` in the menu)

4. Install `toncli` by running `pip install toncli`

5. Download the compiled TON binaries from [here](https://github.com/newton-blockchain/ton/actions/runs/1713804021) (you need to be logged in to GitHub)

![image](https://user-images.githubusercontent.com/19264196/160259203-07fd0e26-9b8e-4aff-b4f0-8e4e6f871088.png)

6. Unzip the downloaded archive 

7. Add [libcrypto-1_1-x64.dll](https://disk.yandex.ru/d/BJk7WPwr_JT0fw) to unziped files

![image](https://user-images.githubusercontent.com/19264196/160259288-3af468d7-74ac-45cb-9001-9f2604cf4119.png)

9. Open the folder in the console (right mouse button, open in the terminal in Windows 11, Windows 10 and less - copy the path in Explorer and in the PowerShell (win+x) and run `cd <<copied path>>`)

10. Run `toncli` in console, it will automatically detect `.exe` files and added paths to config:

![image](https://user-images.githubusercontent.com/19264196/160259355-dacc0234-f8b7-4b9e-b1cd-8a5d6df0712a.png)

11. Success! 

P.S. for a beautiful display of colors and emoticons, it is advised to install the latest version of the 'Windows Terminal Preview' from the Microsoft Store


## Installation from source

### macOS (m1)

1. Please follow [this](/docs/apple_m1_compile_fix.md) guide to compile `func` / `fift`/ `lite-client`
2. Run `pip install toncli` or `pip3 install toncli`
   1. If you see `WARNING: The script toncli is installed in '/bla/bla/bla/Python/3.9/bin' which is not on PATH.` please manually add absolute `bin` path to PATH env
3. Run `toncli` and pass absolute path to `func` / `fift` / `lite-client` from first step

### Linux

1. Follow official [docs](https://ton.org/docs/#/compile) to compile sources
2. Run `pip install toncli` or `pip3 install toncli`
   1. If you see `WARNING: The script toncli is installed in '/bla/bla/bla/Python/3.9/bin' which is not on PATH.` please manually add absolute `bin` path to PATH env
3. Run `toncli` and pass absolute path to `func` / `fift` / `lite-client` from first step


