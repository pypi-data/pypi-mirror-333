#! /usr/bin/env bash

function test_blue_gan_README() {
    local options=$1

    abcli_eval ,$options \
        blue_gan build_README
}
