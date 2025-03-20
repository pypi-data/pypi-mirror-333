#! /usr/bin/env bash

function blue_gan_ingest() {
    local options=$1
    local dataset=$(abcli_option "$options" dataset animal10)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_upload=$(abcli_option_int "$options" upload 0)
    local use_cache=$(abcli_option_int "$options" cache 1)

    local object_name=$(abcli_clarify_object $2 $dataset-$(abcli_string_timestamp_short))

    local ingest_options=$3

    if [[ "$dataset" == "animal10" ]]; then
        local cache_object_name=""
        if [[ "$use_cache" == 1 ]]; then
            cache_object_name=$(abcli_mlflow_tags_search \
                dataset=$dataset,full_cache=1 \
                --log 0 \
                --count 1)
            [[ -z "$cache_object_name" ]] &&
                abcli_log "$dataset cache not found, caching now."
        fi

        if [[ ! -z "$cache_object_name" ]]; then
            if [[ ! -f "$ABCLI_OBJECT_ROOT/$cache_object_name/translate.py" ]]; then
                abcli_log_warning "$cache_object_name: cache is invalid, regenerating ..."
                cache_object_name=""
            fi
        fi

        if [[ -z "$cache_object_name" ]]; then
            cache_object_name=$dataset-full_cache-$(abcli_string_timestamp_short)
            local cache_object_path=$ABCLI_OBJECT_ROOT/$cache_object_name

            abcli_log "caching $dataset -> $cache_object_name ..."

            abcli_eval dryrun=$do_dryrun \
                "kaggle datasets download \
                -d alessiocorrado99/animals10 \
                -p $cache_object_path"
            [[ $? -ne 0 ]] && return 1

            local zip_filename=$cache_object_path/animals10.zip
            abcli_eval dryrun=$do_dryrun \
                unzip \
                $zip_filename \
                -d $cache_object_path
            [[ $? -ne 0 ]] && return 1

            rm -v $zip_filename

            abcli_mlflow_tags_set \
                $cache_object_name \
                dataset=$dataset,full_cache=1
        fi

        local animal=$(abcli_option "$ingest_options" animal cat)
        local count=$(abcli_option "$ingest_options" count 10)
        abcli_log "ingesting $cache_object_name/$animal -count=$count-> $object_name ..."

        abcli_eval dryrun=$do_dryrun \
            python3 -m blue_gan.ingest $dataset \
            --animal $animal \
            --count $count \
            --cache_object_name $cache_object_name \
            --object_name $object_name
        [[ $? -ne 0 ]] && return 1

        abcli_mlflow_tags_set \
            $object_name \
            contains_$animal=1
    else
        abcli_log_error "$dataset: dataset not found".
        return 1
    fi

    abcli_mlflow_tags_set \
        $object_name \
        dataset=$dataset

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name
}
