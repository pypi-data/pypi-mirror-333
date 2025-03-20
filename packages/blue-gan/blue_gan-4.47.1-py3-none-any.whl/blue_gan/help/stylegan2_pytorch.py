from typing import List

from blue_options.terminal import show_usage, xtra


def help_stylegan2_pytorch(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("~download,dryrun,~upload", mono=mono)

    args = ["<args>"]

    return show_usage(
        [
            "@gan",
            "stylegan2_pytorch",
            f"[{options}]",
            "[.|<dataset-object-name>]",
            "[-|<results-object-name>]",
        ]
        + args,
        "run stylegan2_pytorch.",
        mono=mono,
    )
