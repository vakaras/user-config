" Set mapleader
let mapleader = ","
let g:mapleader = ","

" Fast saving
nmap <leader>w :w!<cr>
nmap <leader>f :find<cr>

" Date and time:
iab xdate <c-r>=strftime("%Y-%m-%d")<cr>
iab xtime <c-r>=strftime("%H:%M:%S")<cr>

{% raw %}
augroup MyIMAPs
    au!
    au VimEnter * call IMAP("$t", "{% <++> %}<++>", "")
    au VimEnter * call IMAP("$v", "{{ <++> }}<++>", "")
    au VimEnter * call IMAP("((", "(<++>)<++>", "")
    au VimEnter * call IMAP("[[", "[<++>]<++>", "")
    au VimEnter * call IMAP("{{", "{<++>}<++>", "")
    au VimEnter * call IMAP("\"\"", "\"<++>\"<++>", "")
    au VimEnter * call IMAP("\'\'", "\'<++>\'<++>", "")
augroup END
{% endraw %}

" LaTeX Alt-Key remap.
imap <leader>b <Plug>Tex_MathBF
imap <leader>c <Plug>Tex_MathCal
imap <leader>l <Plug>Tex_LeftRight
imap <leader>i <Plug>Tex_InsertItemOnThisLine

" Copy/paste from global clipboard.
nmap <C-p> "+p
vmap <C-y> "+y

" make
nmap <leader><C-b> :!make<cr>
