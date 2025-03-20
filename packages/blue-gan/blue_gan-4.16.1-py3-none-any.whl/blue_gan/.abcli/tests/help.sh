#! /usr/bin/env bash

function test_blue_gan_help() {
    local options=$1

    local module
    for module in \
        "@gan" \
        \
        "@gan pypi" \
        "@gan pypi browse" \
        "@gan pypi build" \
        "@gan pypi install" \
        \
        "@gan pytest" \
        \
        "@gan test" \
        "@gan test list" \
        \
        "@gan PyTorch_GAN" \
        \
        "@gan browse" \
        \
        "blue_gan"; do
        abcli_eval ,$options \
            abcli_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
