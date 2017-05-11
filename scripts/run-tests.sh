#!/bin/sh

# Run the sanity check
sanity="$(ccino test/core/sanity.py --config false --out /dev/null)"

if [ "$sanity" != "sanity test" ]; then
    echo 'Sanity test failed.'
    exit 1
fi

echo 'Sanity test passed.'
