{% block syntax_highlight %}
let python_highlight_all = 1
{% endblock %}

{% block pep8 %}
set shiftwidth=4

" Lines of code must be shorter than 79 symbols.
set wrapmargin=79

" Lines of documentation must be shorter than 72 symbols.
"set wrapmargin=72
{% endblock %}

{% block mappings %}
call IMAP("$q", "\'\'\' <++>\<cr>\'\'\'<++>", "python")
call IMAP("$w", "\"\"\" <++>\<cr>\"\"\"<++>", "python")
call IMAP("`f", "def <++>(<++>):\<cr>\"\"\" <++>\<cr>\"\"\"<++>", "python")
call IMAP("`c", "class <++>:\<cr>\"\"\" <++>\<cr>\"\"\"<++>", "python")
call IMAP("`s", "self", "python")
call IMAP("`_", "def __<++>__(<++>):\<cr><++>", "python")

" Comments, fixes, bugs, etc.
call IMAP ("#LT", " # FIXME: LT WORD USED.", "python")

" Imports.
call IMAP ("INTER", ">>> import interlude; interlude.interact(locals())",
      \ "python")
" http://docs.python.org/library/pdb.html#debugger-commands
call IMAP ("PDB", "import pdb; pdb.set_trace()", "python")
call IMAP ("TRACE", "import sys, traceback; traceback.print_exc(file=sys.stdout)", "python")
call IMAP ("ipython", ">>> from chaoflow.testing.ipython import dtipshell; dtipshell(locals())", "python")

{% endblock %}
