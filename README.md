# Version Controlled Configuration

This mostly copies my friend's dotfiles setup:
https://github.com/mark64/dotfiles, which takes advantage of the
[XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).

- currently setup to track and configure these main tools:
  - git
  - vim
  - tmux
  - zsh
  - several others are configured simply through the use of XDG_CONFIG_HOME
	redirection
- terminal colors: need to also select from terminal preferences

## Layout

- `setup.sh`: the script that sets all of this up
- `.gitignore`: all of the XDG_CONFIG_HOME files we don't want to track
- config directories:
  - `linked_config`: config files that have to be linked / aren't able to use
	the XDG_CONFIG_HOME overwrite
  - `template_config`: config that we modify and then set
  - `xdg_config_dir`: XDG_CONFIG_HOME tracked files

## How To Use / Installation
- Note this will override several files, best to save them for future use if
  running for the first time
  - `~/.bash_profile`
  - `~/.bashrc`
  - `~/.inputrc`
  - `~/.profile`
  - `~/.ssh/authorized_keys`
  - `~/.ssh/config`
  - `~/.zshenv`
- Custom overrides are available with `xdg_config_dir/`:
  - `git/userconfig` -> `git/config`
  - `userprofile` -> `~/.profile`
  - `user.aliases` -> `shared.aliases`
  - `linked_config/ssh/user_authorized_keys` -> `~/.ssh/authorized_keys`
- requires installation of several system utilities, see
  https://github.com/michael-christen/toolbox/blob/35af433e6c955fd6bc50b4a98d4ca8576d5bfdb6/ansible_playbooks/dev_setup.yaml
  for an example
- run `./setup.sh`
- if this is your first time, you'll want to logout/login to ensure UI
  applications can use the new XDG_ environment variables

- Update tmux plugins with `<prefix> + I`

## Future Plans / TODOs
- auto-update the repo / improve crontab definitions
- Use more neovim features, eg) mason: https://github.com/williamboman/mason.nvim

## Other Manual Steps

### GPG Key signing
```
# Follow defaults, enter user info and passphrase
gpg --full-generate-key

# List and copy key id, looking for sec rsa.../<key>
gpg --list-secret-keys --keyid-format=long

# Export
gpg --armor --export <key>

# Add to github

# Update user git config
git config --global --unset gpg.format
# eg, write
[user]
	signingkey = 69F1D7374821253F
[commit]
	gpgsign = true

# to xdg_config_dir/git/userconfig

# to xdg_config_dir/userprofile
# XXX: or should it be a .rc?
# GPG_TTY=$(tty)
# pgrep gpg-agent > /dev/null || /usr/bin/gpg-agent

# Cache GPG key 2 hours at a time instead of asking for password regularly
mkdir -p ~/.gnupg
echo -e "\ndefault-cache-ttl 7200\nmax-cache-ttl 7200" >> ~/.gnupg/gpg-agent.conf
# Restart GPG agent to apply changes
gpgconf --reload gpg-agent

# can setup gh with gh auth login -p ssh -h $GH_HOST --web
```
