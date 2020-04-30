#!/usr/bin/env python3

import subprocess
import os
import shutil
from pathlib import Path

cwd = os.path.dirname(os.path.realpath(__file__))
cwd_path = Path(cwd)

def linkDotfiles():
    dotfiles = [
        (Path(os.path.join(cwd_path, 'zshrc')), '.zshrc'),
        (Path(os.path.join(cwd_path, 'vimrc')), '.vimrc'),
        (Path(os.path.join(cwd_path, 'tmux.conf')), '.tmux.conf'),
        (Path(os.path.join(cwd_path, 'vscode/settings.json')), '.config/Code/User/settings.json'),
        (Path(os.path.join(Path.home(), '.oh-my-zsh/custom/themes/zsh/dracula.zsh-theme')), '.oh-my-zsh/themes/dracula.zsh-theme')
    ]

    for it in dotfiles:
        src = it[0]
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

def installTPM():
    tpm_path = Path(os.path.join(Path.home(), '.tmux/plugins/tpm'))

    if tpm_path.exists():
        subprocess.run(['git', 'pull'], cwd=tpm_path)
    else:
        subprocess.run([
            'git',
            'clone',
            'https://github.com/tmux-plugins/tpm',
            tpm_path
        ])

def installZshDraculaTheme():
    oh_my_zsh_path = Path(os.path.join(Path.home(), '.oh-my-zsh'))
    theme_path = Path(os.path.join(oh_my_zsh_path, 'custom/themes/zsh'))

    if theme_path.exists():
        subprocess.run(['git', 'pull'], cwd=theme_path)
    else:
        subprocess.run([
            'git',
            'clone',
            'git@github.com:dracula/zsh.git',
            theme_path
        ])

if __name__ == "__main__":
    print('Installing nvm...')
    installNVM()

    print('Installing vim-plug...')
    installVimPlug()

    print('Installing tpm...')
    installTPM()

    print('Installing zsh dracula theme')
    installZshDraculaTheme()

    print('Linking dotfiles...')
    linkDotfiles()

    print('Installing vscode extensions...')
    installVSCodeExtensions()
