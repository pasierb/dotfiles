#!/usr/bin/env python3

import subprocess
import os
import shutil
from pathlib import Path

cwd = os.path.dirname(os.path.realpath(__file__))
cwd_path = Path(cwd)

def linkDotfiles():
    dotfiles = [
        ('zshrc', '.zshrc'),
        ('vimrc', '.vimrc'),
        ('tmux.conf', '.tmux.conf'),
        ('vscode/settings.json', '.config/Code/User/settings.json')
    ]

    for it in dotfiles:
        src = Path(os.path.join(cwd_path, it[0]))
        dest = Path(os.path.join(Path.home(), it[1]))

        print('linking {0}'.format(dest.name))

        if dest.exists() and dest.is_symlink():
            print('{0}: symlink exist, unlinking'.format(str(dest)))
            dest.unlink()

        if dest.exists() and not dest.is_symlink():
            print('{0}: file exist, backing up'.format(str(dest)))
            shutil.move(dest, Path(str(dest) + '.back'))

        dest.symlink_to(src)

def installVSCodeExtensions():
    subprocess.run(['zsh', os.path.join(cwd, 'vscode/extensions')])

def installVimPlug():
    subprocess.run([
        'curl',
        '-fLo',
        os.path.join(Path.home(), '.vim/autoload/plug.vim'),
        '--create-dirs',
        'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
    ])

def installNVM():
    subprocess.run([
        'curl',
        '-o-',
        'https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh',
        '|',
        'bash'
    ])

if __name__ == "__main__":
    print('Installing nvm...')
    installNVM()

    print('Installing vim-plug...')
    installVimPlug()

    print('Linking dotfiles...')
    linkDotfiles()

    print('Installing vscode extensions...')
    installVSCodeExtensions()
