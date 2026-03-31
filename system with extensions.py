import random

# This program simulates a coffee shop checkout system with five extensions:
# 1. Rush-Hour Arrivals (Demand Variation)
# 2. Second Cashier (Increased Capacity)
# 3. Worker Break (Temporary Reduced Capacity)
# 4. Mobile Orders (Priority Rules)
# 5. Customer Abandonment (Customer Response to Congestion)

# Customers arrive at different rates depending on the time of day.
# Some customers are mobile-order customers and receive priority service.
# Two cashiers are available, but one cashier takes a break during a set time interval.
# Customers may choose not to join the line if it is too long, or leave if they wait too long.
# The model tracks waiting time, time in system, throughput, and cashier utilization.


# 1. Model set up

num_customers = 30  # number of customers to simulate

# Break settings for cashier 2
break_start = 20
break_end = 35

# Abandonment settings
max_queue_length = 5       # if queue is longer than this, customer will not join
max_wait_time = 8          # if wait is longer than this, customer leaves

# Lists to store data for each customer
interarrival_times = []
arrival_times = []
service_times = []
service_start_times = []
departure_times = []
waiting_times = []
time_in_system = []



# 2. Generate service and arrival times

current_time = 0

for i in range(num_customers):
    # Rush-hour arrivals:
    # If current time is during rush hour, customers arrive faster
    if 15 <= current_time <= 40:
        interarrival = random.randint(1, 2)   # to simulate busy period
    else:
        interarrival = random.randint(3, 5)   # to simulate off-peak period

    current_time += interarrival

    # Random service time
    service = random.randint(2, 6)

    # Mobile order customers (priority customers)
    # Assume 30% chance customer is a mobile-order pickup
    if random.random() < 0.3:
        cust_type = "Priority"
    else:
        cust_type = "Regular"

    customer_numbers.append(i + 1)
    interarrival_times.append(interarrival)
    arrival_times.append(current_time)
    service_times.append(service)
    customer_types.append(cust_type)


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