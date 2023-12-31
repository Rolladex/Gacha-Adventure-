# -*- coding: utf-8 -*-
"""
 ▄▄▄      ▄▄▄▄    ██████▄▄▄█████▓██▀███  ▄▄▄      ▄████▄ ▄▄▄█████▓
▒████▄   ▓█████▄▒██    ▒▓  ██▒ ▓▓██ ▒ ██▒████▄   ▒██▀ ▀█ ▓  ██▒ ▓▒
▒██  ▀█▄ ▒██▒ ▄█░ ▓██▄  ▒ ▓██░ ▒▓██ ░▄█ ▒██  ▀█▄ ▒▓█    ▄▒ ▓██░ ▒░
░██▄▄▄▄██▒██░█▀   ▒   ██░ ▓██▓ ░▒██▀▀█▄ ░██▄▄▄▄██▒▓▓▄ ▄██░ ▓██▓ ░ 
 ▓█   ▓██░▓█  ▀█▒██████▒▒ ▒██▒ ░░██▓ ▒██▒▓█   ▓██▒ ▓███▀ ░ ▒██▒ ░ 
 ▒▒   ▓▒█░▒▓███▀▒ ▒▓▒ ▒ ░ ▒ ░░  ░ ▒▓ ░▒▓░▒▒   ▓▒█░ ░▒ ▒  ░ ▒ ░░   
  ▒   ▒▒ ▒░▒   ░░ ░▒  ░ ░   ░     ░▒ ░ ▒░ ▒   ▒▒ ░ ░  ▒      ░    
  ░   ▒   ░    ░░  ░  ░   ░       ░░   ░  ░   ▒  ░         ░      
      ░  ░░           ░            ░          ░  ░ ░              
               ░                                 ░                
             ▄▄▄▄   ██▓███ ▓█████ ██░ ██▄▄▄█████▓                 
            ▓█████▄▓██░  ██▓█   ▀▓██░ ██▓  ██▒ ▓▒                 
            ▒██▒ ▄█▓██░ ██▓▒███  ▒██▀▀██▒ ▓██░ ▒░                 
            ▒██░█▀ ▒██▄█▓▒ ▒▓█  ▄░▓█ ░██░ ▓██▓ ░                  
            ░▓█  ▀█▒██▒ ░  ░▒████░▓█▒░██▓ ▒██▒ ░                  
            ░▒▓███▀▒▓▒░ ░  ░░ ▒░ ░▒ ░░▒░▒ ▒ ░░                    
"""
import random
# import json
# import re
# import pyfiglet


class Player:
    def __init__(self):
        self.mining_tool_durability = 10  # ??? inventory store items
        self.position = (0, 0)
        self.good_gatcha = []
        self.bad_gatcha = []
        self.statistics = {
          "money": 100,
          "life": 100,
          "times_died": 0,
          "monsters_slain": 0,
          "collected_gatcha": 0
        }

        # Dictionary to map directions to their corresponding walls
        self._direction_walls = {
            "left": "left",
            "right": "right",
            "up": "top",
            "down": "bottom"
        }

    def mine(self, direction, maze):
        if self.mining_tool_durability <= 0:
            print("Your mining tool is broken! You can't mine anymore.")
            return

        x, y = self.position

        if not direction:  # If no direction is provided
            valid_directions = []

            for d, wall in self._direction_walls.items():
                if maze._grid[x][y].walls[wall]:
                    valid_directions.append(d)

            if not valid_directions:
                print("No valid directions to mine from the current position.")
                return

            direction = random.choice(valid_directions)

        wall = self._direction_walls.get(direction)

        if wall and maze._grid[x][y].walls[wall]:
            coins_earned = random.randint(5, 15)
            self.statistics["money"] += coins_earned
            self.mining_tool_durability -= 1
            print(f"Mined the {direction} wall and earned {coins_earned} coins!")
        else:
            print(f"Cannot mine {direction} from the current position.")

    def get_stat(self, stat):
        return self.statistics[stat]

    def add_gatcha(self, gatcha_item):  # ???
        if gatcha_item.is_good:
            self.good_gatcha.append(gatcha_item)
        else:
            self.bad_gatcha.append(gatcha_item)

    def last_gatcha(self, good):  # ???
        if good:
            return self.good_gatcha[-1]
        else:
            return self.bad_gatcha[-1] if self.bad_gatcha else None


