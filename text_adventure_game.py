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

    def connect_room(self, direction, room):
        self.connected_rooms[direction] = room

class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = []

    def move(self, direction):
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
        else:
            print("You can't go that way.")

    def interact(self, obj):
        # code to interact with an object in the virtual world
        # you can add more details here depending on the game logic
        pass

class VirtualWorld:
    def __init__(self):
        self.rooms = []
        self.objects = []

    def add_room(self, room):
        self.rooms.append(room)

    def add_object(self, obj):
        self.objects.append(obj)

class Object:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def interact(self):
        # code to interact with the object
        # you can add more details here depending on the game logic
        pass

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

def play_game():
    player = Player()
    world = VirtualWorld()

    # Set up the virtual world
    room1 = Room("Room 1", "A dimly lit room.")
    room2 = Room("Room 2", "A room with a large window.")
    room1.connect_room("north", room2)
    room2.connect_room("south", room1)
    
    world.add_room(room1)
    world.add_room(room2)
    
    player.current_room = room1  # Player starts in room1

    while True:
        print("You are in", player.current_room.name)
        print(generate_description(player.current_room))
        
        command = input("> ").split()
        
        action = command[0].lower()
        if action == "move":
            if len(command) > 1:
                player.move(command[1])
            else:
                print("Which direction do you want to move?")
        elif action == "interact":
            if len(command) > 1:
                # Assuming the object is in the same room as the player
                object_name = " ".join(command[1:])
                obj = next((o for o in world.objects if o.name == object_name), None)
                if obj:
                    player.interact(obj)
                else:
                    print("That object doesn't exist in this room.")
            else:
                print("What do you want to interact with?")
        else:
            print("I don't understand that command.")

def main():
    play_game()

if __name__ == "__main__":
    main()

