set runtimepath^=$XDG_CONFIG_HOME/vim runtimepath+=$XDG_CONFIG_HOME/vim/after
let &packpath = &runtimepath
source $XDG_CONFIG_HOME/vim/vimrc
lua require('config')
set background=dark " or light if you want light mode
colorscheme gruvbox
