#!/usr/bin/env bash

SETUP_FILE_PATH=$(realpath $0)
cd "$(dirname "$SETUP_FILE_PATH")"
NEW_XDG_CONFIG_HOME=$(dirname "$SETUP_FILE_PATH")/xdg_config_dir

# TODO: Update this repository
# command -v git 2>&1 > /dev/null && (git pull | tail -n +2)  # TODO if there's updates, re-exec

# Set XDG_CONFIG_HOME to the directory xdg_config_dir
sed "s,export XDG_CONFIG_HOME=.*,export XDG_CONFIG_HOME=\"$NEW_XDG_CONFIG_HOME\"," template_config/profile > ~/.profile
# Make sure we have the latest profile settings sourced.
source ~/.profile

command -v bash 2>&1 > /dev/null && ln -sf "$PWD/linked_config/bash/bashrc" ~/.bashrc && mkdir -p ${XDG_DATA_HOME:-~/.local/share}/bash
command -v bash 2>&1 > /dev/null && ln -sf "$PWD/linked_config/bash/bash_profile.bash" ~/.bash_profile
command -v bash 2>&1 > /dev/null && ln -sf "$PWD/linked_config/zsh/zshenv" ~/.zshenv
# Load any new bashrc settings.
source ~/.bashrc
# TODO: What to do about aliases?

command -v ssh 2>&1 > /dev/null && mkdir -p ~/.ssh \
    && (for FILE in $(find "$PWD/linked_config/ssh" -name authorized_keys -o -name 'config' -o -name 'user_authorized_keys' | sort); do ln -sf "$FILE" ~/.ssh/; done)

[ ! -f ~/.inputrc ] && ln -sf "$PWD/linked_config/inputrc" ~/.inputrc

# Tmux
# Download tpm if not present and install plugins
if [ ! -d $XDG_CONFIG_HOME/tmux/plugins/tpm ]; then
    git clone https://github.com/tmux-plugins/tpm $XDG_CONFIG_HOME/tmux/plugins/tpm
    $XDG_CONFIG_HOME/tmux/plugins/tpm/bin/install_plugins
fi
# Download Vundle if not present
if [ ! -d $XDG_CONFIG_HOME/vim/bundle/Vundle.vim ]; then
	  git clone https://github.com/VundleVim/Vundle.vim.git $XDG_CONFIG_HOME/vim/bundle/Vundle.vim
fi
# Download oh-my-zsh if not present
if [ ! -d $XDG_CONFIG_HOME/zsh/.oh-my-zsh ]; then
    git clone git@github.com:ohmyzsh/ohmyzsh.git $XDG_CONFIG_HOME/zsh/.oh-my-zsh;
fi

# Install vim plugins
vim -c 'PluginInstall' -c 'qa!' --headless 2> /dev/null;

# Oh-my-zsh
# Configure zsh as default shell
if [ -n "`$SHELL -c 'echo $ZSH_VERSION'`" ]; then
    # Assume in zsh
    echo "" > /dev/null;
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

# TODO: Consider auto-pulling this and adding other crontab jobs
# Setup cron
# echo "Installing crontab";
# crontab crontab
# crontab -l
# echo "Finished installing crontab";
# SETUP_CRON_LINE="0 */6 * * * '$SETUP_FILE_PATH'"
# command -v crontab 2>&1 > /dev/null \
#     && (
#         [ "$(crontab -l | grep "$SETUP_FILE_PATH" | wc -l)" -ne 0 ] \
#         || cat <(crontab -l) <(echo "$SETUP_CRON_LINE") | crontab -
#     ) || (
#         grep ~/.bashrc -e './setup.sh' || cat >> ~/.bashrc <<EOF
# DIR="$PWD"
# cd $XDG_CONFIG_HOME && ./setup.sh
# cd $DIR
# EOF
#     )
