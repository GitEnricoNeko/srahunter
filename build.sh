#!/bin/bash
mkdir -p $PREFIX/bin
cp $RECIPE_DIR/scripts/* $PREFIX/bin
chmod +x $PREFIX/bin/
$PYTHON -m pip install $RECIPE_DIR/. -vv

