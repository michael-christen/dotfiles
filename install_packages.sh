#!/bin/bash

echo "Installing required system packages"

add-apt-repository ppa:martin-frost/thoughtbot-rcm
apt-get update

if [ $(uname) == "Darwin" ]; then
  brew install the_silver_searcher;
elif [ "$(uname)" == "Linux" ]; then
  apt-get install zsh;
  apt-get install silversearcher-ag;
  apt-get install ctags;
  apt-get install clang-format;
	# For vim clipboard=unnamedplus
	apt-get install vim-gtk;
	apt-get install rcm;
	apt-get install tmux;
	apt-get install xclip;
fi
