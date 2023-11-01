import numpy as np
import matplotlib.pyplot as plt

# Constants
Henry_Constant = 3.3e-2  # Henry's Law constant in mol/(L*atm) for CO2 at 25°C
K1 = 2.5e-4             # First dissociation constant of carbonic acid
K2 = 5.6e-7             # Second dissociation constant of carbonic acid
Kw = 1e-14              # Ion product of water
S0 = 35                 # Reference salinity in PSU
T0 = 25                 # Reference temperature in °C
R = 8.314               # Universal gas constant in J/(mol*K)
density_sw = 1025       # Seawater density in kg/m^3
molar_mass_CO2 = 0.044  # Molar mass of CO2 in kg/mol
K0 = 0.03 

# Initial conditions
pH_initial = 8.1        # Initial seawater pH
CO2_initial = 400       # Initial atmospheric CO2 concentration in ppm
temperature_initial = 25 # Initial seawater temperature in °C

# Simulation parameters
num_years = 100          # Number of years to simulate
time_step = 1            # Time step in years
years = np.arange(0, num_years, time_step)
CO2_levels = np.zeros_like(years)
pH_levels = np.zeros_like(years)

# Initialize parameters
CO2 = CO2_initial / 1e6   # Convert ppm to atm
pH = pH_initial
temperature = temperature_initial
S = S0                    # Salinity (constant for simplicity)

# Biological processes (photosynthesis and respiration)
photosynthesis_rate = 0.01  # Rate of photosynthesis (hypothetical value)
respiration_rate = 0.02     # Rate of respiration (hypothetical value)

# Run the simulation
for i in range(len(years)):
    # Calculate [CO3_2-] from pH
    H_concentration = 10**(-pH)
    OH_concentration = Kw / H_concentration
    CO3_2_concentration = (K1 * H_concentration**2) / (H_concentration + K1 * K2)
    
    # Calculate alkalinity
    Alkalinity = (2 * CO3_2_concentration + H_concentration - OH_concentration) * S
    
    # Calculate CO2 concentration in seawater
    CO2_sw = CO2 / (1 + (CO2 / (K0 + (K1 / H_concentration) + (K2 / (H_concentration**2)))))
    
    # Calculate new pH using alkalinity, CO2, and other factors
    H_concentration_new = (Alkalinity + CO2_sw - OH_concentration) / (S * Kw)
    
    # Update pH due to biological processes (photosynthesis and respiration)
    pH += (photosynthesis_rate - respiration_rate) * time_step
    
    # Update CO2 concentration (for simplicity, we assume a linear increase)
    CO2 += 2.15e-6 * time_step  # 2.15 ppm per year (realistic CO2 increase rate)
    
    # Store data for plotting
    CO2_levels[i] = CO2 * 1e6  # Convert back to ppm
    pH_levels[i] = pH

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(years, CO2_levels, label='CO2 Concentration (ppm)')
plt.plot(years, pH_levels, label='Seawater pH')
plt.xlabel('Years')
plt.ylabel('Concentration / pH')
plt.legend()
plt.title('Advanced Ocean Acidification Model with Biological Processes')
plt.grid(True)
plt.show()
