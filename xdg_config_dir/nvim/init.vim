set runtimepath^=$XDG_CONFIG_HOME/vim runtimepath+=$XDG_CONFIG_HOME/vim/after
let &packpath = &runtimepath
source $XDG_CONFIG_HOME/vim/vimrc
lua require('config')
set background=dark " or light if you want light mode
colorscheme gruvbox

" Function to sort lines while keeping comments attached
function! SortLinesWithComments()
  " Define a pattern to match comment lines
  let comment_pattern = '^\s*#'

  " Get the range of lines to sort
  let start_line = line("'<")
  let end_line = line("'>")

  " Collect lines and their comments
  let lines = []
  let temp_lines = []

  for lnum in range(start_line, end_line)
    let line = getline(lnum)
    if line =~ comment_pattern
      " It's a comment line, save it separately
      call add(temp_lines, line)
    else
      " It's a code line, add it to the main list along with accumulated comments
      call extend(temp_lines, [line])
      call add(lines, join(temp_lines, "\n"))
      let temp_lines = []
    endif
  endfor

  " If there are any remaining comments, add them as well
  if !empty(temp_lines)
    call add(lines, join(temp_lines, "\n"))
  endif

  " Sort the lines
  call sort(lines)

  " Replace the lines in the buffer
  let lnum = start_line
  for line in lines
    let splitted_lines = split(line, "\n")
    for split_line in splitted_lines
      call setline(lnum, split_line)
      let lnum += 1
    endfor
  endfor

  " Clear remaining lines
  while lnum <= end_line
    call setline(lnum, '')
    let lnum += 1
  endwhile
endfunction

" Map the function to a key combination in visual mode
vnoremap <silent> <leader>s :<C-U>call SortLinesWithComments()<CR>
