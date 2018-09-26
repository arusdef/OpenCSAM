#!/bin/bash

for md in $(find . -name "*.md" | grep -v node_modules); do 
    html="$(echo $md | sed 's~.md~.html~g')"
    html="$(echo $html | sed 's~^./~./documentation/~')"
    echo "Converting $md to $html"
    dirname="${html%/*}"
    mkdir -p "$dirname"
    pandoc -f markdown -t html5 -c pandoc.css -s "$md" -o "$html"
done