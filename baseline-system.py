import random

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

average_waiting_time = sum(waiting_times) / num_customers
average_time_in_system = sum(time_in_system) / num_customers

total_busy_time = sum(service_times)
total_simulation_time = departure_times[-1] - arrival_times[0]
utilization = total_busy_time / total_simulation_time

throughput = num_customers / total_simulation_time


# 7. Print customer results

print("Customer Data")
print("----------------------------------------------------------------------------------------------------------")
print("Customer # | Interarrival Time | Arrival Time | Service Time | Start Time | Depart Time | Wait Time | Time in System")

for i in range(num_customers):
    print(
        f"{i+1:>4} |"
        f"{interarrival_times[i]:>13} |"
        f"{arrival_times[i]:>8} |"
        f"{service_times[i]:>8} |"
        f"{service_start_times[i]:>6} |"
        f"{departure_times[i]:>7} |"
        f"{waiting_times[i]:>5} |"
        f"{time_in_system[i]:>14}"
    )
