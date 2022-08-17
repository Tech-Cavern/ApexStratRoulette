# SCRAPPED: Create menu to make options for randomizing (Divide into weapon classes/ammo classes)
# DONE: Create functions to yield and (temporarily) save data from json per item class (Legends, weapons)
# DONE: Create function to randomise output in sets of 3x1
# DONE: Prettyprint output
# DONE: Expand json with: Legends | Maps (Drop POIs) | Maps (Map features (MRVNs, Holds, Nature) | //Ordnance
# DONE: Expand randomizer to fetch weapons through json
# DONE: Create basic map POI selection output
# DONE: Mirror output from console into tkinter popup window
# DONE: Implement a % chance of getting a special map POI on top of the drop site (Explosive Holds, Vaults, etc.)
# DONE: Heirloom weapon protection
# TODO: Make the output window a bit more pretty, plain white black-on-white text is too boring
# DONE: Implement a % chance of running melee-/grenade only matches (Skipping weapon choice altogether in this %)
# TODO: Add map image (Despite tkinter absolutely fucking hating images)
# DONE: Refresh / close buttons
# DONE: Optimise code for a refresh button to work. Currently, it would create a completely new window
# DONE: Create a custom list/entry in data.json with custom challenges. Brainstorm some ideas!
# DONE: Clean up code / Optimise code / Un-spagghetify code / Holy fuck lmao
# DONE: Expand data.json to include custom challenge that can't be rolled through the current program philosophy
# DONE: Implement reading custom challenges and add these to a button, which will open a pop-up with a random challenge
# DONE: Optimise API usage, greatly reduce amount of API calls
# DONE: Update data and stuff for Season 14

import json
import random
import time

import requests
import tkinter as tk
from tkinter import messagebox

# Prioritised actions are above refresh function definition for readability and clarification
# Receive auth token for map data API through secrets file
with open("secrets.json", "r") as secretsData:
    secrets = json.load(secretsData)
    auth = secrets["authtoken"]

mapRequest = f"https://api.mozambiquehe.re/maprotation?version=2&auth={auth}"


