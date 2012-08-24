" Always show the statusline
set laststatus=2

" Format the statusline:
:set statusline=%F%m%r%h%w\ [FORMAT=%{&ff}]\ [TYPE=%Y]\ [ASCII=\%03.3b]\ [HEX=\%02.2B]\ Line:\ %l/%L:%c
