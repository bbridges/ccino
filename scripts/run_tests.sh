#!/bin/sh

# Run the sanity check
sanity = [ `ccino test/core/sanity.py --reporter debug` -eq 'sanity test\n' ]
