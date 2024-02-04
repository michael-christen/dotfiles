#!/usr/bin/env bash

# Manage these various files:
# $PWD/profile -> .profile
# $PWD/bash/bashrc  -> .bashrc
# $PWD/bash/bash_profile.bash  -> .bash_profile
# $PWD/ssh/authorized_keys -> .ssh/authorized_keys
# $PWD/ssh/config -> .ssh/config
# $PWD/inputrc -> .inputrc
# Make directories
# ${XDG_DATA_HOME:~/.local/share}/bash
# ~/.ssh
# Tools supported / tracked
# - git
# - bash
# - nvim

# Do I want these? set -o errexit
# set -o pipefail

# XXX: Remove need for submodules, plugins, etc ...
# echo "Updating any git submodules"
# git submodule update --init --recursive

SETUP_FILE_PATH=$(realpath $0)
cd "$(dirname "$SETUP_FILE_PATH")"

# XXX: Consider doing this
# Update this repository
# NOTE: `command -v "cmd" 2>&1 > /dev/null` checks for existence of `cmd`
# command -v git 2>&1 > /dev/null && (git pull | tail -n +2)  # XXX if there's updates, re-exec

# Set XDG_CONFIG_HOME to this directory
sed "s,export XDG_CONFIG_HOME=.*,export XDG_CONFIG_HOME=\"$(dirname "$SETUP_FILE_PATH")\"," profile > ~/.profile
# Make sure we have the latest profile settings sourced.
source ~/.profile

command -v bash 2>&1 > /dev/null && ln -sf "$PWD/bash/bashrc" ~/.bashrc && mkdir -p ${XDG_DATA_HOME:-~/.local/share}/bash
command -v bash 2>&1 > /dev/null && ln -sf "$PWD/bash/bash_profile.bash" ~/.bash_profile
# Load any new bashrc settings.
source ~/.bashrc
# XXX: What to do about aliases?


# # Generate SSH Key
# # From
# # https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/
# if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
#     echo "No ssh key exists, generating it now in $HOME/.ssh/id_rsa.pub!";
#     read -p "Enter github email address: " email_address
#     ssh-keygen -t rsa -b 4096 -C $email_address;
#     eval "$(ssh-agent -s)";
#     ssh-add $HOME/.ssh/id_rsa;
# fi
# XXX: Remove .pub?
command -v ssh 2>&1 > /dev/null && mkdir -p ~/.ssh \
    && (for FILE in $(find "$PWD/ssh" -name authorized_keys -o -name '*.pub' -o -name 'config'); do ln -sf "$FILE" ~/.ssh/; done)

[ ! -f ~/.inputrc ] && ln -sf "$PWD/inputrc" ~/.inputrc


# XXX: Install neovim / vim updates
# HASNVIM=$(command -v nvim 2> /dev/null)
# [ "$HASNVIM" ] && [ "$XDG_CONFIG_HOME" ] \
#     && command -v git 2>&1 > /dev/null \
#     && nvim --headless -c 'autocmd User MasonUpdateAll quitall' -c 'quitall' > /dev/null
# # XXX I want to view the change logs, maybe have them be emailed?
# #     && nvim --headless -c 'autocmd User Lazy update quitall' -c 'quitall' > /dev/null \

# # Install vim plugins
# # NOTE: UI will pop up
# echo "Installing vim plugins";
# vim -c 'PluginInstall' -c 'qa!';
# echo "Finished installing vim plugins";

# Setup cron
# echo "Installing crontab";
# crontab crontab
# crontab -l
# echo "Finished installing crontab";

# XXX: Consider auto-pulling this
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

# echo "Installing tools";
# # Install tools
# # Oh-my-zsh
# if [ ! -d $HOME/.oh-my-zsh ]; then
#     git clone git://github.com/robbyrussell/oh-my-zsh.git $HOME/.oh-my-zsh;
# fi
# # Configure zsh as default shell
# if [ -n "`$SHELL -c 'echo $ZSH_VERSION'`" ]; then
#     # Assume in zsh
#     echo "zsh already configured";
# else
#     echo "Switching default shell to zsh, enter password:";
#     chsh -s $(which zsh);
#     echo "You may have to restart your terminal for changes to take effect";
# fi
