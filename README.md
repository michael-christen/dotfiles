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
