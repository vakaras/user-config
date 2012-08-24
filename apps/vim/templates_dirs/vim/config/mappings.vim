" Set mapleader
let mapleader = ","
let g:mapleader = ","

" Fast saving
nmap <leader>w :w!<cr>
nmap <leader>f :find<cr>

" Date and time:
iab xdate <c-r>=strftime("%Y-%m-%d")<cr>
iab xtime <c-r>=strftime("%H:%M:%S")<cr>

" Default auto complete for (, [, {, ", '
inoremap $1 ()<++><esc>:let leavechar=")"<cr>4hi
inoremap $2 []<++><esc>:let leavechar="]"<cr>4hi
inoremap $4 {<esc>o}<esc>o<++><esc>k>>:let leavechar="}"<cr>O
inoremap $3 {}<++><esc>:let leavechar="}"<cr>4hi
inoremap $q ''<++><esc>:let leavechar="'"<cr>4hi
inoremap $w ""<++><esc>:let leavechar='"'<cr>4hi

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
