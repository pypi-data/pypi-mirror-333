#! /usr/bin/env bash

function test_blue_gan_version() {
    local options=$1

    abcli_eval ,$options \
        "blue_gan version ${@:2}"
}
