from typing import List

from blue_options.terminal import show_usage, xtra
from abcli.help.generic import help_functions as generic_help_functions

from blue_gan import ALIAS
from blue_gan.help.ingest import help_ingest
from blue_gan.help.PyTorch_GAN import help_PyTorch_GAN
from blue_gan.help.stylegan2_pytorch import help_stylegan2_pytorch


def help_browse(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "actions|repo"

    return show_usage(
        [
            "@gan",
            "browse",
            f"[{options}]",
        ],
        "browse blue_gan.",
        mono=mono,
    )


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "browse": help_browse,
        "ingest": help_ingest,
        "PyTorch_GAN": help_PyTorch_GAN,
        "stylegan2_pytorch": help_stylegan2_pytorch,
    }
)
