# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from functools import lru_cache
from os import environ
from typing import Final, List, Optional, Union

from osom_api.logging.logging import SEVERITIES, SEVERITY_NAME_INFO
from osom_api.types.string.to_boolean import string_to_boolean

PROG: Final[str] = "osom-api"
DESCRIPTION: Final[str] = "osom master and worker"
EPILOG: Final[str] = ""

DEFAULT_SEVERITY: Final[str] = SEVERITY_NAME_INFO

CMD_BOT: Final[str] = "bot"
CMD_BOT_HELP: Final[str] = "Bot"
CMD_BOT_EPILOG: Final[str] = ""

CMD_HEALTH: Final[str] = "health"
CMD_HEALTH_HELP: Final[str] = "Healthcheck"
CMD_HEALTH_EPILOG: Final[str] = ""

CMD_MASTER: Final[str] = "master"
CMD_MASTER_HELP: Final[str] = "Master node"
CMD_MASTER_EPILOG: Final[str] = ""

CMD_WORKER: Final[str] = "worker"
CMD_WORKER_HELP: Final[str] = "Worker node"
CMD_WORKER_EPILOG: Final[str] = ""

CMDS = (CMD_BOT, CMD_HEALTH, CMD_MASTER, CMD_WORKER)

DEFAULT_HTTP_HOST: Final[str] = "localhost"
DEFAULT_HTTP_PORT: Final[int] = 8080
DEFAULT_HTTP_TIMEOUT: Final[float] = 8.0

DEFAULT_HEALTHCHECK_TIMEOUT: Final[float] = 8.0
DEFAULT_HEALTHCHECK_URI: Final[str] = f"http://localhost:{DEFAULT_HTTP_PORT}/health"

DEFAULT_REDIS_HOST: Final[str] = "localhost"
DEFAULT_REDIS_PORT: Final[int] = 6379
DEFAULT_REDIS_DATABASE: Final[int] = 0
DEFAULT_REDIS_CONNECTION_TIMEOUT: Final[float] = 8.0
DEFAULT_REDIS_SUBSCRIBE_TIMEOUT: Final[float] = 8.0

REDIS_CONNECTION_TIMEOUT_HELP = (
    f"Redis connection timeout in seconds "
    f"(default: {DEFAULT_REDIS_CONNECTION_TIMEOUT:.2f})"
)
REDIS_SUBSCRIBE_TIMEOUT_HELP = (
    f"Redis subscribe timeout in seconds "
    f"(default: {DEFAULT_REDIS_SUBSCRIBE_TIMEOUT:.2f})"
)

PRINTER_ATTR_KEY: Final[str] = "_printer"

DefaultTypes = Optional[Union[str, bool, int, float]]


def defval(key: str, default: DefaultTypes = None) -> DefaultTypes:
    if default is None:
        return environ.get(key)

    value = environ.get(key, str(default))
    if isinstance(default, str):
        return value
    elif isinstance(default, bool):
        return string_to_boolean(value)
    elif isinstance(default, int):
        return int(value)
    elif isinstance(default, float):
        return float(value)
    else:
        raise TypeError(f"Unsupported default type: {type(default).__name__}")


@lru_cache
def version() -> str:
    # [IMPORTANT] Avoid 'circular import' issues
    from osom_api import __version__

    return __version__


def add_http_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--http-host",
        default=defval("HTTP_HOST", DEFAULT_HTTP_HOST),
        metavar="host",
        help=f"Host address (default: '{DEFAULT_HTTP_HOST}')",
    )
    parser.add_argument(
        "--http-port",
        default=defval("HTTP_PORT", DEFAULT_HTTP_PORT),
        metavar="port",
        type=int,
        help=f"Port number (default: {DEFAULT_HTTP_PORT})",
    )
    parser.add_argument(
        "--http-timeout",
        default=defval("HTTP_TIMEOUT", DEFAULT_HTTP_TIMEOUT),
        metavar="sec",
        type=float,
        help=f"Common timeout in seconds (default: {DEFAULT_HTTP_TIMEOUT})",
    )


def add_redis_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--redis-host",
        default=defval("REDIS_HOST", DEFAULT_REDIS_HOST),
        metavar="host",
        help=f"Redis host address (default: '{DEFAULT_REDIS_HOST}')",
    )
    parser.add_argument(
        "--redis-port",
        default=defval("REDIS_PORT", DEFAULT_REDIS_PORT),
        metavar="port",
        type=int,
        help=f"Redis port number (default: {DEFAULT_REDIS_PORT})",
    )
    parser.add_argument(
        "--redis-database",
        default=defval("REDIS_DATABASE", DEFAULT_REDIS_DATABASE),
        metavar="index",
        type=int,
        help=f"Redis database index (default: {DEFAULT_REDIS_DATABASE})",
    )
    parser.add_argument(
        "--redis-password",
        default=defval("REDIS_PASSWORD"),
        metavar="passwd",
        help="Redis password",
    )

    parser.add_argument(
        "--redis-use-tls",
        action="store_true",
        default=defval("REDIS_USE_TLS", False),
        help="Enable redis TLS mode",
    )
    parser.add_argument(
        "--redis-ca-cert",
        default=defval("REDIS_CA_CERT"),
        help="CA Certificate file to verify with",
    )
    parser.add_argument(
        "--redis-cert",
        default=defval("REDIS_CERT"),
        help="Client certificate to authenticate with",
    )
    parser.add_argument(
        "--redis-key",
        default=defval("REDIS_KEY"),
        help="Private key file to authenticate with",
    )

    parser.add_argument(
        "--redis-connection-timeout",
        default=defval("REDIS_CONNECTION_TIMEOUT", DEFAULT_REDIS_CONNECTION_TIMEOUT),
        metavar="sec",
        type=float,
        help=REDIS_CONNECTION_TIMEOUT_HELP,
    )
    parser.add_argument(
        "--redis-subscribe-timeout",
        default=defval("REDIS_SUBSCRIBE_TIMEOUT", DEFAULT_REDIS_SUBSCRIBE_TIMEOUT),
        metavar="sec",
        type=float,
        help=REDIS_SUBSCRIBE_TIMEOUT_HELP,
    )


