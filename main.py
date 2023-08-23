import random, json, time, os
color_red = '\033[91m'
color_green = '\033[92m'
color_yellow = '\033[93m'
color_blue = '\033[94m'
color_magenta = '\033[95m'
color_cyan = '\033[96m'
color_white = '\033[97m'
color_reset = '\033[96m'
#color_reset = '\033[0m'


# Define the Player class
class Player:
    def __init__(self, name):
        # Initialize player attributes
        self.name = name
        self.team = []
        self.hp = 100
        self.inventory = []
        self.karma = random.randint(-100, 100)
        self.attack_damage = random.randint(1, 10)
        self.hunger = 100

    def add_teammate(self):
        self.team.append()

    def remove_teammate(self):
        self.team.remove()

    # Method to handle player taking damage
    def take_damage(self, damage):
        self.hp -= damage

    # Method to calculate total attack damage
    def get_total_attack_damage(self):
        total_damage = self.attack_damage
        for item in self.inventory:
            if item == "Small Dagger":
                total_damage += 5
        return total_damage

# Function to save player data to a JSON file
def save_game(players, current_day):
    data_to_save = {
        "current_day": current_day,
        "players": [player.__dict__ for player in players]
    }
    with open("saved_game.json", "w") as file:
        json.dump(data_to_save, file, indent=4)

# Function to load player data from a JSON file
def load_game():
    try:
        with open("saved_game.json", "r") as file:
            data = json.load(file)
            players_data = data["players"]
            current_day = data["current_day"]
            players = []
            
            for player_data in players_data:
                player = Player(player_data["name"])
                player.team = player_data["team"]
                player.hp = player_data["hp"]
                player.karma = player_data["karma"]
                player.inventory = player_data["inventory"]
                player.hunger = player_data["hunger"]
                players.append(player)
            
            
            return players, current_day  # Return the loaded players and current_day
    except FileNotFoundError:
        return [], 1  # Return an empty list of players and start from day 1 if no save file found


# Function to limit player karma within a certain range
def limit_karma(player):
    player.karma = max(100, min(player.karma, -100))

