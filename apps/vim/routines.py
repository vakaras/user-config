import subprocess
import os
import glob
import shutil


sh = lambda cmd: subprocess.call(cmd, shell=True)


def vimball(ctx, url, extension='.vba', **kwargs):
    sh('wget "{0}" -O /tmp/vimball{1}'.format(url, extension))
    sh('vim -c \'so % | q\' /tmp/vimball.vba')


def vim_cmd(ctx, cmd, **kwargs):
    sh('vim -c \'{0}\''.format(cmd))


def nerd_commenter(ctx, **kwargs):
    url = 'http://www.vim.org/scripts/download_script.php?src_id=14455'
    archive = '/tmp/vim-nerdcommenter.zip'
    sh('wget "{0}" -O {1}'.format(url, archive))
    os.makedirs('/tmp/vim', exist_ok=True)
    sh('unzip {0} -d /tmp/vim'.format(archive))
    dst = os.path.join(ctx.env.HOME_DIR, '.vim/plugin')
    os.makedirs(dst, 0o777, True)
    shutil.copy2('/tmp/vim/plugin/NERD_commenter.vim', dst)


def latex_suite(ctx, **kwargs):
    url = (
            'http://sourceforge.net/projects/vim-latex/files/'
            'snapshots/vim-latex-1.8.23-20120125.768-git8b62284.tar.gz/'
            'download')
    archive = '/tmp/vim-latex.tar.gz'
    sh('wget "{0}" -O {1}'.format(url, archive))
    os.makedirs('/tmp/vim', exist_ok=True)
    sh('tar --extract --file={0} --directory=/tmp/vim'.format(archive))
    path = glob.glob('/tmp/vim/vim-latex*/')[0]
    def copy(src, dst):
        print(src, dst)
        for file_name in os.listdir(src):
            new_src = os.path.join(src, file_name)
            new_dst = os.path.join(dst, file_name)
            if os.path.isdir(new_src):
                copy(new_src, new_dst)
            else:
                os.makedirs(dst, 0o777, True)
                shutil.copy2(new_src, new_dst)
    for directory in os.listdir(path):
        if directory in (
                'latextags', 'ltags', 'Makefile', 'Makefile.in',
                '.gitignore'):
            continue
        else:
            copy(
                    os.path.join(path, directory),
                    os.path.join(ctx.env.HOME_DIR, '.vim', directory))