# Main functions used for the program
def generate(jsonData, mapRequest):

    # Legend selection
    # The list of legends regenerated with each time the function is ran, so it won't end up empty
    legends = []
    for item in jsonData["legends"]:
        legends.append(item)
    counterLegends = 0
    # Repeats until it's generated three legends
    while True:
        if counterLegends <= 3:
            counterLegends += 1
            if counterLegends == 1:
                randomLegend = random.choice(legends)
                legends.remove(randomLegend)  # Legend gets removed from the list, so it can't be picked again
                legend1["text"] = f"First legend pick: {randomLegend}"
            elif counterLegends == 2:
                randomLegend = random.choice(legends)
                legends.remove(randomLegend)
                legend2["text"] = f"Second legend pick: {randomLegend}"
            elif counterLegends == 3:
                randomLegend = random.choice(legends)
                legends.remove(randomLegend)
                legend3["text"] = f"Third legend pick: {randomLegend}\n"
        else:
            break

    # Weapon selection
    if random.randint(1, 100) <= 5:  # 5% chance for this to occur. Weapon selection will be skipped.
        weaponLabel["text"] = "No weapons! You'll only use your fists and grenades this match!\n"
    else:  # For the other 95%, the program will use the standard weapon picking
        weaponSet1 = ""
        weaponSet2 = ""
        weaponSet3 = ""

        counterWeapons = 1
        # Repeats until it's generated 3 weapon sets
        while counterWeapons <= 3:
            if counterWeapons == 1:
                counterWeapons += 1
                primary = random.choice(allWeapons)
                if primary in heirloomWeapons and random.randint(1, 100) <= 50:
                    # To prevent heirloom weapons from rolling too often, there's a 50% chance to roll again
                    # In case the weapon ends up being a heirloom. This isn't proper proofing, but it does the job.
                    primary = random.choice(allWeapons)
                time.sleep(0.3)  # Waits a tiny bit before generating to prevent similar loadouts from occurring
                secondary = random.choice(allWeapons)
                if secondary in heirloomWeapons and random.randint(1, 100) <= 50:
                    secondary = random.choice(allWeapons)
                    # If both weapons are in the care package, it will fall back to pistols
                if primary in heirloomWeapons and secondary in heirloomWeapons:
                    weaponSet1 = f"{random.choice(fallbackWeapons)} and {random.choice(fallbackWeapons)} " \
                                 f"(Heirloom protection)"
                else:
                    weaponSet1 = f"{primary} and {secondary}"

            elif counterWeapons == 2:
                counterWeapons += 1
                primary = random.choice(allWeapons)
                if primary in heirloomWeapons and random.randint(1, 100) <= 50:
                    primary = random.choice(allWeapons)
                time.sleep(0.3)
                secondary = random.choice(allWeapons)
                if secondary in heirloomWeapons and random.randint(1, 100) <= 50:
                    secondary = random.choice(allWeapons)
                if primary in heirloomWeapons and secondary in heirloomWeapons:
                    weaponSet2 = f"{random.choice(fallbackWeapons)} and {random.choice(fallbackWeapons)} " \
                                 f"(Heirloom protection)"
                else:
                    weaponSet2 = f"{primary} and {secondary}"

            elif counterWeapons == 3:
                counterWeapons += 1
                primary = random.choice(allWeapons)
                if primary in heirloomWeapons and random.randint(1, 100) <= 50:
                    primary = random.choice(allWeapons)
                time.sleep(0.3)
                secondary = random.choice(allWeapons)
                if secondary in heirloomWeapons and random.randint(1, 100) <= 50:
                    secondary = random.choice(allWeapons)
                if primary in heirloomWeapons and secondary in heirloomWeapons:
                    weaponSet3 = f"{random.choice(fallbackWeapons)} and {random.choice(fallbackWeapons)} " \
                                 f"(Heirloom protection)"
                else:
                    weaponSet3 = f"{primary} and {secondary}"
            else:
                break

        weaponLabel["text"] = f"You'll be running the following weapons:\n" \
                              f"{weaponSet1}\n" \
                              f"{weaponSet2}\n" \
                              f"{weaponSet3}\n"

    # Map retrieval from the JSON file
    with open("mapData.json", "r") as data:
        mapData = json.load(data)
        data.close()

    # If the map data is empty, or the end time has passed, it will call for the API
    if mapData["end"] == 0 or mapData["end"] < time.time():
        response = requests.get(mapRequest)
        currentMap = response.json()["battle_royale"]["current"]["map"]
        mapEndTimer = response.json()["battle_royale"]["current"]["end"]

        # Create new dictionary with new data to push to data file
        newMapData = {
            "map": currentMap,
            "end": mapEndTimer
        }

        with open("mapData.json", "w") as outfile:
            json.dump(newMapData, outfile, indent=4)
    else:
        currentMap = mapData["map"]

    # Drop point location selection
    if currentMap == "Kings Canyon":
        KCmaps = []
        for item in jsonData["maps"]["kingscanyon"]["POIs"]:
            KCmaps.append(item)
        dropPoint = random.choice(KCmaps)
        # For this and following elifs: There is a 10% chance to roll a map event (Holds, Vaults, etc.)
        if random.randint(1, 100) <= 10:
            questLabel["text"] = "\nOpen an Explosive Hold this match!"
        else:  # Clear label upon refresh
            questLabel["text"] = ""

    elif currentMap == "World's Edge":
        WEmaps = []
        for item in jsonData["maps"]["worldsedge"]["POIs"]:
            WEmaps.append(item)
        dropPoint = random.choice(WEmaps)
        if random.randint(1, 100) <= 10:
            questLabel["text"] = "\nOpen a vault this match!"
        else:  # Clear label upon refresh
            questLabel["text"] = ""

    elif currentMap == "Olympus":  # Not active in Season 14
        OLmaps = []
        for item in jsonData["maps"]["olympus"]["POIs"]:
            OLmaps.append(item)
        dropPoint = random.choice(OLmaps)
        if random.randint(1, 100) <= 10:
            questLabel["text"] = "\nCollect a MRVN arm this match!"
        else:  # Clear label upon refresh
            questLabel["text"] = ""

    elif currentMap == "Storm Point":
        SPmaps = []
        for item in jsonData["maps"]["stormpoint"]["POIs"]:
            SPmaps.append(item)
        dropPoint = random.choice(SPmaps)
        if random.randint(1, 100) <= 10:
            questLabel["text"] = "\nClear out an IMC armory this match!"
        else:  # Clear label upon refresh
            questLabel["text"] = ""

    # Basic output of current map and a randomly picked POI to land on
    mapLabel["text"] = f"The current map is {currentMap}\n" \
                       f"You'll land on {dropPoint} this match"


def customChallenge(jsonData):
    challengeList = []
    # Reads data from the json data and adds each item to a local list, after which a random item will be picked
    for item in jsonData["challenges"]["custom"]:
        challengeList.append(item)
    customLabel["text"] = f"Custom challenge:\n{random.choice(challengeList)}"


# Open general data file for use
with open("data.json", "r") as data:
    jsonData = json.load(data)

# Weapon selection from data.json, gets all items directly under the array "weapons", and adds them to a local list
allWeapons = []
for item in jsonData["weapons"]:
    allWeapons.append(item)

