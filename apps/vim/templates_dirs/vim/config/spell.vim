set nospell
let g:check_spell=0

function! ChangeSpellCheck()
if g:check_spell==1
  set nospell
  let g:check_spell=0
else
  set spell
  let g:check_spell=1
endif
endfunction

map <leader>c :call ChangeSpellCheck()<cr>

set spelllang=lt,en
