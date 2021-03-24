#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
function mfb {
    outfile=/tmp/mfb_$(date +%s)_${RANDOM}
    python3 ${DIR}/mfb.py -o $outfile
    if [ -f "$outfile" ]; then
        path=$(cat $outfile)
        rm $outfile
        if ! [ -z "$path" ]; then
            cd $path
        fi
    fi
}

