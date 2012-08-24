" Get current directory:
function! CurDir()
  let home = $HOME . '/'
  let curdir = substitute(getcwd(), home, "~/", "g")
  return curdir
endfunction

" Rewraper.
python << EOF

import textwrap
import re

def clean(level):
    return level.replace('+', ' ').replace('-', ' ').replace('*', ' ')

def rewrap(lines):
    blocks = []
    level = None
    block = []
    for line in lines:
        #match = re.match(r'^((>+ )*)(.*)$', line)
        match = re.match(r'^((>+ )+)(.*)$', line)
        if match is None:
            match = re.match(r'^([ ]*([+\-*])?[ ]*)(.*)$', line)
        if match is None:
            matched_level = ''
            matched_text = line
        else:
            matched_level, t, matched_text = match.groups()
            #print 'mlevel: "%s"'%matched_level
        if level is None:
            #print 'veikia 3'
            level = matched_level
        elif '>' in matched_level and level != matched_level:
            #print 'veikia 2'
            blocks.append((level, ' '.join(block)))
            block = []
            level = matched_level
        elif matched_level != clean(level):
            #print 'veikia 1'
            blocks.append((level, ' '.join(block)))
            block = []
            level = matched_level
        #print 'veikia'
        block.append(matched_text)
    blocks.append((level, ' '.join(block)))

    lines = []
    for level, text in blocks:
        for i, line in enumerate(
                textwrap.wrap(text, width=(72 - len(level)))):
            if ('+' in level or '-' in level or '*' in level) and i > 0:
                lines.append(clean(level) + line)
                #print 'veikia 4'
            else:
                lines.append(level + line)
                #print 'veikia 5 "%s"'%line
    return lines

EOF

function! ReWrap() range
python << EOF

import vim
from vim import current

start = int(vim.eval('a:firstline')) - 1
end = int(vim.eval('a:lastline'))
buf = current.buffer


lines = []
for i in range(start, end):
    lines.append(current.buffer[i])
lines = rewrap(lines)

buf[start:end] = lines

EOF
endfunction

vmap <C-w> :call ReWrap()<cr>
