# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

from colorama import Fore, Style

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class TextUtils:
    FIFT_HELP = f'''positional arguments:
      {bl}command{rs}              Which mode to run, can be [interactive, run, sendboc]
      {gr}   interactive - default, run interactive fift
      {gr}   run - run fift file ([config/fift-lib/] will be auto passed to -I
      {gr}   sendboc - run fift file and run sendfile in lite-client, you need to set only BOC in the stack
                   if it called in project root - will create build/boc/[filename].boc file, else will use temp dir
      {rs}
    '''
    LITE_CLIENT_HELP = f'''positional arguments:
          {bl}command{rs}             
          {gr}   interactive - default, run interactive lite_client
          {gr}   
          {gr}   OTHER - all other arguments will passed to lite_client e.g. tnctl lc help
          {rs}
        '''
    FUNC_HELP = f'''positional arguments:
          {bl}command{rs}             
          {gr}   build - default, build func code in build/ folder, or just build func file 
          {gr}   
          {gr}   OTHER - all other arguments and kwargs will pass to fun command
          {rs}
        '''
    HELP_TEXT = f'''{Fore.YELLOW}TON blockchain is the future 🦄
        --------------------------------
        Command list, e.g. usage: toncli start wallet

        {bl}start - create new project structure based on example project  
        {gr}   wallet - create project with v3 wallet example
        {gr}   nft_collection- project with NFT collection example
        {gr}   nft_item      - project with single nft item example
        {gr}   jetton_minter - project with Jetton minter example
        {gr}   jetton_wallet - project with Jetton wallet example
        {gr}   external_data - create external data usage example
        {gr}   external_code - create external code usage example

        {bl}deploy - deploy current project to blockchain
        {bl}get - run get method on contract
        {bl}send - send internal transaction to contract
        {bl}run_transaction - run remote transaction locally

        {bl}fift / f - interact with fift :)
        {gr}   interactive - default, run interactive fift
        {gr}   run - run fift file ([config/fift-lib/] will be auto passed to -I
        {gr}   sendboc - run fift file and run sendfile in lite-client, to made this work you need to add `saveboc` at the end of file
                    if it called in project root - will create build/boc/[filename].boc file, else will use temp dir

        {bl}lite-client / lc - interact with lite-client :)
        {gr}   interactive - default, run interactive lite-client
        {gr}   
        {gr}   All other commands will pass to lite-client -c (network config will auto pass to command)
        {gr}   e.g. -> toncli lc help

        {bl}func / fc - interact with func :)
        {gr}   build - run build on file or project, will be auto passed stdlib

        {gr}   All other commands will pass to func

        {bl}tointeger - parse string to integer to pass to contract in func

        {bl}sendboc - send file with boc info
        {gr}   "sendboc <path-to-file.boc>" - sends BOC file
        {gr}   "sendboc <path-to=file.fif> <other-params>" -  run fift file and run sendfile in lite-client (just like command "fift sendboc ...")

        {bl}wallet - print addresses of 2 wallets - bounceable wallet and deploy wallet
        {gr}   You can use this command only when wallet is built with commands "toncli build" or "toncli deploy"

        All commands can be found in https://github.com/disintar/toncli/blob/master/docs/advanced/commands.md

        {rs}
        Each command have help e.g.: toncli deploy -h

        Credits: {gr}disintar.io{rs} team
    '''
    VERSION_WARNING = f""" Its seems that your local fift and func libs ({bl}%s{rs}) differs from their actual versions ({bl}%s{rs}). You can update them automatically using "{bl}toncli update_libs{rs}" or disable this warning by changing {gr}"LIBS_WARNING" to "False"{rs} param in cofig\n\n"""
