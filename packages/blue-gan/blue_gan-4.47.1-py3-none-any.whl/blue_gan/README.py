import os

from blue_options.help.functions import get_help
from blue_objects import file, README

from blue_gan import NAME, VERSION, ICON, REPO_NAME
from blue_gan import PyTorch_GAN
from blue_gan import stylegan2_pytorch
from blue_gan.help.functions import help_functions


items = README.Items(
    [
        {
            "name": "stylegan2-pytorch",
            "marquee": stylegan2_pytorch.marquee,
            "description": "Simple StyleGan2 for Pytorch. ⏸️",
            "url": "./blue_gan/docs/stylegan2_pytorch.md",
        },
        {},
        {
            "name": "PyTorch-GAN",
            "marquee": PyTorch_GAN.marquee,
            "description": "6+ years old, missing assets, bugs. 🛑",
            "url": "./blue_gan/docs/PyTorch_GAN.md",
        },
        {
            "name": "What is a GAN?",
            "marquee": "https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/11/11/ML-6149-image025.jpg",
            "description": "Background review.",
            "url": "https://aws.amazon.com/what-is/gan/",
        },
    ]
)


def build():
    return all(
        README.build(
            items=readme.get("items", []),
            cols=readme.get("cols", 3),
            path=os.path.join(file.path(__file__), readme["path"]),
            ICON=ICON,
            NAME=NAME,
            VERSION=VERSION,
            REPO_NAME=REPO_NAME,
            help_function=lambda tokens: get_help(
                tokens,
                help_functions,
                mono=True,
            ),
        )
        for readme in [
            {
                "items": items,
                "cols": 2,
                "path": "..",
            },
            {
                "path": "docs/PyTorch_GAN.md",
            },
            {
                "path": "docs/stylegan2_pytorch.md",
            },
        ]
    )