class Gatcha:
    def __init__(self, name, ascii_art, is_good=True):
        self.name = name
        self.ascii_art = ascii_art
        self.is_good = is_good  # Determines if it's a reward or punishment

    def display(self):
        print(self.ascii_art)


RARITY_RATE = 1
RARITY_COUNT = 8


class GatchaFactory:

    def __init__(self):
        # we create Gacha here.
        self.rarity_prefix = [        # Poe?
            "bad", "okay",            # 0, 1 - name
            "good", "great",          # 2, 3 - prefix + name
            "epic", "legendary",      # 4, 5 - prefix + name + suffix
            "mythical", "galaxy"      # 6, 7 - prefix + name + suffix + postfix
        ]
        self.context_linkers = [
            "the", "and", "or", "not", "then",
            "of", "of the", "chased", "collected",
            "open", "quotent of", "their", "intrinsic"
        ]
        self.prefix_name = [
            "degenerated", "edgy", "mediocre", "shambly",
            "bulleted", "gooey", "solid", "metallic"
        ]

        self.name = [
            "chicken", "bacon", "taco", "bagel",
            "toast", "can", "gnome", "shirt",
            "armored armor of armor", "wd40", "marios hat"
        ]
        self.suffix_name = [
            "paladin", "determination", "dragon",
            "eagle", "wolf", "turkey"
        ]
        self.postfix = [
            "the gods", "of determination",
            "of paladin", "of the whales",
        ]

    def pull_gacha(self):
        result = self.gacha.pull()
        self.coins -= 10
        self.coins_spent_without_rare += 10
        # Check the rarity of the pulled character
        if result.rarity in ["epic", "legendary", "mythical", "galaxy"]:
            self.coins_spent_without_rare = 0  # Reset counter

        return result

    def reward_formula(self, gatchaCount: int):  # ??? Elaborate How, What?
        # TODO: Implement logic
        pass

    def create_random(self, gatchaCount: int):  # ??? Elaborate How, What?
        # TODO: Implement logic to create random Gatcha
        pass


class DeckCards:  # TODO: Add card games.
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    VALUES = ['2', '3', '4', '5',
              '6', '7', '8', '9', '10',
              'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        return self.VALUES.index(self.value) < self.VALUES.index(other.value)

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return f"{self.value} of {self.suit}"


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}


class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self._grid = [[Cell(x, y) for y in range(rows)] for x in range(cols)]
        self.generate_maze(self._grid[0][0])

    def generate_maze(self, cell):
        cell.visited = True
        neighbours = self._get_unvisited_neighbours(cell)

        while neighbours:
            direction, next_cell = random.choice(neighbours)

            if direction == "top":
                cell.walls["top"] = False
                next_cell.walls["bottom"] = False
            elif direction == "right":
                cell.walls["right"] = False
                next_cell.walls["left"] = False
            elif direction == "bottom":
                cell.walls["bottom"] = False
                next_cell.walls["top"] = False
            elif direction == "left":
                cell.walls["left"] = False
                next_cell.walls["right"] = False

            self.generate_maze(next_cell)
            neighbours = self._get_unvisited_neighbours(cell)

    def _get_unvisited_neighbours(self, cell):
        neighbours = []
        x, y = cell.x, cell.y

        if y > 0 and not self._grid[x][y - 1].visited:
            neighbours.append(("top", self._grid[x][y - 1]))
        if x < self.cols - 1 and not self._grid[x + 1][y].visited:
            neighbours.append(("right", self._grid[x + 1][y]))
        if y < self.rows - 1 and not self._grid[x][y + 1].visited:
            neighbours.append(("bottom", self._grid[x][y + 1]))
        if x > 0 and not self._grid[x - 1][y].visited:
            neighbours.append(("left", self._grid[x - 1][y]))

        return neighbours


