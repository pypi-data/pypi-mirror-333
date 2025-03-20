import argparse
import sys

from iprm.cli.app import main as cli_main
from iprm.studio_cxx.app import main as studio_cxx_main
from iprm.studio_rust.app import main as studio_rust_main


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--cli', action='store_true', help='IPRM Command Line Interface')
    parser.add_argument('--studio-cxx', action='store_true', help='IPRM Studio (C++)')
    parser.add_argument('--studio-rust', action='store_true', help='IPRM Studio (Rust)')
    args, remaining_args = parser.parse_known_args()
    sys.argv = [sys.argv[0]] + remaining_args
    if args.cli:
        cli_main()
    elif args.studio_cxx:
        studio_cxx_main()
    elif args.atudio_rust:
        studio_rust_main()


if __name__ == '__main__':
    main()
