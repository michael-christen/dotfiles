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

XXX: tmux copy/paste is broken / tmux navigation from vim is too?

## Log

### 2024-03

- Setup [obsidian.nvim](https://github.com/epwalsh/obsidian.nvim)
  - caused
  [restructuring of nvim plugins](https://github.com/folke/lazy.nvim?tab=readme-ov-file#-structuring-your-plugins)
  - Even handles [`^` block links](https://help.obsidian.md/Linking+notes+and+files/Internal+links)
  - note: <ctrl-k> then a motion shows what it is in vim
  - add new fonts with [nerdfont](https://www.nerdfonts.com)
    - list with `fc-list`
    - install to ~/.local/share/fonts
      - could do with [webi](https://github.com/webinstall/webi-installers)
    - rebuild font cache `fc-cache -fv`
    - update fonts used in system via gnome-tweaks, can script by doing it
      there and watching with `dconf watch /`
      - `dconf write /org/gnome/desktop/interface/monospace-font-name "'UbuntuMono Nerd Font Mono 13'"`
    - update fonts used in [chrome settings > appearance > customize fonts](chrome://settings/fonts)
      (Standard font) to "Ubuntu nerd font"
      - https://github.com/ryanoasis/nerd-fonts/blob/master/bin/scripts/lib/i_oct.sh should show up