# Function to generate events for players
def generate_player_event(player, players):
    event_chance = random.randint(1, 100)

    if event_chance == 1:
        print(f"{player.name} found a cave for shelter.")

    elif event_chance == 2:
        print(f"{player.name} found a small dagger.")
        player.inventory.append("Small Dagger")

    
    elif event_chance == 3:
        craft_chance = random.randint(1, 100)
        if craft_chance <= 50:
            print(f"{player.name} Failed to make a crude axe.")

        else:
            print(f"{player.name} Made a crude axe!")
            player.inventory.append("Crude Axe")


    elif event_chance == 4:
        print(f"{player.name} found a mysterious treasure chest.")
        with open("items.json", "r") as items_file:
            items_data = json.load(items_file)
            treasure_items = random.sample(items_data, 3)
            player.inventory.extend(treasure_items)

    
    elif event_chance == 5:
        food_amount = random.randint(1, 5)
        existing_food = None

        for index, item in enumerate(player.inventory):
            if item.startswith("Food"):
                existing_food = index
                break
            
        if existing_food is not None:
            current_amount = int(player.inventory[existing_food].split(" ")[1])
            new_amount = current_amount + food_amount
            player.inventory[existing_food] = f"Food {new_amount}"
        else:
            player.inventory.append(f"Food {food_amount}")
        
        print(f"{player.name} discovered a hidden stash of {food_amount} food.")


    
    elif event_chance == 6:
        print(f"{player.name} stumbled upon a first aid kit.")
        player.inventory.append("First Aid Kit")

    
    elif event_chance == 7:
        print(f"{player.name} encountered a friendly traveler and traded items.")
        if player.inventory:
            trade_item = random.choice(player.inventory)
            player.inventory.remove(trade_item)
            player.inventory.append(trade_item)#need to make this a random item from items.json

    elif event_chance == 8:  # Combat Event
        other_player = random.choice(players)
        if other_player != player and (other_player.name not in player.team):
            print(f"\n{player.name} and {other_player.name} encountered each other!")

            fight_chance = random.randint(1, 100)
            if (player.karma > other_player.karma and fight_chance <= 80):
                print(f"{player.name} decided to fight to the death.")

                damage = player.get_total_attack_damage()
                defender_damage = other_player.get_total_attack_damage()

                block_chance = random.randint(1, 100)
                if block_chance <= 45: 
                    print(f"{player.name} managed to block {other_player.name}'s attack!")
                else:
                    player.take_damage(defender_damage)
                    print(f"{player.name} couldn't block and took {defender_damage} damage from {other_player.name}'s attack!")

                other_player.take_damage(damage)

                print(f"{player.name} attacked {other_player.name} for {damage} damage!")
                print(f"{other_player.name} attacked back for {defender_damage} damage!")

                if player.hp <= 0:
                    print(f"{player.name} has died in combat and will be removed from the game.")
                    players.remove(player)

                if other_player.hp <= 0:
                    print(f"{other_player.name} has died in combat and will be removed from the game.")
                    players.remove(other_player)

                player.karma -= 10

            else:
                print(f"Both {player.name} and {other_player.name} decided to go their separate ways without interacting.")

    
    elif event_chance == 9:  # Teaming Event
        other_player = random.choice(players)
        if other_player != player and (other_player.name not in player.team):
            print(f"\n{player.name} and {other_player.name} decided to join forces!")

            shared_inventory = list(set(player.inventory + other_player.inventory))
            player.inventory = shared_inventory
            player.team.append(other_player.name)  
            other_player.team.append(player.name)
            other_player.inventory = shared_inventory
            player.karma += 10
            other_player.karma += 10
        else:
            print(f"Both {player.name} and {other_player.name} decided to go their separate ways without interacting.")

    # Event 10: Gain Trust of a Friendly Animal
    elif event_chance == 10:
        print(f"{player.name} stumbled upon a friendly animal and gained its trust.")
        player.karma += 5

    # Event 11: Find a Map
    elif event_chance == 11:
        print(f"{player.name} found a map to a hidden location.")
        player.inventory.append("Map")

    # Event 12: Discover a Broken Radio
    elif event_chance == 12:
        print(f"{player.name} discovered a broken radio. Maybe it can be fixed.")
        chance = random.randint(1,2)
        time.sleep(random.randint(1,4))
        if chance == 1:
            print(f"{player.name} decided to take the broken radio.")
            
        else:
            print(f"{player.name} decided not to take the broken radio.")

    # Event 13: Encounter Hostile Creatures
    elif event_chance == 13:
        print(f"{player.name} came across a group of hostile creatures.")
        chance = random.randint(1,2)
        hostile_creatures_dmg = random.randint(10, 25)
        time.sleep(random.randint(1,4))
        if chance == 1:
            print(f"{player.name} managed to leave unoticed.")
        else:
            print(f"{player.name} was noticed by the hostile creatures and was hurt while escaping.")
            player.hp -= hostile_creatures_dmg
            print(f"{player.name} lost {color_red}{hostile_creatures_dmg} hp{color_reset} and is now at {player.hp} health" )

    # Event 14: Find a Medicinal Plant
    elif event_chance == 14:
        print(f"{player.name} found a rare plant with medicinal properties.")
        player.inventory.append("Medicinal Plant")

    # Event 15: Discover a Secret Cave
    elif event_chance == 15:
        print(f"{player.name} stumbled upon a secret cave with ancient inscriptions.")

    # Event 16: Find an Abandoned Campsite
    elif event_chance == 16:
        print(f"{player.name} found an abandoned campsite with valuable resources.")

    # Event 17: Encounter a Fortune Teller
    elif event_chance == 17:
        print(f"{player.name} encountered a mysterious fortune teller who gave a cryptic message.")
        chance = random.randint(1, 2)
        time.sleep(random.randint(1,4))
        if chance == 1:
            player.karma += 5
            print(f"{player.name} gained 5 karma and is now at {player.karma}.")
            time.sleep(random.randint(1,4))
        else:
            player.karma -= 5
            print(f"{player.name} lost 5 karma and is now at {player.karma}.")
            time.sleep(random.randint(1,4))
    
        # Event 18: Discover a Hidden Underground Tunnel
    
    elif event_chance == 18:
        print(f"{player.name} discovered a hidden underground tunnel.")
        chance = random.randint(1, 2)
        time.sleep(random.randint(1,4))
        if chance == 1:
            print(f"{player.name} decided to explore the tunnel.")
            time.sleep(random.randint(1,4))
            if chance == 1:
                print(f"{player.name} found a brick in the shape of a loaf of bread.")
                player.inventory.append("loaf brick")
                time.sleep(random.randint(1,4))
            else:
                print(f"{player.name} found nothing.")
        else:
            print(f"{player.name} decided not to explore the tunnel.")