def add_s3_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--s3-endpoint",
        default=defval("S3_ENDPOINT"),
        metavar="url",
        help="S3 Endpoint URL",
    )
    parser.add_argument(
        "--s3-access",
        default=defval("S3_ACCESS"),
        metavar="key",
        help="S3 Access Key ID",
    )
    parser.add_argument(
        "--s3-secret",
        default=defval("S3_SECRET"),
        metavar="key",
        help="S3 Secret Access Key",
    )
    parser.add_argument(
        "--s3-region",
        default=defval("S3_REGION"),
        metavar="region",
        help="S3 Region Name",
    )


def add_supabase_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--supabase-url",
        default=defval("SUPABASE_URL"),
        metavar="url",
        help="Supabase Project URL",
    )
    parser.add_argument(
        "--supabase-key",
        default=defval("SUPABASE_KEY"),
        metavar="key",
        help="Supabase Anon Key",
    )


def add_telegram_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--telegram-token",
        default=defval("TELEGRAM_TOKEN"),
        metavar="token",
        help="Telegram API Token",
    )


def add_cmd_bot_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_BOT,
        help=CMD_BOT_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_BOT_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)
    add_redis_arguments(parser)
    add_s3_arguments(parser)
    add_supabase_arguments(parser)
    add_telegram_arguments(parser)


def add_cmd_health_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_HEALTH,
        help=CMD_HEALTH_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_HEALTH_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)

    parser.add_argument(
        "--timeout",
        default=defval("HEALTHCHECK_TIMEOUT", DEFAULT_HEALTHCHECK_TIMEOUT),
        metavar="sec",
        type=float,
        help=f"Common timeout in seconds (default: {DEFAULT_HEALTHCHECK_TIMEOUT})",
    )
    parser.add_argument(
        "uri",
        default=defval("HEALTHCHECK_URI", DEFAULT_HEALTHCHECK_URI),
        nargs="?",
        help=f"Healthcheck URI (default: '{DEFAULT_HEALTHCHECK_URI}')",
    )


def add_cmd_master_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_MASTER,
        help=CMD_MASTER_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_MASTER_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)
    add_http_arguments(parser)
    add_redis_arguments(parser)
    add_s3_arguments(parser)
    add_supabase_arguments(parser)


def add_cmd_worker_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_WORKER,
        help=CMD_WORKER_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_WORKER_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)
    add_redis_arguments(parser)
    add_s3_arguments(parser)
    add_supabase_arguments(parser)


def default_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=PROG,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )

    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument(
        "--colored-logging",
        "-c",
        action="store_true",
        default=defval("COLORED_LOGGING", False),
        help="Use colored logging",
    )
    logging_group.add_argument(
        "--simple-logging",
        "-s",
        action="store_true",
        default=defval("SIMPLE_LOGGING", False),
        help="Use simple logging",
    )

    parser.add_argument(
        "--rotate-logging",
        "-r",
        default=None,
        help="Rotate logging prefix",
    )
    parser.add_argument(
        "--rotate-logging-when",
        default="D",
        help="Rotate logging when",
    )

    parser.add_argument(
        "--use-uvloop",
        action="store_true",
        default=defval("USE_UVLOOP", False),
        help="Replace the event loop with uvloop",
    )
    parser.add_argument(
        "--severity",
        choices=SEVERITIES,
        default=defval("SEVERITY", DEFAULT_SEVERITY),
        help=f"Logging severity (default: '{DEFAULT_SEVERITY}')",
    )

    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        default=defval("DEBUG", False),
        help="Enable debugging mode and change logging severity to 'DEBUG'",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=defval("VERBOSE", 0),
        help="Be more verbose/talkative during the operation",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=version(),
    )

    subparsers = parser.add_subparsers(dest="cmd")
    add_cmd_bot_parser(subparsers)
    add_cmd_health_parser(subparsers)
    add_cmd_master_parser(subparsers)
    add_cmd_worker_parser(subparsers)
    return parser


def get_default_arguments(
    cmdline: Optional[List[str]] = None,
    namespace: Optional[Namespace] = None,
) -> Namespace:
    parser = default_argument_parser()
    return parser.parse_known_args(cmdline, namespace)[0]