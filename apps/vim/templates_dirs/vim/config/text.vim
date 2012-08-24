set expandtab
set shiftwidth=2
set tabstop=2

set smarttab
set lbr
set tw=500

"Auto indent
set ai

"Smart indet
set si

"C-style indeting
set cindent

"Wrap lines
set wrap
set wrapmargin=79

"Remember last edited line
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif
