#!/bin/bash

echo "Updating any git submodules"
git submodule update --init --recursive

echo "Linking configuration files into $HOME";
rcup -v -d files/

echo "Installing tools";
# Install tools
# Oh-my-zsh
if [ ! -d $HOME/.oh-my-zsh ]; then
    git clone git://github.com/robbyrussell/oh-my-zsh.git $HOME/.oh-my-zsh;
fi
# Configure zsh as default shell
if [ -n "`$SHELL -c 'echo $ZSH_VERSION'`" ]; then
    # Assume in zsh
    echo "zsh already configured";
else
    echo "Switching default shell to zsh, enter password:";
    chsh -s $(which zsh);
    echo "You may have to restart your terminal for changes to take effect";
fi

# Generate SSH Key
# From
# https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/
if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
    echo "No ssh key exists, generating it now in $HOME/.ssh/id_rsa.pub!";
    read -p "Enter github email address: " email_address
    ssh-keygen -t rsa -b 4096 -C $email_address;
    eval "$(ssh-agent -s)";
    ssh-add $HOME/.ssh/id_rsa;
fi

# Install vim plugins
# NOTE: UI will pop up
echo "Installing vim plugins";
vim -c 'PluginInstall' -c 'qa!';
echo "Finished installing vim plugins";
