#!/usr/bin/env python3

import subprocess
import os
import shutil
from pathlib import Path

cwd = os.path.dirname(os.path.realpath(__file__))
cwd_path = Path(cwd)

def linkDotfiles():
    dotfiles = map(lambda i: Path(os.path.join(cwd, i)), ['.zshrc', '.vimrc', '.tmux.conf'])
    for p in dotfiles:
        print('linking {0}'.format(p.name))
        fp = Path(os.path.join(Path.home(), p.name))

        if fp.exists() and fp.is_symlink():
            fp.unlink()
        elif fp.exists() and not fp.is_symlink():
            shutil.move(fp, Path(str(p) + '.back'))

        fp.symlink_to(p)

def installVSCodeExtensions():
    subprocess.run(['zsh', os.path.join(cwd, 'vscode/extensions')])

if __name__ == "__main__":
    print('Linking dotfiles...')
    linkDotfiles()

    print('Installing vscode extensions...')
    installVSCodeExtensions()
