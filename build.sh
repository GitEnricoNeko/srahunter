#!/bin/bash
$PYTHON -m pip install . --no-deps --ignore-installed -vv
mkdir -p $PREFIX/bin
cp $RECIPE_DIR/scripts/* $PREFIX/bin
chmod +x $PREFIX/bin/*

