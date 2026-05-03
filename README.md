# bubble-tea-queue-simulation
Python simulation project analyzing bubble tea shop queue performance, wait times, rush hour demand, and staffing scenarios.
# Bubble Tea Shop Queue Simulation

A discrete-event queue simulation built in Python for MSE 131 at the University of Waterloo. The simulation models a full 8-hour operating day at a bubble tea shop, tracking how customers arrive, wait, and get served — and how real-world factors like rush hours and worker breaks affect performance.


## What It Does

The simulation runs a minute-by-minute model of a bubble tea shop. Each minute, customers may arrive, join the queue, and get served by one or more workers. Results are averaged across **30 replications** to produce statistically stable outputs.

### Five Real-World Extensions

| # | Extension | Description |

 1  **Rush Hour** | Arrival probability doubles between minutes 150–210 |
 2  **Two Drink Types** | 60% simple orders (2–4 min), 40% complex orders (4–7 min) |
 3  **Worker Break** | One worker is unavailable from minutes 240–270 |
 4  **Mobile Orders** | 10% chance per minute of an additional mobile order arriving |
 5  **Congestion Slowdown** | When 5+ customers are queued, service time increases 1.5× |

## Experiments

### Experiment 1 — Scenario Comparison
Compares three operating situations with all extensions off:
- **Baseline** — 1 worker, arrival probability = 0.25
- **High Demand** — 1 worker, arrival probability = 0.35
- **Two Workers** — 2 workers, arrival probability = 0.25

### Experiment 2 — Baseline vs Full Model
Isolates the combined effect of all five extensions at once, using the same server count and arrival rate.

### Experiment 3 — Sensitivity Analysis
Changes one variable at a time with all extensions active:
- **Part A** — Arrival probability varied from 0.15 to 0.40 (1 server)
- **Part B** — Number of servers varied from 1 to 3 (arrival prob = 0.30)


## Output Metrics

| Metric | Description |

| `avg_wait` | Average customer wait time (minutes) |
| `avg_queue` | Average queue length across the day |
| `max_queue` | Peak queue length recorded |
| `utilization` | % of time servers were actively making drinks |
| `service_rate` | Fraction of arriving customers who were served |
| `left_in_queue` | Customers still waiting at the end of the day |


## How to Run

No dependencies required — uses Python's built-in `random` module only.


## Key Concepts

- **Discrete-event simulation** — state changes happen at each minute tick
- **Multi-server queue** — multiple workers serve customers in parallel
- **Stochastic arrivals** — customer arrivals and service times are randomized each run
- **Replication averaging** — 30 runs per experiment to reduce variance

## Author
**Marcus Chuthamsatid** — Management Engineering, University of Waterloo  

