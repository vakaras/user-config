" Global variables:
let g:VIM_ROOT_DIR = $HOME . '/.vim/'
let g:VIM_CONFIG_DIR = g:VIM_ROOT_DIR . 'config/'
let g:CURRENT_DIR = g:VIM_ROOT_DIR

function Include(directory, file)
  let l:tmp_dir = g:CURRENT_DIR
  let g:CURRENT_DIR = a:directory
  exec ":source " . a:directory . a:file . ".vim"
  let g:CURRENT_DIR = l:tmp_dir
endfunction

function IncludePy(directory, file)
  let l:tmp_dir = g:CURRENT_DIR
  let g:CURRENT_DIR = a:directory
  exec ":pyfile " . a:directory . a:file . ".py"
  let g:CURRENT_DIR = l:tmp_dir
endfunction

" Include predefined functions:
call Include(g:VIM_CONFIG_DIR, 'functions')

"Get out of VI's compatible mode:
function MySys()
  return "linux"
endfunction
set nocompatible

"Sets how many lines of history VIM has to remember
set history=400

"Enable filetype plugin
filetype plugin on
filetype indent on

"Set to auto read when a file is changed from the outside
set autoread

"Have the mouse enabled all the time:
set mouse=a

" Mappings:
call Include(g:VIM_CONFIG_DIR, 'mappings')

" Colors and Fonts:
call Include(g:VIM_CONFIG_DIR, 'style')

" GUI options:
if has("gui_running")
  call Include(g:VIM_CONFIG_DIR, 'gui')
endif

autocmd BufEnter * :syntax sync fromstart

" File formats:
call Include(g:VIM_CONFIG_DIR, 'fileformats')

" User interface:
call Include(g:VIM_CONFIG_DIR, 'ui')

" Status line:
call Include(g:VIM_CONFIG_DIR, 'status_line')

" Search options:
call Include(g:VIM_CONFIG_DIR, 'search')

" Buffers:
call Include(g:VIM_CONFIG_DIR, 'backup')

" Folding:
call Include(g:VIM_CONFIG_DIR, 'folding')

" Text:
call Include(g:VIM_CONFIG_DIR, 'text')

" Calling other programs:
call Include(g:VIM_CONFIG_DIR, 'programs')

" Define new file types:
call Include(g:VIM_CONFIG_DIR, 'filetypes')

" Spell check:
call Include(g:VIM_CONFIG_DIR, 'spell')

" Tag list:
call Include(g:VIM_CONFIG_DIR, 'taglist')
