#!/usr/bin/python

import argparse
import sys

import yaml
from path import Path
from yaml import CLoader

from barrancas.generator import Generator
from barrancas.server import Server

CONFIG = {
    "port": 8000,
}


def main():

    try:
        properties_f = Path("conf.yml").read_text()
        properties = yaml.load(properties_f, Loader=CLoader)
        CONFIG.update(properties)
    except:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server", metavar="PORT", nargs="?", default=None, type=int, required=False
    )
    parser.add_argument(
        "--directory", metavar="DIRECTORY", default=None, type=str, required=False
    )
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()
    if len(sys.argv) > 1:
        if args.server or args.server is None:
            port = CONFIG["port"]
            if not args.server is None:
                port = args.server
            if args.directory:
                directory = args.directory
            else:
                directory = "."
            s = Server(port, directory)
            s.start()
        if args.generate:
            g = Generator(CONFIG)
            g.generate()
    else:
        g = Generator(CONFIG)
        g.generate()


if __name__ == "__main__":
    main()
    sys.exit(0)
