class Chemical:
    def __init__(self, name, formula, molar_mass, boiling_point=None, density=None):
        self.name = name
        self.formula = formula
        self.molar_mass = molar_mass
        self.boiling_point = boiling_point
        self.density = density
        self.concentration = 0.0 # Molar concentration

    def __repr__(self):
        return f"{self.name} ({self.formula}): Conc={self.concentration}"

class ChemicalStream:
    def __init__(self, chemicals=None, temperature=25.0, pressure=1.0):
        self.chemicals = chemicals if chemicals is not None else {}  # Dictionary of Chemical objects (name: Chemical object)
        self.temperature = temperature  # Celsius
        self.pressure = pressure  # atm

    def add_chemical(self, chemical, concentration):
        """Adds a chemical to the stream."""
        self.chemicals[chemical.name] = (chemical, concentration)

    def get_chemical_concentration(self, chemical_name):
        """Returns concentration of a chemical."""
        for chemical, concentration in self.chemicals.values():
            if chemical.name == chemical_name:
                return concentration
        return 0.0  # Return 0 if chemical not found.

    def __repr__(self):
        chemical_info = ", ".join(f"{name}:{conc}" for name, (chem, conc) in self.chemicals.items())
        return f"ChemicalStream: {chemical_info}, Temp={self.temperature}C, Pressure={self.pressure}atm"

class Reaction:
    def __init__(self, name, reactants, products):
        self.name = name
        self.reactants = reactants  # List of reactant names
        self.products = products #Dict with chemical and % each
        self.conversion = None