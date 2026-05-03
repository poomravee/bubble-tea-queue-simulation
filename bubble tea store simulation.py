# MSE 131 Final Project
# Name: Marcus Chuthamsatid
# Bubble Tea Shop Queue Simulation

# This program simulates a bubble tea shop over an 8-hour (480 minute) day.
# Customers arrive randomly, join a queue, and get served by one or more workers.
# We run the simulation 30 times and average the results to get stable numbers.


import random

SIM_MINUTES  = 480   # Length of one workday (8 hours x 60 minutes)
REPLICATIONS = 30    # How many times we repeat the simulation and average

#  Extension 1: Rush Hour 
RUSH_START = 150     # Rush hour begins at minute 150 (2.5 hours into the day)
RUSH_END   = 210     # Rush hour ends at minute 210 (3.5 hours into the day)

# Extension 3: Worker Break
BREAK_START = 240    # One worker's break begins at minute 240 (4 hours in)
BREAK_END   = 270    # One worker's break ends at minute 270 (30-minute break)

# Extension 4: Mobile Orders 
MOBILE_PROB = 0.10   # Each minute, there is a 10% chance a mobile order arrives

# Extension 5: Slow Service When Busy 
SLOW_THRESHOLD = 5   # If queue reaches 5+ people, service slows down
SLOW_FACTOR    = 1.5 # Service time is multiplied by 1.5x when queue is long


# Frun_simulation
# Runs a single 480-minute simulation day and returns performance results.
# Parameters:
#  arrival_prob     chance a walk-in customer arrives each minute (e.g. 0.25)
#  num_servers      how many workers are on shift 
#  rush_hour        True/False: turn rush hour on or off        (Extension 1)
#  two_types        True/False: simple vs complex drinks on/off  (Extension 2)
#  worker_break     True/False: turn worker break on or off      (Extension 3)
#  mobile_orders    True/False: turn mobile orders on or off     (Extension 4)
#  congestion_slow  True/False: slow service when busy on/off    (Extension 5)
#  seed             random seed so each replication is different but repeatable


