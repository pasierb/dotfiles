set encoding=utf-8

" line numbering
set number
set numberwidth=5

set noswapfile

" Softtabs, 2 spaces
set tabstop=2
set shiftwidth=2
set shiftround
set expandtab

" display extra whitespaces
set list listchars=tab:»·,trail:·,nbsp:·


"
" Plugins!
" Make sure you use single quotes
"

call plug#begin('~/.vim/plugged')

Plug 'preservim/nerdtree'
Plug 'dracula/vim', { 'as': 'dracula' }
Plug 'junegunn/fzf'
Plug 'junegunn/fzf.vim'
Plug 'leafgarland/typescript-vim'

call plug#end()

colorscheme dracula

map ; :Files<CR>

let NERDTreeShowHidden=1

