#!/usr/bin/env python3

from typing import List, Tuple
import subprocess
import os
import shutil
from pathlib import Path

cwd = os.path.dirname(os.path.realpath(__file__))
cwd_path = Path(cwd)
oh_my_zsh_path = Path(os.path.join(Path.home(), '.oh-my-zsh'))

def cloneOrPull(repo_url: str, target_path: Path):
    """
    Clones git repository `repo_url` into `target_path` if it doesn't exist,
    pulls latest changes otherwise.
    """
    if target_path.exists():
        subprocess.run(['git', 'pull'], cwd=target_path)
    else:
        subprocess.run([
            'git',
            'clone',
            repo_url,
            target_path
        ])

def linkFiles(dotfiles: List[Tuple[Path, str]]):
    """
    Creates/updates symlinks to dotfiles
    """
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
    """
    Installs VS Code extensions listed in `vscode/extensions`
    """
    subprocess.run(['zsh', os.path.join(cwd, 'vscode/extensions')])

def installVimPlug():
    """
    Installs Vim plug - Vim plugin manager (https://github.com/junegunn/vim-plug)
    """
    subprocess.run([
        'curl',
        '-fLo',
        os.path.join(Path.home(), '.vim/autoload/plug.vim'),
        '--create-dirs',
        'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
    ])

def installNVM():
    """
    Installs nvm - Node version manager (https://github.com/nvm-sh/nvm)
    """
    subprocess.run([
        'curl',
        '-o-',
        'https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash',
    ])

def installTPM():
    """
    Installs tpm - Tmux plugin manager (https://github.com/tmux-plugins/tpm)
    """
    tpm_path = Path(os.path.join(Path.home(), '.tmux/plugins/tpm'))

    cloneOrPull(repo_url='https://github.com/tmux-plugins/tpm', target_path=tpm_path)

def installZshDraculaTheme():
    """
    Installs dracula theme for ZSH
    """
    theme_path = Path(os.path.join(oh_my_zsh_path, 'custom/themes/zsh'))

    cloneOrPull(repo_url='git@github.com:dracula/zsh.git', target_path=theme_path)

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
    linkFiles([
        (Path(os.path.join(cwd_path, 'zshrc')), '.zshrc'),
        (Path(os.path.join(cwd_path, 'vimrc')), '.vimrc'),
        (Path(os.path.join(cwd_path, 'tmux.conf')), '.tmux.conf'),
        (Path(os.path.join(cwd_path, 'vscode/settings.json')), '.config/Code/User/settings.json'),
        (Path(os.path.join(Path.home(), '.oh-my-zsh/custom/themes/zsh/dracula.zsh-theme')), '.oh-my-zsh/themes/dracula.zsh-theme')
    ])

    print('Installing vscode extensions...')
    installVSCodeExtensions()
