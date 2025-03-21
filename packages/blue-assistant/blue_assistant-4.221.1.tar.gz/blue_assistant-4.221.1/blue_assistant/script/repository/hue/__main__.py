import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from blue_assistant import NAME
from blue_assistant import env
from blue_assistant.script.repository.hue.functions import (
    create_user,
    list_lights,
    set_light_color,
    test,
)
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="create_user | list | set | test",
)
parser.add_argument(
    "--bridge_ip",
    type=str,
    default=env.HUE_BRIDGE_IP_ADDRESS,
)
parser.add_argument(
    "--username",
    type=str,
    default=env.HUE_BRIDGE_USERNAME,
    help="aka API key",
)
parser.add_argument(
    "--light_id",
    type=str,
    default="",
    help="all | <light_id>",
)
parser.add_argument(
    "--hue",
    type=int,
    default=65535,
    help="0 to 65535",
)
parser.add_argument(
    "--saturation",
    type=int,
    default=254,
    help="0 to 254",
)
parser.add_argument(
    "--verbose",
    type=int,
    default=0,
    help="0 | 1",
)
parser.add_argument(
    "--interval",
    type=float,
    default=0.1,
    help="in seconds",
)
args = parser.parse_args()

success = False
if args.task == "create_user":
    username = create_user(
        bridge_ip=args.bridge_ip,
    )
    if username:
        success = True
elif args.task == "list":
    success, _ = list_lights(
        bridge_ip=args.bridge_ip,
        username=args.username,
        verbose=args.verbose == 1,
    )
elif args.task == "set":
    success = set_light_color(
        bridge_ip=args.bridge_ip,
        username=args.username,
        light_id=args.light_id,
        hue=args.hue,
        saturation=args.saturation,
        verbose=args.verbose == 1,
    )
elif args.task == "test":
    success = test(
        bridge_ip=args.bridge_ip,
        username=args.username,
        light_id=args.light_id,
        interval=args.interval,
        hue=args.hue,
        verbose=args.verbose == 1,
    )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
