
-- Leader key is spacebar
vim.g.mapleader = " "

-- project view
vim.keymap.set("n", "<leader>pv", vim.cmd.Ex)

-- Allows for movement of visual mode lines, pair with capital V
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

-- Keeps cursor in place when appending line below into current line
vim.keymap.set("n", "J", "mzJ`z")
-- Keeps cursor in the middle while going up and down:
vim.keymap.set("n", "<C-d>", "<C-d>zz")
vim.keymap.set("n", "<C-u>", "<C-u>zz")
-- Keeps cursor in the middle while / searching:
vim.keymap.set("n", "n", "nzzzv")
vim.keymap.set("n", "N", "Nzzzv")

-- Paste over! (without losing current thing!)
vim.keymap.set("x", "<leader>p", "\"_dP")

-- Meant to copy yank into the clipboard, but doesn't seem to work
--vim.keymap.set("n", "<leader>y", "\"+y")
--vim.keymap.set("v", "<leader>y", "\"+y")
--vim.keymap.set("n", "<leader>Y", "\"+Y")

-- Find and replace the word you're on
vim.keymap.set("n","<leader>s",[[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]])

-- Spell check keys
vim.keymap.set("n", "<A-.>", "]s") -- move to next mistake
vim.keymap.set("n", "<A-,>", "[s") -- move to prev mistake
vim.keymap.set("n", "<A-/>", "z=") -- see options to replace word
vim.keymap.set("n", "<A-a>", "zg") -- add the word to dict

-- Window navigation
vim.keymap.set("n", "<leader>h", "<C-w>h")
vim.keymap.set("n", "<leader>j", "<C-w>j")
vim.keymap.set("n", "<leader>k", "<C-w>k")
vim.keymap.set("n", "<leader>l", "<C-w>l")
vim.keymap.set("n", "<leader>c", "<C-w>o")

-- Esc made easy
vim.keymap.set("i", "jj", "<Esc>")
