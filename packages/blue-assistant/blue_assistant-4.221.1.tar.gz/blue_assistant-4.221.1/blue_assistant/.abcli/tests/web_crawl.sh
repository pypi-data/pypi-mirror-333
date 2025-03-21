#! /usr/bin/env bash

function test_blue_assistant_web_crawl() {
    local options=$1

    abcli_eval ,$options \
        blue_assistant_web_crawl \
        ~upload \
        https://ode.rsl.wustl.edu/+https://oderest.rsl.wustl.edu/ \
        test_blue_assistant_web_crawl-$(abcli_string_timestamp_short) \
        --max_iterations 3
}