# run one simulation
def run_simulation(arrival_prob, num_servers,
                   rush_hour=True,
                   worker_break=True,
                   mobile_orders=True,
                   two_types=True,
                   congestion_slow=True,
                   seed=None):

    random.seed(seed)

    servers = [0] * num_servers
    queue = []

    total_wait = 0
    customers_arrived = 0
    customers_served = 0
    total_queue_length = 0
    max_queue_length = 0
    busy_minutes = [0] * num_servers

    for minute in range(SIM_MINUTES):

        # Extension 3: Worker Break
        # During the break window, one fewer worker is available.
        # We always keep at least 1 worker so the shop does not fully stop.

        active_servers = num_servers
        if worker_break and BREAK_START <= minute < BREAK_END:
            active_servers = max(1, num_servers - 1)

        # Extension 1: Rush Hour
        # During the rush hour window, arrival probability doubles.
        # Capped at 95% to keep some randomness.
        current_pro = arrival_prob
        if rush_hour and RUSH_START <= minute < RUSH_END:
            current_pro = min(arrival_prob * 2, 0.95)

        #walk in customer arrival
        if random.random() < current_pro:
            # Extension 2: Two Customer Types
            # 60% of customers order simple drinks (2–4 min to make).
            # 40% order complex drinks (4–7 min to make).
            # If two_types is OFF, all customers are treated as simple orders.
            if two_types:
                if random.random() < 0.60:
                    drink = "simple"
                else:
                    drink = "complex"
            else:
                drink = "simple"

            queue.append([minute, drink])
            customers_arrived += 1

        # Extension 4: Mobile Orders
        # Each minute there is a 10% chance a mobile order also arrives.
        # Mobile orders join the same queue as walk-ins
        if mobile_orders and random.random() < MOBILE_PROB:
            if two_types:
                if random.random() < 0.60:
                    drink = "simple"
                else:
                    drink = "complex"
            else:
                drink = "simple"

            queue.append([minute, drink])
            customers_arrived += 1

        # serve customers
        # Check each active server; if they are free and someone is waiting, serve them.
        for i in range(active_servers):
            if servers[i] <= minute and len(queue) > 0:

                customer = queue.pop(0)
                arrival_time = customer[0]
                drink_type = customer[1]

                wait_time = minute - arrival_time
                total_wait += wait_time

                if drink_type == "simple":
                    service_time = random.randint(2, 4)
                else:
                    service_time = random.randint(4, 7)


                # Extension 5: Slow Service When Queue Is Long
                # When 5+ customers are waiting, the worker is under pressure
                # and makes drinks 50% slower (service_time x 1.5).
                # This creates a feedback loop: long queue --> slower service --> longer queue.

                if congestion_slow and len(queue) >= SLOW_THRESHOLD:
                    service_time = int(service_time * SLOW_FACTOR)

                if service_time < 1:
                    service_time = 1

                servers[i] = minute + service_time
                customers_served += 1

        # track busy time
        for i in range(num_servers):
            if servers[i] > minute:
                busy_minutes[i] += 1

        # track queue length
        total_queue_length += len(queue)
        if len(queue) > max_queue_length:
            max_queue_length = len(queue)



    # Average waiting time: total wait ÷ number of customers served
    avg_wait = total_wait / customers_served if customers_served > 0 else  0

    # Average queue length: sum of queue each minute ÷ total minutes
    avg_queue = total_queue_length / SIM_MINUTES

    # Server utilization: fraction of time servers were actively making drinks
    utilization = sum(busy_minutes) / (num_servers * SIM_MINUTES) if num_servers > 0 else 0

    # Service rate: what fraction of arriving customers were actually served
    service_rate = customers_served / customers_arrived if customers_arrived > 0 else 0

    return{
        "arrived":       customers_arrived,
        "served":        customers_served,
        "avg_wait":      round(avg_wait, 2),
        "avg_queue":     round(avg_queue, 2),
        "max_queue":     max_queue_length,
        "utilization":   round(utilization * 100, 1),
        "service_rate":  round(service_rate, 2),
        "left_in_queue": len(queue)
    }
    


# Runs the simulation many times and returns the average of all results.
# Using 30 replications
def replicate(arrival_prob, num_servers, replications=REPLICATIONS, **kwargs):

    totals = {
        "arrived": 0, "served": 0, "avg_wait": 0, "avg_queue": 0,
        "max_queue": 0, "utilization": 0, "service_rate": 0, "left_in_queue": 0
    }

    for r in range(replications):
        result = run_simulation(arrival_prob, num_servers, seed = r + 1, **kwargs)
        for key in totals:
            totals[key] += result[key]

    return {key: round(totals[key] / replications, 2) for key in totals}


# Prints a clean, aligned table

def print_table(title, headers, rows):
    col_w = 16

    print("\n" + "=" * (col_w * len(headers)))
    print(title)
    print("=" * (col_w * len(headers)))
    print("".join(str(h).ljust(col_w) for h in headers))
    print("-" * (col_w * len(headers)))
    for row in rows:
        print("".join(str(item).ljust(col_w) for item in row))

# Experiment 1  Scenario Comparison
# Compare three operating situations with all extension off.
# Scenario 1  Baseline:    1 worker, arrival prob = 0.25
# Scenario 2  High Demand: 1 worker, arrival prob = 0.35
# Scenario 3  Two Workers: 2 workers, arrival prob = 0.25

def experiment_1_scenarios():
    no_ext = dict(rush_hour=False, two_types=False,
                  worker_break=False, mobile_orders=False, congestion_slow=False)
    
    baseline    = replicate(0.25, 1, **no_ext)   # Scenario 1: Baseline
    high_demand = replicate(0.35, 1, **no_ext)   # Scenario 2: High demand
    two_workers = replicate(0.25, 2, **no_ext)   # Scenario 3: Two workers

    headers = ["Scenario", "Avg Wait", "Avg Queue", "Util %", "Served", "Svc Rate"]

    rows = [
        ["Baseline",    baseline["avg_wait"],    baseline["avg_queue"],
         str(baseline["utilization"]) + "%",    baseline["served"],    baseline["service_rate"]],
        ["High Demand", high_demand["avg_wait"], high_demand["avg_queue"],
         str(high_demand["utilization"]) + "%", high_demand["served"], high_demand["service_rate"]],
        ["Two Workers", two_workers["avg_wait"], two_workers["avg_queue"],
         str(two_workers["utilization"]) + "%", two_workers["served"], two_workers["service_rate"]],
    ]

    print_table("Experiment 1: Scenario Comparion (all extensions OFF)", headers, rows)

