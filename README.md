# EV Battery Charge/Discharge Simulation

## Project Overview

This project presents a simplified Python-based simulation of an Electric Vehicle (EV) battery's charge and discharge cycles. It models key battery characteristics such as State of Charge (SoC), Open Circuit Voltage (OCV), and terminal voltage, providing insights into battery behavior under various current profiles.

Developed by Anshika Bansal (https://github.com/AnshikaB-25).

## Key Features

* **Coulomb Counting SoC Estimation:** Tracks the battery's charge level over time.
* **Linear OCV-SoC Model:** Implements a basic relationship between battery's Open Circuit Voltage and its State of Charge.
* **Terminal Voltage Calculation:** Incorporates internal resistance to calculate the realistic voltage observed at the battery terminals.
* **Customizable Current Profiles:** Allows users to define time-varying charge and discharge currents.
* **Visual Data Representation:** Generates plots for SoC, Terminal Voltage, and Current over the simulation period using Matplotlib.

## Technical Skills Demonstrated

* **Electrical Engineering Fundamentals:** Understanding of battery behavior, State of Charge, Open Circuit Voltage, Internal Resistance, and current/voltage relationships.
* **Programming (Python):** Scripting, function definition, data structures (dictionaries, lists), numerical computation with NumPy.
* **Data Visualization:** Using Matplotlib for clear and informative graphical representation of simulation results.
* **Version Control (Git & GitHub):** Repository management, committing changes, pushing code to a remote repository, and collaborative development readiness.
* **Simulation & Modeling:** Ability to translate real-world electrical systems into simplified mathematical models for analysis.

## Getting Started

### Prerequisites

* Python 3.x
* `numpy` library (`pip install numpy`)
* `matplotlib` library (`pip install matplotlib`)

### Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourGitHubUsername/EV-Battery-Simulator.git](https://github.com/YourGitHubUsername/EV-Battery-Simulator.git)
    cd EV-Battery-Simulator
    ```
    (Replace `YourGitHubUsername` and `EV-Battery-Simulator` with your actual GitHub username and repository name.)

2.  **Install dependencies:**
    ```bash
    pip install numpy matplotlib
    ```

### Usage

To run the simulation and generate plots:

```bash
python battery_simulator.py
