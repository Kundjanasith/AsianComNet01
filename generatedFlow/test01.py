# Given parameters
data_size_MB = 10
data_rate_Gbps = 10
distance_AB_km = 2800
distance_AC_km = 300

# Constants
speed_of_light_mps = 3 * 10**8  # Speed of light in meters per second

# Calculate propagation delays
propagation_delay_AB = distance_AB_km * 1000 / speed_of_light_mps  # Convert km to meters
propagation_delay_AC = distance_AC_km * 1000 / speed_of_light_mps  # Convert km to meters

# Calculate transmission times
transmission_time = data_size_MB * 8 / (data_rate_Gbps * 10**9)  # Convert MB to bits and Gbps to bps

# Calculate total transmission times
total_transmission_time_AB = propagation_delay_AB + transmission_time
total_transmission_time_AC = propagation_delay_AC + transmission_time

# Output results
print(f"Total Transmission Time (A to B): {total_transmission_time_AB:.5f} seconds")
print(f"Total Transmission Time (A to C): {total_transmission_time_AC:.5f} seconds")


# Given parameters
data_size_kbit = 10
data_rate_Gbps = 10
distance_AB_km = 2800
distance_AC_km = 300

# Constants
speed_of_light_mps = 3 * 10**8  # Speed of light in meters per second

# Calculate propagation delays
propagation_delay_AB = distance_AB_km * 1000 / speed_of_light_mps  # Convert km to meters
propagation_delay_AC = distance_AC_km * 1000 / speed_of_light_mps  # Convert km to meters

# Calculate transmission times
transmission_time = data_size_kbit * 1000 / (data_rate_Gbps * 10**9)  # Convert kbit to bits and Gbps to bps

# Calculate total transmission times
total_transmission_time_AB = propagation_delay_AB + transmission_time
total_transmission_time_AC = propagation_delay_AC + transmission_time

# Output results
print(f"Total Transmission Time (A to B): {total_transmission_time_AB:.2e} seconds")
print(f"Total Transmission Time (A to C): {total_transmission_time_AC:.2e} seconds")
