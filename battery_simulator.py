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


# --- 3. Simulation Parameters ---
SIMULATION_DURATION_HOURS = 10 # Total simulation duration in hours
TIME_STEP_SECONDS = 60       # Time step for simulation in seconds (e.g., 60s = 1 minute)

# --- 4. Simulation Function ---
def simulate_battery(initial_soc_percent, current_profile_amps, simulation_duration_hours, time_step_seconds):
    """
    Simulates the charge/discharge behavior of the battery.
    Inputs:
        initial_soc_percent (float): Starting State of Charge in percentage (0-100).
        current_profile_amps (dict): Dictionary mapping time (in hours) to current (Amps).
                                     Positive current for charging, negative for discharging.
        simulation_duration_hours (float): Total simulation duration in hours.
        time_step_seconds (float): Time step for the simulation in seconds.
    Outputs:
        time_hours (list): List of time points in hours.
        soc_history (list): List of SoC values over time.
        ocv_history (list): List of OCV values over time.
        terminal_voltage_history (list): List of terminal voltage values over time.
        current_history (list): List of current values applied over time.
    """

    # Convert duration and time step to consistent units (seconds)
    total_steps = int((simulation_duration_hours * 3600) / time_step_seconds)
    dt_hours = time_step_seconds / 3600.0 # Time step in hours

    # Initialize lists to store simulation data
    time_hours = []
    soc_history = []
    ocv_history = []
    terminal_voltage_history = []
    current_history = []

    # Set initial SoC
    current_soc_percent = initial_soc_percent

    # Determine the current at each time step based on the profile
    profile_times_hours = sorted(current_profile_amps.keys())

    # Simulation loop
    for i in range(total_steps + 1): # +1 to include the final time point
        t_current_hours = i * dt_hours
        time_hours.append(t_current_hours)

        # Find the current value for the current time step
        # This logic assumes the current profile specifies current for time intervals
        current_amp = 0
        for k in range(len(profile_times_hours)):
            if t_current_hours >= profile_times_hours[k]:
                current_amp = current_profile_amps[profile_times_hours[k]]
            else:
                break # Use the last valid current until the next defined time
        current_history.append(current_amp)

        # --- Battery Model Calculations ---

        # 1. Update SoC using Coulomb Counting
        # Current is in Amps, dt_hours in hours, NOMINAL_CAPACITY_AH in Ah
        # delta_soc = (Current * time_step_hours / Nominal_Capacity_Ah) * 100
        # For charging, current is positive, efficiency applies to incoming charge.
        # For discharging, current is negative, efficiency applies to outgoing charge (or is 1/efficiency for calculation).

        if current_amp > 0: # Charging
            delta_soc_percent = (current_amp * dt_hours * COULOMBIC_EFFICIENCY / NOMINAL_CAPACITY_AH) * 100
        else: # Discharging (current_amp is negative)
            # For discharging, divide by efficiency as more charge is needed to output same useful energy
            delta_soc_percent = (current_amp * dt_hours / COULOMBIC_EFFICIENCY / NOMINAL_CAPACITY_AH) * 100

        current_soc_percent += delta_soc_percent

        # Clip SoC to stay within 0-100% physically
        current_soc_percent = np.clip(current_soc_percent, 0, 100)
        soc_history.append(current_soc_percent)

        # 2. Calculate Open Circuit Voltage (OCV)
        ocv_v = get_ocv(current_soc_percent)
        ocv_history.append(ocv_v)

        # 3. Calculate Terminal Voltage
        # V_terminal = OCV - (I * R_internal)
        # Positive current (charging) means V_terminal > OCV
        # Negative current (discharging) means V_terminal < OCV
        terminal_voltage_v = ocv_v - (current_amp * INTERNAL_RESISTANCE_OHM)
        terminal_voltage_history.append(terminal_voltage_v)

    return time_hours, soc_history, ocv_history, terminal_voltage_history, current_history


# --- 5. Example Usage / Main Execution Block ---
if __name__ == "__main__":
    print("\n--- Starting Battery Simulation ---")

    # Define a simple current profile (time in hours: current in Amps)
    # Positive current = Charging, Negative current = Discharging
    # Example: Discharge at 10A for 5 hours, then Charge at 5A for 5 hours
    current_profile = {
        0: -10,  # From 0 hours, discharge at 10 Amps
        5: 5     # From 5 hours, charge at 5 Amps
    }

    # Run the simulation
    times, socs, ocvs, voltages, currents = simulate_battery(
        INITIAL_SOC_PERCENT,
        current_profile,
        SIMULATION_DURATION_HOURS,
        TIME_STEP_SECONDS
    )

    # Print some sample results
    print(f"Simulation completed for {SIMULATION_DURATION_HOURS} hours.")
    print(f"Initial SoC: {INITIAL_SOC_PERCENT:.2f}%")
    print(f"Final SoC: {socs[-1]:.2f}%")
    print(f"Final Terminal Voltage: {voltages[-1]:.2f} V")

    # --- 6. Plotting Results ---
    print("\n--- Generating Plots ---")

    plt.figure(figsize=(12, 8)) # Create a figure with a specific size

    # Plot 1: State of Charge (SoC)
    plt.subplot(3, 1, 1) # 3 rows, 1 column, 1st plot
    plt.plot(times, socs, label='State of Charge (%)', color='blue')
    plt.title('Battery Simulation: SoC, Voltage, and Current Profile')
    plt.ylabel('SoC (%)')
    plt.grid(True)
    plt.legend()
    plt.ylim(0, 100) # Ensure y-axis for SoC is always 0-100

    # Plot 2: Terminal Voltage
    plt.subplot(3, 1, 2) # 3 rows, 1 column, 2nd plot
    plt.plot(times, voltages, label='Terminal Voltage (V)', color='red')
    plt.ylabel('Voltage (V)')
    plt.grid(True)
    plt.legend()
    # Set realistic voltage limits based on typical Li-ion cell range
    plt.ylim(OCV_MIN_V - 0.1, OCV_MAX_V + 0.1) 


    # Plot 3: Current Profile
    plt.subplot(3, 1, 3) # 3 rows, 1 column, 3rd plot
    plt.plot(times, currents, label='Applied Current (A)', color='green')
    plt.xlabel('Time (Hours)')
    plt.ylabel('Current (A)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout() # Adjust subplot parameters for a tight layout
    plt.show() # Display the plots

    print("Plots generated successfully!")

    # You can inspect specific points if needed, e.g., after 1 hour (index approx 60 steps)
    # print(f"SoC after 1 hour: {socs[int(3600/TIME_STEP_SECONDS)]:.2f}%")

# Test the OCV function (this part only runs when the script is executed directly)
if __name__ == "__main__":
    print(f"--- Testing OCV Model ---")
    print(f"OCV at 0% SoC: {get_ocv(0):.2f} V")
    print(f"OCV at 50% SoC: {get_ocv(50):.2f} V")
    print(f"OCV at 100% SoC: {get_ocv(100):.2f} V")
    print(f"OCV at 25% SoC: {get_ocv(25):.2f} V") # Example intermediate value
    print(f"OCV at 75% SoC: {get_ocv(75):.2f} V") # Example intermediate value