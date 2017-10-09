#!/bin/sh

for f in $(find files/ -mindepth 1 -maxdepth 1); do
  echo "Linking ${f} into home directory";
  # Use -sf if desire to force override
  ln -s -t ~/ $(realpath $f);
done

# Install tools
# Oh-my-zsh
git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
# Configure zsh as default shell
chsh -s $(which zsh)
# Reload zsh config
source ~/.zshrc
