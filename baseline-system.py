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