class Game:
    def __init__(self):
        self.player = Player()
        self.maze = Maze(10, 10)  # 10x10 maze for simplicity
        self.current_location = "start"
        self.action_handlers = {
            "go": self.move,
            "walk": self.move,
            "mine": self.player.mine
        }

        # Shorthand for directions
        self.direction_shorthand = {
            "w": "up",
            "s": "down",
            "a": "left",
            "d": "right",
            "m": "mine"
        }

    def play(self):
        print("Welcome to the game!")
        print("Commands: go [direction], mine [direction], quit")
        action = input("Enter your action: ")
        sanitized_action = self.sanitize_input(action)
        self.parse_action(sanitized_action)
        while True:
            self.display()
            action = input("Enter your action: ").lower()
            if action == "quit":
                print("Thanks for playing!")
                break
            self.parse_action(action)

    def display(self):
        # draws the full display
        print(f"Current Location: {self.current_location}")
        print(f"Life: {self.player.get_stat('life')}")
        print(f"Money: {self.player.get_stat('money')}")
        # Display the player's position in the maze
        for y in range(self.maze.rows):
            for x in range(self.maze.cols):
                cell = self.maze._grid[x][y]

                # Check for the left wall of the cell
                if cell.walls["left"]:
                    print("██", end="")
                else:
                    print("  ", end="")

                if (x, y) == self.player.position:
                    print("PP", end="")
                elif cell.walls["top"]:
                    print("██", end="")
                else:
                    print("  ", end="")
            print()

    def sanitize_input(self, action):
        # Strip leading and trailing whitespaces
        sanitized_action = action.strip()

        # Convert to lowercase for consistency
        sanitized_action = sanitized_action.lower()

        # Remove any characters not allowed (for this example, we'll just allow alphanumeric characters and spaces)
        sanitized_action = ''.join(char for char in sanitized_action if char.isalnum() or char.isspace())

        return sanitized_action

    def parse_action(self, action):
        sanitized_action = self.sanitize_input(action)

        split_action = sanitized_action.split()
        # Filter out empty strings from the split result
        valid_parts = [part for part in split_action if part]

        # If there are no valid parts, return with a message
        if not valid_parts:
            print("No valid action entered. Please enter a valid command.")
            return

        command, *args = valid_parts

        # Mapping shorthand commands to their full versions
        shorthand_commands = {
            'w': 'up',
            's': 'down',
            'a': 'left',
            'd': 'right',
            'm': 'mine'
        }

        # Split the user action into command and arguments
        command, *args = sanitized_action.split()

        # Check if the command is a shorthand and replace it
        if command in shorthand_commands:
            if command == 'm':  # If the command is 'mine'
                command = shorthand_commands[command]
            else:  # If the command is a movement direction
                args = [shorthand_commands[command]]
                command = 'go'  # Prepend the 'go' command
        else:
            command = shorthand_commands.get(command, command)

        # Check if the command is in our action handlers
        if command in self.action_handlers:
            # Provide feedback and execute the action
            print(f"Executing {command} command...")
            if command == "mine":
                if len(args) == 0:  # No direction provided
                    self.action_handlers[command](None, self.maze)  # pass None as direction and maze instance
                else:
                    self.action_handlers[command](*args, self.maze)  # pass the direction and maze instance
            else:
                self.action_handlers[command](*args)
        else:
            # Dynamic feedback for unrecognized commands
            similar_commands = [cmd for cmd in self.action_handlers if cmd.startswith(command)]
            if similar_commands:
                print(f"Did you mean {', '.join(similar_commands)}?")
            else:
                print("Invalid action. Try commands like 'go left', 'mine', etc.")

    def move(self, direction):
        x, y = self.player.position
        wall_direction = self.player._direction_walls[direction]

        if direction == "left" and not self.maze._grid[x][y].walls[wall_direction]:
            self.player.position = (x-1, y)
        elif direction == "right" and not self.maze._grid[x][y].walls[wall_direction]:
            self.player.position = (x+1, y)
        elif direction == "up" and not self.maze._grid[x][y].walls[wall_direction]:
            self.player.position = (x, y-1)
        elif direction == "down" and not self.maze._grid[x][y].walls[wall_direction]:
            self.player.position = (x, y+1)
        else:
            print(f"🚧 Cannot move {direction} from position {self.player.position}. There's a wall!")
            return  # Return early if the player can't move in the specified direction

        print(f"🚶 Moved {direction} to position {self.player.position}")
        x, y = self.player.position
        self.current_location = f"({x}, {y}) in the maze"


if __name__ == "__main__":
    game = Game()
    game.play()
