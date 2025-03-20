#! /usr/bin/env bash

function blue_gan_PyTorch_GAN() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    local algo=$2
    if [[ "+$BLUE_GAN_LIST_OF_ALGO+" != *"+$algo+"* ]]; then
        abcli_log_error "$algo: algo not found."
        return 1
    fi

    # https://github.com/eriklindernoren/PyTorch-GAN?tab=readme-ov-file#bicyclegan
    pushd $abcli_path_git/PyTorch-GAN/ >/dev/null
    cd data/
    bash download_pix2pix_dataset.sh edges2shoes
    cd ../implementations/bicyclegan/
    python3 bicyclegan.py
    popd >/dev/null
}
