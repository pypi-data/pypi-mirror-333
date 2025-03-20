#! /usr/bin/env bash

function abcli_install_blue_gan() {
    abcli_git_clone https://github.com/eriklindernoren/PyTorch-GAN
    pushd $abcli_path_git/PyTorch-GAN/ >/dev/null
    pip3 install -r requirements.txt
    popd >/dev/null
}

abcli_install_module blue_gan 1.1.1
