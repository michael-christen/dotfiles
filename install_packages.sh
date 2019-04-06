#!/bin/bash

echo "Installing required system packages"

if [ $(uname) == "Darwin" ]; then
  brew install the_silver_searcher;
elif [ "$(uname)" == "Linux" ]; then
  apt-get install zsh;
  apt-get install silversearcher-ag;
  apt-get install ctags;
  apt-get install clang-format;
fi
