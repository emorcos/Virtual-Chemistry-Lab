import pandas as pd

from models.equipment_model import EquipmentModel
from core.data_structures import Chemical, ChemicalStream
import numpy as np

class ReactorModel(EquipmentModel):
    def __init__(self, name, volume, model = None): #Add model name
        super().__init__(name)
        self.volume = volume  # Liters
        self.parameters['temperature'] = 25.0  # Celsius
        self.inputs['reactant_stream'] = None
        self.outputs['product_stream'] = ChemicalStream()
        self.reaction = None  # Store the Reaction object here
        self.model = model #ML
        self.conversion = 0.5  # Default conversion

    def set_reaction(self, reaction):
        """Sets the reaction to be used by this reactor."""
        self.reaction = reaction

    def process(self):
        """Simulate the reaction based on the provided Reaction object."""
        stream = self.inputs.get('reactant_stream') #Get stream value

        if stream is None or not stream.chemicals: #If values does not exist, stop the process
            print("Reactant Stream is empty or does not exist.")
            return

        temperature = self.parameters.get('temperature')
        if temperature is None: #If value does not exits stop
            temperature = 1 #Value isnt none
        #Load chemicals for model
        initial_concentration = None #Pre defined as blank
        limiting_reactant_stream = stream.chemicals.get(self.reaction.reactants[0]) #Name
        if limiting_reactant_stream is None:
            print("Value is None. A reactiant stream with the specified reactant needs to be made")
            return #Can be found stop

        #Set concentration, the second part of the tuple should exist
        initial_concentration = limiting_reactant_stream[1] #Concentraton

        flow_rate = 2 #L/min #Hardcode as a default value for now
        rate_constant = 0.05 #Default reaction constant
        #Set reactor volume based on model
        reactor_volume  = self.volume #Hardcode as a default value for now

        if self.reaction is None:
            print("Reaction is not defined. Please set the reaction before processing.")
            return

        #Using the new values, find
        space_time = reactor_volume/flow_rate
        product_Stream_conversion = self.model.predict([[temperature, initial_concentration,space_time,rate_constant]])

        #Create Product Stream
        product_stream = ChemicalStream() #Create a new temp stream
        for chemical_name, (chemical, concentration) in stream.chemicals.items():
            conversionStream = False
            for streamName in self.reaction.reactants:
                if (streamName == chemical_name):
                    conversionStream = True #If match, set true

            if(conversionStream == True):#Reactant and product are sepearte, so has to check reactants

                converted_amount = concentration * product_Stream_conversion  #React for new stream
                chemical.concentration = concentration - converted_amount #Set amount that hasnt reacted
                product_stream.add_chemical(chemical,chemical.concentration)

                stream.chemicals[chemical_name] = (chemical,concentration) #Keep its value in this stream
            else:
                product_stream.add_chemical(chemical, concentration)

        self.outputs['product_stream'] = product_stream
        print(f"Reactor: Reacting chemicals. Output is = {self.outputs['product_stream']}")
