import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from blue_assistant import NAME
from blue_assistant import env
from blue_assistant.script.repository.hue.functions import set_light_color
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="set",
)
parser.add_argument(
    "--bridge_ip",
    type=str,
    default=env.HUE_BRIDGE_IP_ADDRESS,
)
parser.add_argument(
    "--username",
    type=str,
    help="aka API key",
)
parser.add_argument(
    "--light_id",
    type=str,
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
args = parser.parse_args()

success = False
if args.task == "set":
    success = set_light_color(
        bridge_ip=args.bridge_ip,
        username=args.username,
        light_id=args.light_id,
        hue=args.hue,
        saturation=args.saturation,
        verbose=args.verbose == 1,
    )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
