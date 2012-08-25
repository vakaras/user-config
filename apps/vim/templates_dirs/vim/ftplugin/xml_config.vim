let g:FTP_DIR = g:VIM_ROOT_DIR . 'ftplugin/'
let g:XML_DIR = g:FTP_DIR . 'xml/'

let xml_jump_string = "<++>"
let xml_use_xhtml = 1

"call Include(g:XML_DIR, 'xml')

call IMAP ("EX", "<example nr=\"<++>\"\<cr>org=\"<++>\"\<cr>tr=\"<++>\" />", "xml")
call IMAP ("WO", "<word id=\"<++>\" value=\"<++>\">\<cr><++>\<cr></word>", "xml")
