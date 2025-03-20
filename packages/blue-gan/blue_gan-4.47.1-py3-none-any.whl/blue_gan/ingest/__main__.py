import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from blue_gan import NAME
from blue_gan.ingest import animals10
from blue_gan.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="animal10",
)
parser.add_argument(
    "--animal",
    type=str,
    default="cat",
    help=" | ".join(sorted(animals10.translate.values())),
)
parser.add_argument(
    "--count",
    type=int,
    default=10,
    help="-1: all",
)
parser.add_argument(
    "--cache_object_name",
    type=str,
)
parser.add_argument(
    "--object_name",
    type=str,
)
args = parser.parse_args()

success = False
if args.task == "animal10":
    success = animals10.ingest(
        animal=args.animal,
        count=args.count,
        cache_object_name=args.cache_object_name,
        object_name=args.object_name,
    )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
