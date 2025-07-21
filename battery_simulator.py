# battery_simulator.py

import numpy as np
import matplotlib.pyplot as plt

# --- 1. Battery Parameters Definition ---

# General Battery Characteristics (typical for Li-ion EV battery)
# You can adjust these values based on typical EV battery packs (e.g., 60 kWh pack)
# For a simplified module/cell simulation, these values are reasonable.
NOMINAL_CAPACITY_AH = 100  # Ampere-hours (Ah) - e.g., a single large cell or a small module
NOMINAL_VOLTAGE_V = 3.7   # Volts (V) - Nominal voltage for a single Li-ion cell
INTERNAL_RESISTANCE_OHM = 0.005 # Ohms - Simplified internal resistance
COULOMBIC_EFFICIENCY = 0.99 # Efficiency of charge transfer (unitless, 0-1)

# Initial State
INITIAL_SOC_PERCENT = 80 # Initial State of Charge in percentage (0-100)

# --- 2. Simple Open Circuit Voltage (OCV) Model ---
# This is a very simplified linear relationship for OCV vs SoC.
# In reality, OCV-SoC curve is non-linear and more complex (S-shaped).
# For a quick demo, linear approximation is sufficient.
# You can later enhance this with a lookup table or a more complex polynomial fit.

# Let's assume a voltage range for the cell from 3.0V (0% SoC) to 4.2V (100% SoC)
# This is typical for Li-ion cells.
OCV_MIN_V = 3.0 # Volts - Open Circuit Voltage at 0% SoC
OCV_MAX_V = 4.2 # Volts - Open Circuit Voltage at 100% SoC

def get_ocv(soc_percent):
    """
    Calculates the Open Circuit Voltage (OCV) based on SoC using a linear approximation.
    Input: soc_percent (float) - State of Charge in percentage (0-100)
    Output: ocv_v (float) - Open Circuit Voltage in Volts
    """
    # Ensure SoC is within bounds (0 to 100)
    soc_percent = np.clip(soc_percent, 0, 100)

    # Linear interpolation between OCV_MIN_V and OCV_MAX_V
    ocv_v = OCV_MIN_V + (OCV_MAX_V - OCV_MIN_V) * (soc_percent / 100)
    return ocv_v

# Test the OCV function (this part only runs when the script is executed directly)
if __name__ == "__main__":
    print(f"--- Testing OCV Model ---")
    print(f"OCV at 0% SoC: {get_ocv(0):.2f} V")
    print(f"OCV at 50% SoC: {get_ocv(50):.2f} V")
    print(f"OCV at 100% SoC: {get_ocv(100):.2f} V")
    print(f"OCV at 25% SoC: {get_ocv(25):.2f} V") # Example intermediate value
    print(f"OCV at 75% SoC: {get_ocv(75):.2f} V") # Example intermediate value