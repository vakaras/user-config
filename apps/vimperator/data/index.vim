set gui=none
set editor="gvim -f -c 'set ft=mail' -c 'call ChangeSpellCheck()'"

" Search engine:
set defsearch=duck

" Mappings
nnoremap ,t :tabmove 
nnoremap s :panorama switch 
nnoremap a :set gui=none<cr>
nnoremap ,a :set gui=all<cr>
