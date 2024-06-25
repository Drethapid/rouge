#!/usr/bin/env python3

import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


# define the main screen and set size
def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)
    # ^ set player initial position

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    # ^ assign the tileset to use

    event_handler = EventHandler()

    # initiate terminal and initial screen
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Rougelike",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=player_x, y=player_y, string="@")

            context.present(root_console)

            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if action is None:
                    continue #continue if no action taken

                if isinstance(action, MovementAction): # move the cursor
                    player_x += action.dx
                    player_y += action.dy  

                elif isinstance(action, EscapeAction):
                    raise SystemExit() # close if escape hit


if __name__ == "__main__":
    main()
