import random

# This program simulates a coffee shop checkout system using a single cashier and a single waiting line. 
# Customers arrive at random times and require random service times, creating variability in the system. 
# The model tracks each customer's arrival time, service start time, and departure time to calculate waiting times and overall system performance.
# The key performance measures of this system includes average waiting time, time in system, server utilization, and throughput.
# This baseline model provides a simple representation of the application of real-world service system operates and serves as a foundation for further analysis and extensions. 


# 1. Model set up

num_customers = 20   # number of customers to simulate

# Lists to store data for each customer
interarrival_times = []
arrival_times = []
service_times = []
service_start_times = []
departure_times = []
waiting_times = []
time_in_system = []



# 2. Generate service and arrival times

for i in range(num_customers):
    # Random time between arrivals: 1 to 5 minutes intervals
    interarrival = random.randint(1, 5)
    interarrival_times.append(interarrival)

    # Random service time: 2 to 6 minutes intervals
    service = random.randint(2, 6)
    service_times.append(service)



# 3. Calculate arrival times

for i in range(num_customers):
    if i == 0:
        arrival_times.append(interarrival_times[i])
    else:
        arrival_times.append(arrival_times[i - 1] + interarrival_times[i])



# 4. Calculate service start times and departure times

for i in range(num_customers):
    if i == 0:
        # First customer starts service as soon as they arrive
        start_time = arrival_times[i]
    else:
        # Customer starts service either when they arrive
        # or when the previous customer leaves
        start_time = max(arrival_times[i], departure_times[i - 1])

    service_start_times.append(start_time)

    # Departure time = service start + service time
    finish_time = start_time + service_times[i]
    departure_times.append(finish_time)



# 5. Calculate waiting time and time in system

for i in range(num_customers):
    wait = service_start_times[i] - arrival_times[i]
    waiting_times.append(wait)

    total_time = departure_times[i] - arrival_times[i]
    time_in_system.append(total_time)



# 6. Calculate performace ratings

# Average waiting time - the average time customers spend in the queue before service begins
average_waiting_time = sum(waiting_times) / num_customers

# Average time in system - the total time from arrival to departure
average_time_in_system = sum(time_in_system) / num_customers

total_busy_time = sum(service_times)
total_simulation_time = departure_times[-1] - arrival_times[0]

# Server utilization - the proportion of time the cashier is actively serving customers
utilization = total_busy_time / total_simulation_time

# Throughput - the number of customers served per unit time
throughput = num_customers / total_simulation_time



# 7. Print customer results

print("Customer Data")
print("-" * 120)
print("Customer # | Interarrival Time | Arrival Time | Service Time | Start Time | Depart Time | Wait Time | Time in System")
print("-" * 120)

for i in range(num_customers):
    print(
        f"{i+1:>10} | "
        f"{interarrival_times[i]:>17} | "
        f"{arrival_times[i]:>12} | "
        f"{service_times[i]:>12} | "
        f"{service_start_times[i]:>10} | "
        f"{departure_times[i]:>11} | "
        f"{waiting_times[i]:>9} | "
        f"{time_in_system[i]:>15}"
    )


# 8. Print summary results

print("\nSummary Performance Measures")
print("-----------------------------------")
print("Average waiting time:", round(average_waiting_time, 2), "minutes")
print("Average time in system:", round(average_time_in_system, 2), "minutes")
print("Server utilization:", round(utilization, 2))
print("Throughput:", round(throughput, 2), "customers per minute")