heirloomWeapons = ["Kraber", "Mastiff", "Bocek", "Rampage"]  # As per Season 14
fallbackWeapons = ["RE-45", "P2020", "Wingman", "Mozambique"]

# Application window generation
root = tk.Tk()
root.title("Apex Strat Roulette")
root.geometry("720x480")
root.iconbitmap("APEX_legends_logo_mini.ico")
root.option_add('*Dialog.msg.font', 'Helvetica 16')

# Legend selection creation. The legends are not yet generated, this happens on the first refresh
legend1 = tk.Label(text="Legend 1 not generated", font="Helvetica, 16")
legend2 = tk.Label(text="Legend 2 not generated", font="Helvetica, 16")
legend3 = tk.Label(text="Legend 3 not generated", font="Helvetica, 16")

# Weapon label creation before receiving data
weaponLabel = tk.Label(text="\nWeapon selection not generated\n",
                       font="Helvetica 16")

# Basic output of current map and a randomly picked POI to land on
mapLabel = tk.Label(text=f"Map selection not generated",
                    font="Helvetica, 16")

# Variable creations before assignment, prevents errors
questLabel = tk.Label(text="",
                      font="Helvetica, 16")

customLabel = tk.Label(text="Custom challenge:\n(Not generated)", font="Helvetica, 16", wraplength=600)

closeButton = tk.Button(root, text="Close", width=10, command=root.destroy)
refreshButton = tk.Button(root, text="Generate", width=10, command=lambda: generate(jsonData, mapRequest))
customButton = tk.Button(root, text="Custom", width=10, command=lambda: customChallenge(jsonData))

# Chunk packing of all the above-created labels
legend1.pack()
legend2.pack()
legend3.pack()
weaponLabel.pack()
mapLabel.pack()
questLabel.pack()
customLabel.pack()
closeButton.place(x=240, y=450)
refreshButton.place(x=320, y=450)
customButton.place(x=400, y=450)

# Start window until forcibly closed
root.mainloop()


# The functions below are ignored and only here for archival purposes
# They are functional, but not used, and have been integrated into the runWindow() function
def Main():
    yieldLegends()
    yieldWeapons(jsonData)
    selectMap(jsonData, mapRequest)


def yieldLegends():
    legends = ["Bloodhound", "Gibraltar", "Lifeline", "Pathfinder", "Wraith", "Bangalore", "Caustic", "Mirage",
               "Octane", "Wattson", "Crypto", "Revenant", "Loba", "Rampart", "Horizon", "Fuse", "Valkyrie", "Seer",
               "Ash", "Mad Maggie", "Newcastle"]
    print("Picked legends:")
    counter = 0
    while True:
        if counter <= 2:
            counter += 1
            randomLegend = random.choice(legends)
            print(randomLegend)
            legends.remove(randomLegend)
        else:
            break


def yieldWeapons(jsonData):
    allWeapons = []
    for item in jsonData["Weapons"]:
        allWeapons.append(item)

    print(f"\nYou'll be running the following weapons:\n"
          f"{random.choice(allWeapons)} and {random.choice(allWeapons)}\n"
          f"{random.choice(allWeapons)} and {random.choice(allWeapons)}\n"
          f"{random.choice(allWeapons)} and {random.choice(allWeapons)}\n")


def selectMap(jsonData, mapRequest):
    response = requests.get(mapRequest)
    currentMap = response.json()["battle_royale"]["current"]["map"]

    if currentMap == "Kings Canyon":
        # Create blank list to push POIs from the JSON into
        KCmaps = []
        for item in jsonData["maps"][0]["kingscanyon"]["POIs"]:
            KCmaps.append(item)
        dropPoint = random.choice(KCmaps)
    elif currentMap == "World's Edge":
        # Create blank list to push POIs from the JSON into
        WEmaps = []
        for item in jsonData["maps"][0]["worldsedge"]["POIs"]:
            WEmaps.append(item)
        dropPoint = random.choice(WEmaps)
    elif currentMap == "Olympus":
        # Create blank list to push POIs from the JSON into
        OLmaps = []
        for item in jsonData["maps"][0]["olympus"]["POIs"]:
            OLmaps.append(item)
        dropPoint = random.choice(OLmaps)
    elif currentMap == "Storm Point":
        # Create blank list to push POIs from the JSON into
        SPmaps = []
        for item in jsonData["maps"][0]["stormpoint"]["POIs"]:
            SPmaps.append(item)
        dropPoint = random.choice(SPmaps)

    # Basic output of current map and a randomly picked POI to land on
    print(f"\nThe current map is {currentMap}\n"
          f"You'll land on {dropPoint} this match.")

