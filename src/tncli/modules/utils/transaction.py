import tempfile
from typing import Optional

import requests as r
from jinja2 import FileSystemLoader, Environment, select_autoescape

from tncli.modules.utils.lite_client.lite_client import LiteClient
from tncli.modules.utils.system.conf import toncenter, project_root
from tncli.modules.utils.fift.fift import Fift
from tncli.modules.utils.lite_client.commands import get_account_status
import base64
import urllib.parse


def parse_workchain(smc_address: str) -> int:
    """Parse workchain https://ton.org/docs/#/howto/step-by-step"""
    decoded_addr = base64.urlsafe_b64decode(smc_address)
    worckchain_signed_8 = decoded_addr[1]
    worckchain_signed_8 = (((worckchain_signed_8 >> 7) * 128) ^ worckchain_signed_8) - (
            (worckchain_signed_8 >> 7) * 128)
    return worckchain_signed_8


def run_transaction(network: str, smc_address: str, logical_time: str, tx_hash: str, function: int,
                    save_location: Optional[str] = None):
    """Download transaction and run it locally

    :param function: Function selector of runv
    :param network: Network to run transaction debugging
    :param smc_address: Address of smart contract
    :param logical_time: Logical time of transaction
    :param tx_hash: Hash of transaction
    :return:
    """
    # TODO: auto detect function if it possible

    logical_time = int(logical_time)

    tx_hash = urllib.parse.quote(tx_hash)
    wc = parse_workchain(smc_address)

    # Get block of transaction to get code and data on this block, we need to take it by logical time
    lite_client = LiteClient('bylt',
                             args=[f"{wc}:8000000000000000", str(logical_time)], kwargs={'lite_client_args': '-v 0',
                                                                                         'net': network,
                                                                                         'update': False},
                             get_output=True)
    answer = lite_client.run().decode()

    # Get previous block (so account data, code, amount not changed yet)
    prev_block = ''
    for i in answer.split('\n'):
        if 'previous block' in i:
            prev_block = i.split()[-1]
            break

    # Get account balance
    amount, _ = get_account_status(network, smc_address, update_config=False, block_id_ext=prev_block)
    amount *= 1000000000

    # TODO: use lite client
    answer = r.get(
        f"{toncenter[network]}/getTransactions?address={smc_address}&limit=1&lt={logical_time}&hash={tx_hash}&archival=true")
    result = answer.json()["result"][0]

    # Get message value
    msg_value = int(result["in_msg"]["value"])
    # Get message utime
    time = int(result["utime"])
    # Get transaction hex
    tx = base64.b64decode(result["data"]).hex().upper()

    # Get message body
    message = base64.b64decode(result["in_msg"]["msg_data"]["body"]).hex().upper()

    # Generate temporary location for all needed files
    to_save_location: str = tempfile.mkstemp(suffix='.fif')[1]
    to_save_location_c3: str = tempfile.mkstemp(suffix='.boc')[1]
    to_save_location_c4: str = tempfile.mkstemp(suffix='.boc')[1]
    to_save_location_config: str = tempfile.mkstemp(suffix='.boc')[1]

    # Save account code
    lite_client = LiteClient('saveaccountcode',
                             args=[to_save_location_c3, smc_address, prev_block],
                             kwargs={'lite_client_args': '-v 0',
                                     'net': network,
                                     'update': False},
                             get_output=True)
    lite_client.run()

    # Save account data
    lite_client = LiteClient('saveaccountdata',
                             args=[to_save_location_c4, smc_address, prev_block],
                             kwargs={'lite_client_args': '-v 0',
                                     'net': network,
                                     'update': False},
                             get_output=True)
    lite_client.run()

    # TODO: Use [block-id-ext]
    # Save global config
    lite_client = LiteClient('saveconfig',
                             args=[to_save_location_config],
                             kwargs={'lite_client_args': '-v 0',
                                     'net': network,
                                     'update': False},
                             get_output=True)
    lite_client.run()

    # Add info to Jinja template
    render_kwargs = {
        'tx_hex': tx,
        'message_hex': message,
        'msg_value': msg_value,
        'c3': to_save_location_c3,
        'c4': to_save_location_c4,
        'config': to_save_location_config,
        'time': time,
        'smc_address': smc_address,
        'trans_lt': str(logical_time),
        'amount': amount,
        'function': str(function)
    }

    # Load template of transaction_debug
    loader = FileSystemLoader(f"{project_root}/modules/fift")

    env = Environment(
        loader=loader,
        autoescape=select_autoescape()
    )

    template = env.get_template("transaction_debug.fif.template")

    rendered = template.render(**render_kwargs)

    if save_location:
        with open(save_location, 'w') as f:
            f.write(rendered)
    else:
        with open(to_save_location, 'w') as f:
            f.write(rendered)

            # Run generated by jinja fift script
        fift = Fift('run', args=[to_save_location, prev_block])
        fift.run()


if __name__ == "__main__":
    run_transaction('testnet', 'EQBzEuizZDQva_Q-MsMtPBpcrHODSf8SqE0Eoi7-5gUlltyv', '8677048000001',
                    'f8FbgaufZbdZLMzFlle9iMgfDMbJleuEfIbtq8ybUJ8=', -1)
