#!/bin/sh

echo "Linking configuration files into $HOME";

for f in $(find files -mindepth 1 -maxdepth 1); do
    f_base=$(basename $f);
    if [ "$(readlink $HOME/$f_base)" -ef "$f" ]; then
        echo "${f} already linked"
    else
        echo "Linking ${f} into home directory";
        # Use -sf if desire to force override
        ln -s $(realpath $f) $HOME/;
    fi
done


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
