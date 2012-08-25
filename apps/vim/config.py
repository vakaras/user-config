{
    'install': {
        'all': [
            'vim',
            'vim-addon-manager',
            'vim-scripts',
            'exuberant-ctags',
            ],
        'install_gui': [
            'vim-gtk',
            ],
        },
    'templates': {
        home('.vimrc'): 'vimrc',
        },
    'templates_dirs': {
        home('.vim'): 'vim',
        },
    'routines': {
        'vimball': (app('.'), 'routines', 'vimball'),
        'latex_suite': (app('.'), 'routines', 'latex_suite'),
        'vim_cmd': (app('.'), 'routines', 'vim_cmd'),
        'nerd_commenter': (app('.'), 'routines', 'nerd_commenter'),
        },
    'exec': [
        {
            'routine': 'nerd_commenter',
            },
        {
            'routine': 'vimball',
            'url': 'http://www.vim.org/scripts/download_script.php?src_id=16854',
            'extension': '.vba.gz',
            },
        {
            'routine': 'vimball',
            'url': 'http://www.vim.org/scripts/download_script.php?src_id=13387',
            'extension': '.vba',
            },
        {
            'routine': 'latex_suite',
            },
        ]
    }