# Event 19: Meet a Group of Survivors
    elif event_chance == 19:
        print(f"{player.name} came across a group of survivors and exchanged stories.")

# Event 20: Find a Cache of Rare Coins and Artifacts
    elif event_chance == 20:
        print(f"{player.name} found a cache of rare coins and artifacts.")
        player.inventory.append("Rare Coins")
        player.inventory.append("Artifacts")

    # Event 21: Stumble Upon an Old Diary
    elif event_chance == 21:
        print(f"{player.name} stumbled upon an old diary that contains valuable information and gained +5 atk damage.")
        player.attack_damage += 5
        
    elif 22 <= event_chance <= 40:
        food_amount = random.randint(1, 5)
        existing_food = None

        for index, item in enumerate(player.inventory):
            if item.startswith("Food"):
                existing_food = index
                break
            
        if existing_food is not None:
            current_amount = int(player.inventory[existing_food].split(" ")[1])
            new_amount = current_amount + food_amount
            player.inventory[existing_food] = f"Food {new_amount}"
        else:
            player.inventory.append(f"Food {food_amount}")
        
        with open("food_messages.json", "r") as file:
            food_messages = json.load(file)
            food_message = random.choice(food_messages)
            print(f"{player.name}{food_message.format(food_amount=food_amount)}")

    elif 40 <= event_chance <= 90:
    
        
        with open("filler_messages.json", "r") as file:
            filler_messages = json.load(file)
            filler_message = random.choice(filler_messages)
            print(f"{player.name}{filler_message}")

    elif 90 <= event_chance <= 100:
        damage = random.randint(10, 60)
        
        with open("death_messages.json", "r") as file:
            death_messages = json.load(file)
            death_message = random.choice(death_messages)
            formatted_death_message = death_message.format(damage=damage, color_red = color_red,color_reset = color_reset)
            print(f"{player.name}{color_red}{formatted_death_message}{color_reset}")
            player.hp = max(player.hp - damage, 0)
            if player.hp <= 0:
                print(f"{player.name} has died and will be removed from the game.")
                players.remove(player)


def decrease_hunger(player, players):
    hunger_dmg = random.randint(5, 20)
    if player.hunger <= 100:
        
        for index, item in enumerate(player.inventory):
            if item.startswith("Food"):
                existing_food = index
                break
        else:
            existing_food = None

        if existing_food is not None and player.inventory:
            current_amount = int(player.inventory[existing_food].split(" ")[-1])
            new_amount = max(current_amount - 1, 0)
            player.inventory[existing_food] = f"Food {new_amount}"

        else:
            player.hunger = max(player.hunger - random.randint(3, 15), 0)
            print(f"{player.name}'s hunger decreased. Current hunger: {player.hunger}")
            time.sleep(1)

            if player.hunger <= 0:
                print(f"{player.name} is weakened by hunger, losing {hunger_dmg} health.")
                player.hp = max(player.hp - hunger_dmg, 0)
                player.hp = min(player.hp, 100) 

def heal(player, players):
    first_aid = random.randint(30, 75)
    herb = random.randint(20, 45)
    if player.hp <= 75:
        print(f"{player.name} noticed their health is low and checks if they have any healing items.")
        if "First Aid Kit" in player.inventory:
            player.inventory.remove("First Aid Kit")
            player.hp = min(player.hp + first_aid, 100)  # Increase health by 30 - 75, capped at 100
            print(f"{player.name} used the First Aid Kit and gained {first_aid} health. {player.name} is currently at {player.hp} health")
        elif "Medicinal Plant" in player.inventory:
            player.inventory.remove("Medicinal Plant")
            player.hp = min(player.hp + herb, 100)  # Increase health by 20 - 45, capped at 100
            print(f"{player.name} used the First Aid Kit and gained {herb} health. {player.name} is currently at {player.hp} health")
        else:
            print("Unfortunately, they didn't have any healing items to use.")
        

