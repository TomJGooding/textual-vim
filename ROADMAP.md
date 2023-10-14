# Roadmap

## Features

- [ ] Insert Mode
- [ ] Normal Mode
- [ ] Number Prefixes
- [ ] Visual Mode
- [ ] Undo/Redo
- [ ] Visual Line Mode

## Left-right motions

- [ ] `h` - left
- [ ] `l` - right
- [ ] `0` - first char of the line
- [ ] `^` - first non-blank char of the line
- [ ] `$` - end of line
- [ ] `f{char}` - occurrence of char to the right
- [ ] `F{char}` - occurrence of char to the left
- [ ] `t{char}` - before occurrence of char to the right
- [ ] `T{char}` - before occurrence of char to the left
- [ ] `;` - repeat the last `f`, `F`, `t`, or `T`
- [ ] `,` - repeat the last `f`, `F`, `t`, or `T` in opposite direction

## Up-down motions

- [ ] `k` - up
- [ ] `j` - down
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

- [ ] `a` - append text after the cursor
- [ ] `A` - append text at the end of the line
- [ ] `i` - insert text before the cursor
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