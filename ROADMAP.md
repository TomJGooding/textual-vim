# Roadmap

## Features

- [x] Insert Mode
- [ ] Normal Mode
- [ ] Number Prefixes
- [ ] Visual Mode
- [ ] Undo/Redo
- [ ] Visual Line Mode

## Insert mode keys

- [x] `<Esc>` - end Insert mode, back to Normal mode
- [x] `cursor keys` - move left/right/up/down
- [ ] `shift-left/right` - one word left/right
- [x] `<End>` - end the line
- [x] `<Home>` - start of line

## Left-right motions

- [x] `h` - left
- [x] `l` - right
- [x] `0` - first char of the line
- [x] `^` - first non-blank char of the line
- [x] `$` - end of line
- [ ] `f{char}` - occurrence of char to the right
- [ ] `F{char}` - occurrence of char to the left
- [ ] `t{char}` - before occurrence of char to the right
- [ ] `T{char}` - before occurrence of char to the left
- [ ] `;` - repeat the last `f`, `F`, `t`, or `T`
- [ ] `,` - repeat the last `f`, `F`, `t`, or `T` in opposite direction

## Up-down motions

- [x] `k` - up
- [x] `j` - down
- [ ] `G` - last line
- [ ] `gg` - first line

## Text object motions

- [ ] `w` - word forward
- [ ] `W` - blank-separated WORD forward
- [ ] `e` - forward to the end of the word
- [ ] `E` - forward to the end of the blank-separated WORD
- [ ] `b` - word backward
- [ ] `B` - blank-separated WORD backward

## Inserting text

- [x] `a` - append text after the cursor
- [ ] `A` - append text at the end of the line
- [x] `i` - insert text before the cursor
- [ ] `I` - insert text before the first non-blank in the line
- [ ] `o` - open a new line below the current line, append text
- [ ] `O` - open a new line above the current line, append text

## Deleting text

- [ ] `x` - delete under the cursor
- [ ] `X` - delete before the cursor
- [ ] `dd` - delete lines
- [ ] `D` - delete to the end of the line
- [ ] `d{motion}` - delete the text that is moved over with motion

## Copying and moving text

- [ ] `yy` - yank (copy) lines
- [ ] `y{motion}` - yank the text that is moved over with motion
- [ ] `p` - put (paste) after the cursor position
- [ ] `P` - put (paste) before the cursor position

## Changing text

- [ ] `r{char}`- replace with {char}
- [ ] `c{motion}` - change the text that is moved over with motion
- [ ] `cc` - change lines
- [ ] `C` - change to the end of the line
