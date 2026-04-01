import random

# ** Terminal must be fully extended in order to see the baseline system in the correct formatting**

# This program simulates a bubble tea shop checkout system with five extensions:
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

import random

# 1. Model set up

num_customers = 100

# Break settings for cashier 2
break_start = 20
break_end = 35

# Abandonment settings
max_queue_length = 5
max_wait_time = 8

# Lists to store data for each customer
customer_numbers = []
customer_types = []
interarrival_times = []
arrival_times = []
service_times = []
service_start_times = []
departure_times = []
waiting_times = []
time_in_system = []
customer_status = []

# 2. Generate arrival times and customer types

priority_rate = 0.35  # number to be changed for different scenarios

current_time = 0

for i in range(num_customers):
    # Rush-hour arrival demands
    interarrival = random.randint(2, 4)

    current_time += interarrival

    # Customer type
    if random.random() < priority_rate:
        cust_type = "Priority"
    else:
        cust_type = "Regular"

    # Service time depends on customer type
    if cust_type == "Priority":
        service = random.randint(1, 4)   # faster mobile pickup process time
    else:
        service = random.randint(6, 10)   # regular walk-in order process time

    customer_numbers.append(i + 1)
    interarrival_times.append(interarrival)
    arrival_times.append(current_time)
    service_times.append(service)
    customer_types.append(cust_type)

# 3. Simulation

cashier1_available = 0
cashier2_available = 0

served = [False] * num_customers
balked = [False] * num_customers
reneged = [False] * num_customers
assigned_cashier = [None] * num_customers

for i in range(num_customers):

    arrival = arrival_times[i]

    # Count how many earlier customers are still not completed
    queue_length = 0
    for j in range(i):
        if not served[j] and not balked[j] and not reneged[j]:
            queue_length += 1

    # Extension 5: Balking
    if queue_length > max_queue_length:
        balked[i] = True
        service_start_times.append(None)
        departure_times.append(None)
        waiting_times.append(None)
        time_in_system.append(None)
        assigned_cashier[i] = None
        customer_status.append("Balked")
        continue

    # Handle cashier 2 break
    if break_start <= arrival <= break_end:
        cashier2_available = max(cashier2_available, break_end)

    # Choose cashier with earlier availability
    if cashier1_available <= cashier2_available:
        start_time = max(arrival, cashier1_available)
        cashier = 1
    else:
        start_time = max(arrival, cashier2_available)
        cashier = 2

    wait = start_time - arrival

    # Extension 5: Reneging
    if wait > max_wait_time:
        reneged[i] = True
        service_start_times.append(None)
        departure_times.append(None)
        waiting_times.append(wait)
        time_in_system.append(None)
        assigned_cashier[i] = None
        customer_status.append("Reneged")
        continue

    # Serve customer
    finish = start_time + service_times[i]

    service_start_times.append(start_time)
    departure_times.append(finish)
    waiting_times.append(wait)
    time_in_system.append(finish - arrival)
    assigned_cashier[i] = cashier
    served[i] = True
    customer_status.append("Served")

    # Update cashier availability
    if cashier == 1:
        cashier1_available = finish
    else:
        cashier2_available = finish

# 4. Calculate performance ratings

served_count = 0
balked_count = 0
reneged_count = 0
total_wait = 0
total_time_system = 0
busy_time_1 = 0
busy_time_2 = 0

for i in range(num_customers):
    if served[i]:
        served_count += 1
        total_wait += waiting_times[i]
        total_time_system += time_in_system[i]

        if assigned_cashier[i] == 1:
            busy_time_1 += service_times[i]
        elif assigned_cashier[i] == 2:
            busy_time_2 += service_times[i]

    elif balked[i]:
        balked_count += 1

    elif reneged[i]:
        reneged_count += 1

if served_count > 0:
    average_waiting_time = total_wait / served_count
    average_time_in_system = total_time_system / served_count

    valid_departures = []
    for t in departure_times:
        if t is not None:
            valid_departures.append(t)

    total_simulation_time = max(valid_departures) - min(arrival_times)

    utilization_cashier1 = busy_time_1 / total_simulation_time
    utilization_cashier2 = busy_time_2 / total_simulation_time
    overall_utilization = (busy_time_1 + busy_time_2) / (2 * total_simulation_time)

    throughput = served_count / total_simulation_time
else:
    average_waiting_time = 0
    average_time_in_system = 0
    utilization_cashier1 = 0
    utilization_cashier2 = 0
    overall_utilization = 0
    throughput = 0

# 5. Print customer results

print("Customer Data")
print("-" * 160)
print("Customer # | Type      | Interarrival Time | Arrival Time | Service Time | Start Time | Depart Time | Wait Time | Time in System | Status   | Cashier")
print("-" * 160)

for i in range(num_customers):
    start_val = service_start_times[i] if service_start_times[i] is not None else "-"
    depart_val = departure_times[i] if departure_times[i] is not None else "-"
    wait_val = waiting_times[i] if waiting_times[i] is not None else "-"
    system_val = time_in_system[i] if time_in_system[i] is not None else "-"
    cashier_val = assigned_cashier[i] if assigned_cashier[i] is not None else "-"

    print(
        f"{customer_numbers[i]:>10} | "
        f"{customer_types[i]:<9} | "
        f"{interarrival_times[i]:>17} | "
        f"{arrival_times[i]:>12} | "
        f"{service_times[i]:>12} | "
        f"{str(start_val):>10} | "
        f"{str(depart_val):>11} | "
        f"{str(wait_val):>9} | "
        f"{str(system_val):>14} | "
        f"{customer_status[i]:<8} | "
        f"{str(cashier_val):>7}"
    )

# 6. Print summary results

print("\nSummary Performance Measures")
print("-" * 45)
print("Customers served:", served_count)
print("Customers who balked:", balked_count)
print("Customers who reneged:", reneged_count)
print("Average waiting time:", round(average_waiting_time, 2), "minutes")
print("Average time in system:", round(average_time_in_system, 2), "minutes")
print("Cashier 1 utilization:", round(utilization_cashier1, 2))
print("Cashier 2 utilization:", round(utilization_cashier2, 2))
print("Overall system utilization:", round(overall_utilization, 2))
print("Throughput:", round(throughput, 2), "customers per minute")