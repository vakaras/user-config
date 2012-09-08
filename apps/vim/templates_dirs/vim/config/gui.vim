"Remove toolbars, scrollbars and menu:
set guioptions-=T
set guioptions-=m
set guioptions-=e
set guioptions-=r
map <silent> <C-F2> :if &guioptions =~# 'T' <Bar>
                         \set guioptions-=T <Bar>
                         \set guioptions-=m <bar>
                    \else <Bar>
                         \set guioptions+=T <Bar>
                         \set guioptions+=m <Bar>
                    \endif<CR>

"Colors:
let psc_style='cool'
colorscheme torte

"Highlights current line:
set cursorline
hi cursorline guibg=#333333
hi CursorColumn guibg=#333333

"Change default font:
set guifont=Monospace\ 9