# Function to load default player names
def load_default_names():
    try:
        with open("default_names.json", "r") as file:
            names = json.load(file)
            return names
    except FileNotFoundError:
        return []


# Main Function
def main():
    # Main game loop
    current_day = 1
    max_days = 100
    players = []

    # Check if the save file exists
    if os.path.exists("saved_game.json"):
        load_save_file = input(f"{color_green}Do you want to load your save file? (yes/no):{color_reset} ")

        while load_save_file.lower() not in ["yes", "no"]:
            print(f"{color_red}Invalid input. Please enter 'yes' or 'no.'{color_reset}")
            load_save_file = input(f"{color_green}Do you want to load your save file? (yes/no):{color_reset} ")

        if load_save_file.lower() == "yes":
            players, current_day = load_game()
        elif load_save_file.lower() == "no":
            delete_save_file = input(f"{color_yellow}Do you want to delete the save file? (yes/no):{color_reset} ")

            while delete_save_file.lower() not in ["yes", "no"]:
                print(f"{color_red}Invalid input. Please enter 'yes' or 'no.'{color_reset}")
                delete_save_file = input(f"{color_yellow}Do you want to delete the save file? (yes/no):{color_reset} ")

            if delete_save_file.lower() == "yes":
                os.remove("saved_game.json")
                print("Save file deleted.")
                print("Please restart the game.")
                time.sleep(5)
                exit()
            elif delete_save_file.lower() == "no":
                print(f"{color_blue}Save file not loaded or deleted. Closing...{color_reset}")
                time.sleep(5)
                exit()
    
    # Load default or new player names
    elif not os.path.exists("saved_game.json"):
        while True:
            use_default_names = input(f"{color_green}Do you want to use default names for players? (yes/no):{color_reset} ").lower()

            if use_default_names == "yes":
                default_names = load_default_names()
                num_players_input = input(f"{color_green}Enter the number of players:{color_reset} ")

                while not num_players_input.isdigit():
                    print(f"{color_red}Please enter a valid number.{color_reset}")
                    num_players_input = input(f"{color_green}Enter the number of players:{color_reset} ")

                num_players = int(num_players_input)

                if num_players <= 0:
                    print(f"{color_red}Number of players must be greater than 0.{color_reset}")
                else:
                    players = [Player(name) for name in default_names[:num_players]]
                    break
            
            elif use_default_names == "no":
                while True:
                    num_players_input = input(f"{color_green}Enter the number of players:{color_reset} ")

                    while not num_players_input.isdigit():
                        print(f"{color_red}Please enter a valid number.{color_reset}")
                        num_players_input = input(f"{color_green}Enter the number of players:{color_reset} ")

                    num_players = int(num_players_input)

                    if num_players not in range(1, 100):
                        print(f"{color_red}Number of players must be between 1 and 99.{color_reset}")
                        continue

                    for i in range(num_players):
                        name = input(f"{color_green}Enter name for Player {i + 1}:{color_reset} ")
                        players.append(Player(name))
                    break
            else:
                print(f"{color_red}Invalid input. Please enter 'yes' or 'no.'{color_reset}")




    while True:
        # Loop through days and events
        for day in range(current_day, max_days):
            print(f"\n{color_cyan}--- Story Time ---")
            print(f"\n{color_magenta}Day {current_day}:{color_reset}")
            
            if not players:
                print("No players left. The game will now end.")
                play_again = input("Do you want to reset the game and play again? (yes/no): ")
                if play_again.lower() == "yes":
                    os.remove("saved_game.json")
                    print("Save file wiped. Restarting the game.")
                    time.sleep(3)
                    main()
                else:
                    print("Thank you for playing!")
                    exit()
            
            day_start_time = time.time()
            while time.time() - day_start_time < 300:  # Keep looping for 5 minutes
                for player in players:
                    random_player = random.choice(players)
                    limit_karma(player)
                    heal(player, players)
                    generate_player_event(random_player, players)
                    decrease_hunger(player, players)
                    save_game(players, current_day)
                    time.sleep(random.randint(4, 7))
            current_day += 1

            if day == max_days - 1:
                play_again = input("Game has ended. Do you want to play again? (yes/no): ")
                if play_again.lower() != "yes":
                    os.remove("saved_game.json")
                    print("Save file wiped.")
                    continue
                else:
                    break
if __name__ == "__main__":
    main()