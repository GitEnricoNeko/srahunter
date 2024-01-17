#!/bin/bash
mkdir -p $PREFIX/bin
cp $RECIPE_DIR/scripts/*.sh $PREFIX/bin
chmod +x $PREFIX/bin/*.sh
