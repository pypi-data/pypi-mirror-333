#! /usr/bin/env bash

function blue_gan_action_git_before_push() {
    blue_gan build_README
    [[ $? -ne 0 ]] && return 1

    [[ "$(abcli_git get_branch)" != "main" ]] &&
        return 0

    blue_gan pypi build
}
