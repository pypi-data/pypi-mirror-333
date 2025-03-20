import typing
import readchar
from .. import utils

@utils.ensure('?25h', '0m')
def select(
    prompt: str,
    choices: typing.Iterable,
    max: int | None = 1,
    size: int | None = 10,
    hover: int | str = 36
) -> list | typing.Any:
    '''
    A prompt for selecting item(s) in a list.

    Bindings:
        - up/down: Move cursor
        - space/s: toggle line selection
        - home/end: Go to start/end of list
        - a: Toggle all items
        - shift+s: Toggle from last selection to cursor
        - r: Reset selection
        - enter: Confirm selection
    
    :param prompt: Prompt to display before the menu.
    :param choices: Iterable of choices.
    :param max: Max amount of choices. Set to null for infinite.
    :param size: Display length of the menu. Set to None to display entire menu.
    :param hover: ANSI code to apply when hovering.

    :return: List of choices, or the choice directly if `max` is set to 1.
    '''

    row = 0
    scroll = 0
    sel: list[int] = []
    choices = list(choices) # Convenient for passing iterator directly
    size = size or len(choices)
    last_toggle = -1

    print(prompt)

    def toggle(line: int) -> None:
        # Toggles a line

        if line in sel: sel.remove(line)
        elif not max or len(sel) < max: sel.append(line)
    
    while 1:
        for choice_index, choice in enumerate(choices[scroll:scroll + size]):
            i = scroll + choice_index
            print(f'\x1b[?25l\x1b[0m\x1b[2K{"-+"[i in sel]}\x1b[{hover if i == row else 0}m {choice}\x1b[0m')
        
        print(f'\x1b[{size}A', end = '')
        key = readchar.readkey()

        # Move cursor up
        if key == readchar.key.UP:
            if row > 0: row -= 1
            if row < scroll: scroll -= 1

        # Move cursor down
        if key == readchar.key.DOWN:
            if row < len(choices) - 1: row += 1
            if row >= scroll + size: scroll += 1
        
        # Go to top
        if key == readchar.key.HOME:
            row = scroll = 0
        
        # Go to bottom
        if key == readchar.key.END:
            row = len(choices) - 1
            scroll = row // size
        
        # Toggle line
        if key in (readchar.key.SPACE, 's') and max != 1:
            toggle(row)
            last_toggle = row
        
        # Toggle all lines
        if key == 'a':
            for i in range(len(choices)):
                toggle(i)
        
        # Select plage
        if key == 'S':
            s, e = sorted((last_toggle, row))
            if last_toggle >= row:
                s, e = s - 1, e - 1
            
            for i in range(s, e):
                toggle(i + 1)
        
        # Reset selection
        if key in 'rR':
            sel = []
            last_toggle = -1
        
        # Confirm or direct select
        if key == readchar.key.ENTER:
            if not sel: sel = [row]
            break
    
    sel.sort()
    result = [choices[i] for i in sel]
    return result if max != 1 else result[0]

# EOF