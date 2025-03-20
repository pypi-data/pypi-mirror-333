"""Entrypoint for serving."""

import json
import logging
import os
import signal
from argparse import ArgumentParser
from subprocess import Popen

from .._lib.constants import UNION_SERVE_CONFIG_ENV_VAR, UNION_SERVE_CONFIG_FILE_NAME

logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser()
    parser.add_argument("--config", type=str)
    parser.add_argument("command", nargs="*")

    args = parser.parse_args()

    serve_config = {}
    env_vars = {}

    logger.info("Starting union-serve")

    if args.config:
        config = json.loads(args.config)

        if config["code_uri"] is not None:
            from .._download import download_code

            download_code(config["code_uri"], os.getcwd())

        if config["inputs"]:
            from .._download import download_inputs

            serve_config["inputs"], env_vars = download_inputs(config["inputs"], os.getcwd())

    for name, value in env_vars.items():
        logger.info(f"Set envvar {name}={value}")
        os.environ[name] = value

    serve_file = os.path.join(os.getcwd(), UNION_SERVE_CONFIG_FILE_NAME)
    with open(serve_file, "w") as f:
        json.dump(serve_config, f)

    os.environ[UNION_SERVE_CONFIG_ENV_VAR] = serve_file

    command_joined = " ".join(args.command)
    logger.info(f"Serving command: {command_joined}")
    p = Popen(command_joined, env=os.environ, shell=True)

    def handle_sigterm(signum, frame):
        p.send_signal(signum)

    signal.signal(signal.SIGTERM, handle_sigterm)
    returncode = p.wait()
    exit(returncode)


if __name__ == "__main__":
    main()
