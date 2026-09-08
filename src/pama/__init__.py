import argparse
import asyncio
import getpass
import os
import sys
from typing import Optional, NamedTuple

from pama.exceptions.service import ServiceError
from pama.models.account import Account
from pama.service import account as service
from pama.settings.settings import config


class ScriptArgs(NamedTuple):
    key_master: str
    account_name: Optional[str]
    create_account: Optional[list[str]]

def build_parser() -> argparse.ArgumentParser:
    """
    Build and set an argument parser.
    :return:
    """
    parser = argparse.ArgumentParser(
        description="Script for getting and creating accounts.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument (
        "-k",
        "--key_master",
        dest="key_master",
        type=str,
        default=os.getenv("PAMA_KEY_MASTER"),
        help="Master account key. If not provided, PAMA_KEY_MASTER environment variable will be used. If none of these are provided, key master will be asked.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-a",
        "--account_name",
        dest="account_name",
        type=str,
        help="Account name for getting their pw."
    )

    group.add_argument(
        "-c",
        "--create_account",
        dest="create_account",
        type=str,
        nargs="+", # At least 1.
        metavar=("ACCOUNT_NAME", "PW"),
        help="Create an account with given account name and password. Examples: `pama -k 'blah blah' -c 'acc name', 'af#ees!'`, `pama -c 'acc name'` <- key master and account pw will be asked."
    )
    return parser

def parse_args(args: Optional[list[str]] = None) -> ScriptArgs:
    """
    Analyze and validate args.
    :param args:
    :return:
    """
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.account_name and not parsed.create_account:
        parser.error(
            "-a/--account_name or -c/--create_account must be provided."
        )

    # When environment variable for master key doesn't exist and user doesn't enter -k param, ask for master key.
    if not parsed.key_master:
        parsed.key_master = getpass.getpass("Type the master account key: ")

    # When -c flag is present, check if only name or name and pw. If not pw, ask for it.
    if parsed.create_account is not None:
        if len(parsed.create_account) > 2:
            parser.error("-c/--create_account 2 args max ([1-2]).")
        elif len(parsed.create_account) == 1:
            parsed.create_account.append(getpass.getpass("Type the account password: "))

    return ScriptArgs(
        key_master=parsed.key_master,
        account_name=parsed.account_name,
        create_account=parsed.create_account
    )




def main() -> None:
    args = parse_args()

    service.set_encoder(args.key_master, salt=config.salt)

    if args.account_name is not None:
        try:
            result = asyncio.run(service.search_account(name=args.account_name))
            if len(result) < 1:
                print("Error: No such account", file=sys.stderr)
                sys.exit(1)
            else:
                print(service.decode_pw(result[0].passw))
        except ServiceError as e:
            print(e.msg, file=sys.stderr)
            sys.exit(1)

    elif args.create_account is not None:
        try:
            account = Account(name=args.create_account[0], passw=args.create_account[1].encode("utf-8"),
                              comments="", url="")
            asyncio.run(service.create_account(account))
        except ServiceError as e:
            print(e.msg, file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()