# Experiment 2 — Baseline vs Full Model
# Shows the combined effect of turning on all five extensions at once.
# Both runs use 1 server and arrival prob = 0.25 so we isolate the extensions.

def experiment_2_extensions():

    no_ext  = dict(rush_hour=False, two_types=False,
                   worker_break=False, mobile_orders=False, congestion_slow=False)
    all_ext = dict(rush_hour=True,  two_types=True,
                   worker_break=True,  mobile_orders=True,  congestion_slow=True)

    baseline   = replicate(0.25, 1, **no_ext)    # Clean baseline
    full_model = replicate(0.25, 1, **all_ext)   # All five extensions active

    headers = ["Model", "Avg Wait", "Avg Queue", "Util %", "Served", "Max Queue", "Left in Q"]

    rows = [
        ["Baseline",   baseline["avg_wait"],   baseline["avg_queue"],
         str(baseline["utilization"]) + "%",   baseline["served"],
         baseline["max_queue"],   baseline["left_in_queue"]],
        ["Full Model", full_model["avg_wait"],  full_model["avg_queue"],
         str(full_model["utilization"]) + "%",  full_model["served"],
         full_model["max_queue"],  full_model["left_in_queue"]],
    ]

    print_table("Experiment 2: Baseline vs Full Extensions Model", headers, rows)


# Experiment 3 — Sensitivity Analysis
# We change ONE parameter at a time and watch how results change.
# All five extensions are ON for both parts of this experiment
# Part A: Vary arrival probability from 0.15 to 0.40  (1 server)
# Part B: Vary number of servers from 1 to 3 (arrival prob = 0.30)

def experiment_3_sensitivity():
    all_ext = dict(rush_hour=True,  two_types=True,
                   worker_break=True,  mobile_orders=True,  congestion_slow=True)
    # Part A: Vary arrival probability
    # Shows how wait time and queue grow as the shop gets busier
    headers_a = ["Arrival Prob", "Avg Wait", "Avg Queue", "Util %", "Served", "Svc Rate"]
    rows_a = []

    for prob in [0.15,0.20,0.25,0.30,0.35,0.40]:
        r = replicate(prob, 1 , **all_ext)
        rows_a.append([prob,
                        r["avg_wait"], r["avg_queue"],
                        str(r["utilization"]) + "%",
                        r["served"], r["service_rate"]])
        
    print_table("Experiment 3A: Sensitivity — Arrival Probability  (1 server, all extensions ON)", headers_a, rows_a)

    # Part B: Vary number of servers
    # Shows how adding workers reduces wait time and increases throughput
    headers_b = ["Num Servers", "Avg Wait", "Avg Queue", "Util %", "Served", "Svc Rate"]
    rows_b = []

    for n in [1, 2, 3]:
        r = replicate(0.30, n , **all_ext)
        rows_b.append([n,
                        r["avg_wait"], r["avg_queue"],
                        str(r["utilization"]) + "%",
                        r["served"], r["service_rate"]])
        
    print_table("Experiment 3B: Sensitivity — Number of Servers  (prob = 0.30, all extensions ON)", headers_b, rows_b)




def main():
    print("  MSE 131 — Bubble Tea Shop Queue Simulation")
    print(f"  {SIM_MINUTES}-minute day | {REPLICATIONS} replications per experiment")

    experiment_1_scenarios()    # Experiment 1
    experiment_2_extensions()   # Experiment 2
    experiment_3_sensitivity()  # Experiment 3

    print("\nSimulation complete.")


if __name__ == "__main__":
    main()
