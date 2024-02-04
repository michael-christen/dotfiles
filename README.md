# Version Controlled Configuration

This mostly copies my friend's dotfiles setup:
https://github.com/mark64/dotfiles, which takes advantage of the
[XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).

In progress notes follow:
- currently setup to track:
  - git
  - vim
  - tmux
  - zsh (maybe switch to fish?)
  - ctags (maybe remove?)
- terminal colors: need to also select from terminal preferences

TODO:
- Migrate old ~/.config files to `~/dotfiles/xdg_config_dir`
- move file/directory structure around from rcm to XDG spec
- remove all references to rcm
- change external installs:
  - tpm submodule / handle installation of that differently
  - similar story for oh-my-zsh
  - is Vundle just tracked in source?


---

This repo follows from the blog post found
[here](https://www.digitalocean.com/community/tutorials/how-to-use-git-to-manage-your-user-configuration-files-on-a-linux-vps).
Managing config files (`.vimrc`, `.bashrc`) can get tricky, especially when
working with various systems. The blog post recommended 3 ways of versioning:
1. Put home directory under version control (seems gross)
2. Add a configuration directory and link files back into `~`
3. Put home directory under version control via configuring `core.worktree`
  * This seems neat, it automatically modifies those files, but it's still
    viewing the entire home directory.

I've [used puppet in the past](https://github.com/michael-christen/dev_configuration),
and while that's useful for actually installing
the various utilities, it can become burdensome to update configurations. This
should be a more lightweight approach.

## Architecture

* Configuration files
* Configuration script: simple script to link the various files / directories
  into the home directory.

### Configuration Files

* Shell:
  * `.profile`
    * This should define all of the custom environment variables for a system,
      so will be left out of this version control system. See
      [this post](https://superuser.com/questions/183845/which-setup-files-should-be-used-for-setting-up-environment-variables-with-bash/183956#183956)
      about it.
  * `.bashrc`
  * `.bash_aliases`
  * `.gitconfig`
  * __Stretch Goal__: Install useful scripts
  * `.tmux.conf`
    * Consider using [TPM](https://github.com/tmux-plugins/tpm) for managing
      tmux plugins.
    * tmux-resurrect / tmux-continuum
* Editor:
  * `.vim/`
    * `.vimrc`
  * `.editorconfig`

## Resources:

### Vim

* [Learning Vim Article](https://medium.com/@peterxjang/how-to-learn-vim-a-four-week-plan-cd8b376a9b85)
that made me reevaluate my configuration setup
* [Vim Directory Structure](http://www.panozzaj.com/blog/2011/09/09/vim-directory-structure/)
* [`.vimrc` setup](https://dougblack.io/words/a-good-vimrc.html)
* [Mastering the Vim Language](https://www.youtube.com/watch?v=wlR5gYd6um0&list=LLR8PzB32EL-ldL7Vo_xPCQg&index=1)

## How to Setup

- You may need to configure your default shell to be `zsh`, to do so run:

```
chsh -s /bin/zsh
```

## How to Update

1. Run `sudo ./install_packages.sh` to install system packages
1. Run `./install.sh` to install files and plugins

### Additional Steps When Updating

#### TMux

1. `tmux source ~/.tmux.conf`
1. `<prefix> + I`


Need to setup your own .rcrc with at least this information:

```
DOTFILES_DIRS="/home/${USER}/${REPO_DIR}/files"
```

TODO:
- [ ] Need to probably manage plugins differently, see https://thoughtbot.com/blog/rcm-for-rc-files-in-dotfiles-repos
- [ ] TMUX submodule plugins may be broken too?
