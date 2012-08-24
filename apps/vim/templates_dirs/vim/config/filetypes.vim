let g:tex_flavor='latex'

augroup filetypedetect
  au! BufRead,BufNewFile /tmp/bash* setfiletype sh
  au! BufRead,BufNewFile *.sage,*.spyx,*.pyx setfiletype python
  au! BufRead,BufNewFile *.zcml setfiletype xml
  au! BufRead,BufNewFile *.mw setfiletype flexwiki
  au! BufRead,BufNewFile *.txt setfiletype rst
  au! BufRead,BufNewFile *.dict setfiletype dict
  au! BufRead,BufNewFile *.json setfiletype json
  au! BufRead,BufNewFile *.mem setfiletype xml
  au! BufRead,BufNewFile *.scala setfiletype scala
augroup END
