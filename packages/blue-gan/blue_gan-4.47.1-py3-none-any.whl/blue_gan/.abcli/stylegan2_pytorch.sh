#! /usr/bin/env bash

function blue_gan_stylegan2_pytorch() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local dataset_object_name=$(abcli_clarify_object $2 .)
    local dataset_object_path=$ABCLI_OBJECT_ROOT/$dataset_object_name
    [[ "$do_download" == 1 ]] &&
        abcli_download - $dataset_object_name

    local results_object_name=$(abcli_clarify_object $3 stylegan2_pytorch-results-$(abcli_string_timestamp_short))
    local results_object_path=$ABCLI_OBJECT_ROOT/$results_object_name

    abcli_log "stylegan2_pytorch: $dataset_object_name -> $results_object_name ..."

    abcli_eval dryrun=$do_dryrun \
        stylegan2_pytorch \
        --data $dataset_object_path \
        --results_dir $results_object_path \
        --models_dir $results_object_path/models \
        "${@:4}"
    [[ $? -ne 0 ]] && return 1

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $output_object_name

    return 0
}
