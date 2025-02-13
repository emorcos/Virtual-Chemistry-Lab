import json
from models.equipment_model import EquipmentModel
from models.reactor_model import ReactorModel
from core.data_structures import Chemical, ChemicalStream, Reaction
from core.simulation_engine import SimulationEngine
import pandas as pd #Add pandas
from sklearn.linear_model import LinearRegression #Add LinearRegression

def load_chemical_data(filepath="data/chemicals.json"):
    """Loads chemical data from a JSON file and returns a list of dictionaries."""
    with open(filepath, "r") as f:
        chemical_data = json.load(f)
    return chemical_data

def load_equipment_data(filepath="data/equipment_data.json"):
    """Loads equipment data from a JSON file and returns a list of dictionaries."""
    with open(filepath, "r") as f:
        equipment_data = json.load(f)
    return equipment_data

def load_reaction_data(filepath="data/reactions.json"): #Data to JSON
    """Loads reaction data from a JSON file and returns a list of dictionaries."""
    with open(filepath, "r") as f:
        reaction_data = json.load(f)
    return reaction_data

def choose_chemical(chemicals):
    """Displays a list of chemicals and prompts the user to choose one."""
    print("\nAvailable Chemicals:")
    for i, name in enumerate(chemicals.keys()):
        print(f"{i+1}. {name}")

    while True:
        try:
            choice = int(input("Enter the number of the chemical: "))
            if 1 <= choice <= len(chemicals):
                return chemicals[list(chemicals.keys())[choice - 1]]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def choose_equipment(equipment_data):
    """Displays a list of equipment and prompts the user to choose one."""
    print("\nAvailable Equipment:")
    for i, equipment in enumerate(equipment_data):
        print(f"{i+1}. {equipment['name']} (Type: {equipment['type']})")

    while True:
        try:
            choice = int(input("Enter the number of the equipment: "))
            if 1 <= choice <= len(equipment_data):
                return equipment_data[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def choose_reaction(reaction_data):
    """Displays a list of reactions and prompts the user to choose one."""
    print("\nAvailable Reactions:")
    for i, reaction in enumerate(reaction_data):
        print(f"{i+1}. {reaction['name']}")

    while True:
        try:
            choice = int(input("Enter the number of the reaction: "))
            if 1 <= choice <= len(reaction_data):
                return reaction_data[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    # Load chemical data
    chemicals_data = load_chemical_data()
    chemicals = {chem['name']: Chemical(chem['name'], chem['formula'], chem['molar_mass'], chem['boiling_point'], chem['density'])
                 for chem in chemicals_data}

    # Load equipment data
    equipment_data = load_equipment_data()

    #Load reaction data
    reaction_data = load_reaction_data() #Load reaction

    #Load Model
    try:
        from scripts.train_reactor_model import model #If import works. The file and code should be setup
    except ImportError: #File cant be found?
        print("Train_reactor_model.py is missing. The process to generate a reactor model needs to be made first")
        exit()

    # Choose Equipment
    chosen_equipment_data = choose_equipment(equipment_data)

    #Create a reactor instance
    if chosen_equipment_data["type"] == "Reactor":
        reactor1 = ReactorModel(chosen_equipment_data["name"],chosen_equipment_data["volume"],model) #Value to be tested
        print("You have made " + str(reactor1))
    else:
        print("Please choose an equipment type that is a reactor")
        exit()
        # Create a ChemicalStream
    print("\nCreating Reactant Stream")
    reactant_stream = ChemicalStream()

    while True:
        # Choose Chemicals for the stream
        chosen_chemical = choose_chemical(chemicals)
        concentration = float(input(f"Enter the concentration of {chosen_chemical.name} (0-1): "))
        reactant_stream.add_chemical(chosen_chemical, concentration)

        add_more = input("Add another chemical to the stream? (y/n): ")
        if add_more.lower() != "y":
            break
    print("You are starting with  " + str(reactant_stream))

    # Choose Reaction
    chosen_reaction_data = choose_reaction(reaction_data)

    # Create the Reaction object
    reaction = Reaction(chosen_reaction_data['name'],
                          chosen_reaction_data['reactants'],
                          chosen_reaction_data['products'])

    # Set the reaction to the Reactor
    reactor1.set_reaction(reaction)

    # Add the stream to the Reactor
    reactor1.inputs['reactant_stream'] = reactant_stream

    # Simulate the Reactor
    print("\nRunning reactor")
    reactor1.process()
    print(f"Final is  {reactor1.outputs}")