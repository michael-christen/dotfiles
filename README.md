# Version Controlled Configuration

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

## Manual Steps for installing

1. May need to install `ag`

## Manual Steps When Updating

### TMux

1. `tmux source ~/.tmux.conf`
1. `<prefix> + I`
