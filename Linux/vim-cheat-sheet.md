# Vim Cheat Sheet

## Normal Mode Commands

| **Command** | **Description**                        |
| ----------- | -------------------------------------- |
| `h`         | Move left                              |
| `l`         | Move right                             |
| `j`         | Move down                              |
| `k`         | Move up                                |
| `0`         | Move to the beginning of the line      |
| `$`         | Move to the end of the line            |
| `^`         | Move to the first non-blank character  |
| `w`         | Jump to the start of the next word     |
| `b`         | Jump to the start of the previous word |
| `gg`        | Move to the beginning of the file      |
| `G`         | Move to the end of the file            |
| `yy` or `Y` | Yank (copy) the current line           |
| `dd`        | Delete the current line                |
| `dw`        | Delete from the cursor to the end of the current word |
| `dG`        | Delete from the cursor to the end of the file |
| `p`         | Paste after the cursor                 |
| `u`         | Undo the last change                   |
| `Ctrl+r`    | Redo the undone change                 |
| `/text`     | Search for 'text'                      |
| `?text`     | Search for 'text' backward             |
| `n`         | Repeat the last search forward         |
| `N`         | Repeat the last search backward        |
| `:w`        | Save the file                          |
| `:q`        | Quit Vim                               |
| `:wq`       | Save and quit                          |
| `:x`        | Save and quit                          |
| `:q!`       | Quit without saving changes            |
| `:set number`| Show line numbers                      |
| `:set nonumber`| Hide line numbers                   |
| `:%s/old/new/g`| Replace all occurrences of 'old' with 'new' |
| `:number`   | Jump to the specified line number      |
| `:r filename`| Read the content of a file and insert it below the cursor |
| `:e! filename`| Reload the specified file, discarding any unsaved changes |
| `Ctrl+g`    | Show file information and cursor position |

## Insert Mode Commands

| **Command** | **Description**                                |
| ----------- | ---------------------------------------------- |
| `i`         | Enter insert mode before the cursor            |
| `I`         | Enter insert mode at the beginning of the line |
| `a`         | Enter insert mode after the cursor             |
| `A`         | Enter insert mode at the end of the line       |
| `o`         | Insert a new line below the current line       |
| `O`         | Insert a new line above the current line       |
| `Ctrl+h`    | Delete the character before the cursor         |
| `Ctrl+w`    | Delete the word before the cursor              |
| `Esc`       | Exit insert mode                               |

## Visual Mode Commands

| **Command** | **Description**                   |
| ----------- | --------------------------------- |
| `v`         | Enter visual mode                 |
| `V`         | Enter visual line mode            |
| `Ctrl+v`    | Enter visual block mode           |
| `y`         | Yank (copy) the selected text     |
| `d`         | Delete the selected text          |
| `>`         | Indent the selected text          |
| `<`         | Un-indent the selected text       |
| `~`         | Toggle case for the selected text |
| `Esc`       | Exit visual mode                  |
