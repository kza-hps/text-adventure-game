# Import necessary libraries
import openai
import random
import os

# Set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connected_rooms = {}
        self.items = []

    def connect_room(self, direction, room):
        self.connected_rooms[direction] = room

    def add_item(self, item):
        self.items.append(item)

class Player:
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.inventory = []
        self.health = 100 # added a health attribute for the player

    def move(self, direction):
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
        else:
            print("You can't go that way.")

    def interact(self, item_name, action):
        item = next((i for i in self.current_room.items if i.name == item_name), None)
        if item:
            item.interact(action, self)
        else:
            print("That item doesn't exist in this room.")

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def interact(self, action, player):
        if action == "pick up":
            player.inventory.append(self)
            player.current_room.items.remove(self)
            print(f"You picked up {self.name}.")
        elif action == "drop":
            if self in player.inventory:
                player.inventory.remove(self)
                player.current_room.items.append(self)
                print(f"You dropped {self.name}.")
            else:
                print("You don't have that item.")
        elif action == "use":
            if self in player.inventory:
                # use GPT-3 to generate outcomes and consequences for using the object
                prompt = f"You use {self.name}. What happens?"
                outcome = generate_response(prompt)
                print(outcome)
                # update the game state based on the outcome
                if "damage" in outcome.lower():
                    # assume the outcome contains the amount of damage
                    damage = int(outcome.split()[-1])
                    player.health -= damage
                    print(f"You lost {damage} health. Your current health is {player.health}.")
                    if player.health <= 0:
                        print("You died. Game over.")
                        exit()
                elif "heal" in outcome.lower():
                    # assume the outcome contains the amount of healing
                    heal = int(outcome.split()[-1])
                    player.health += heal
                    print(f"You gained {heal} health. Your current health is {player.health}.")
                elif "unlock" in outcome.lower():
                    # assume the outcome contains the direction of the unlocked room
                    direction = outcome.split()[-1]
                    # assume there is a locked room in that direction
                    locked_room = player.current_room.connected_rooms[direction]
                    # assume there is a key item in the player's inventory
                    key = next((i for i in player.inventory if i.name == "key"), None)
                    if key:
                        # remove the key from the inventory and unlock the room
                        player.inventory.remove(key)
                        locked_room.locked = False
                        print(f"You unlocked the {direction} door with the key.")
                    else:
                        print("You don't have a key.")
                elif "win" in outcome.lower():
                    # assume the outcome contains a message for winning the game
                    print(outcome)
                    print("You won. Congratulations!")
                    exit()
            else:
                print("You don't have that item.")
        elif action == "examine":
            # use GPT-3 to generate descriptions for examining the object
            prompt = f"You examine {self.name}. What do you see?"
            description = generate_response(prompt)
            print(description)
        elif action == "combine":
            if self in player.inventory:
                # ask the player what other object they want to combine with
                other_object_name = input(f"What other object do you want to combine {self.name} with? ")
                other_object = next((o for o in player.inventory if o.name == other_object_name), None)
                if other_object:
                    # use GPT-3 to generate outcomes and consequences for combining the objects
                    prompt = f"You combine {self.name} and {other_object.name}. What happens?"
                    outcome = generate_response(prompt)
                    print(outcome)
                    # update the game state based on the outcome
                    if "create" in outcome.lower():
                        # assume the outcome contains the name and description of the new object
                        new_object_name = outcome.split()[1]
                        new_object_description = outcome.split(".")[1].strip()
                        new_object = Item(new_object_name, new_object_description)
                        # remove the old objects from the inventory and add the new object
                        player.inventory.remove(self)
                        player.inventory.remove(other_object)
                        player.inventory.append(new_object)
                        print(f"You created {new_object.name}.")
                else:
                    print("You don't have that item.")
            else:
                print("You don't have that item.")
        else:
            print("You can't do that.")

class VirtualWorld:
    def __init__(self):
        self.rooms = []
        self.items = []

    def add_room(self, room):
        self.rooms.append(room)

    def add_item(self, item):
        self.items.append(item)

def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].text.strip()

def generate_description(obj):
    prompt = f"Describe {obj.name}."
    return generate_response(prompt)

def generate_hint(player):
    # use GPT-3 to generate a hint for the player based on their current room and inventory
    prompt = f"You are in {player.current_room.name}. You have {', '.join([item.name for item in player.inventory])} in your inventory. What should you do next?"
    hint = generate_response(prompt)
    return hint

def play_game():
    player = Player("Player")
    world = VirtualWorld()

    # Set up the virtual world
    room1 = Room("Room 1", "A small room with a strange device in the corner.")
    room2 = Room("Room 2", "A larger room with an old painting on the wall.")
    room3 = Room("Room 3", "A cold, stone room with a small window.")
    room4 = Room("Room 4", "A secret room with a treasure chest.") # added a new room
    
    room1.connect_room("north", room2)
    room2.connect_room("south", room1)
    room2.connect_room("east", room3)
    room3.connect_room("west", room2)
    room3.connect_room("north", room4) # added a new connection
    room4.connect_room("south", room3) # added a new connection

    world.add_room(room1)
    world.add_room(room2)
    world.add_room(room3)
    world.add_room(room4) # added a new room

    key = Item("key", "A small metal key.")
    knife = Item("knife", "A sharp knife.")
    door = Item("door", "A wooden door with a keyhole.")
    painting = Item("painting", "An old painting of a mysterious figure.") # added a new item
    stone = Item("stone", "A small, shiny stone.")
    chest = Item("chest", "A treasure chest with a lock.") # added a new item

    room1.add_item(key)
    room2.add_item(knife)
    room2.add_item(painting) # added a new item
    room3.add_item(door)
    room3.add_item(stone)
    room4.add_item(chest) # added a new item

    world.add_item(key)
    world.add_item(knife)
    world.add_item(door)
    world.add_item(painting) # added a new item
    world.add_item(stone)
    world.add_item(chest) # added a new item
    
    player.current_room = room1  # Player starts in Room 1

    while True:
        print(f"\nYou are in the {player.current_room.name}.")
        print(player.current_room.description)
        print("You see: ", [item.name for item in player.current_room.items])
        print("You carry: ", [item.name for item in player.inventory])

        command = input("\nWhat do you want to do? (move [direction], interact [item name] [action], hint): ")

        if command.startswith("move"):
            _, direction = command.split()
            player.move(direction)
        elif command.startswith("interact"):
            _, item_name, action = command.split()
            player.interact(item_name, action)
        elif command == "hint":
            hint = generate_hint(player)
            print(hint)
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
