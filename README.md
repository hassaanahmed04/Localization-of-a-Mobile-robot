# Localization of a Mobile Robot Using EKF and Particle Filter

This repository provides a Python-based simulation of **2D localization** for a mobile robot operating in a bounded environment resembling a soccer field. The robot estimates its position using two popular probabilistic localization algorithms:

- **Extended Kalman Filter (EKF)**
- **Particle Filter (PF)**

The simulation accounts for **noisy motion (control inputs)** and **bearing-only observations** of known **landmarks**. It is ideal for understanding probabilistic robotics, state estimation, and sensor fusion concepts.

---

## Directory Structure

```
.
├── Dockerfile              # Docker setup
├── README.md               # Project documentation
├── ekf.py                  # EKF algorithm implementation
├── localization.py         # Main simulation entry point
├── pf.py                   # Particle Filter implementation
├── plot.py                 # Visualization utilities
├── policies.py             # Motion and control policy
├── requirements.txt        # Python dependencies
├── soccer_field.py         # Field and landmark setup
└── utils.py                # Helper functions
```

---

## Features

- Simulated 2D mobile robot in a landmark-based environment
- Realistic motion and sensor noise models
- Extended Kalman Filter (EKF) implementation for nonlinear state estimation
- Particle Filter (PF) implementation with customizable number of particles
- Real-time visualization of ground truth, measurements, and estimated trajectory
- Adjustable simulation parameters for experimentation

---

## How to Run the Simulation

Make sure you have Python installed along with necessary dependencies (e.g., `matplotlib`, `numpy`). Then, use the following commands to run the simulation:

### EKF Mode

Run the simulation using the Extended Kalman Filter with visualization:

```
python localization.py ekf --plot
```

---

## How to Run

Run the simulation with visualization:

```
python localization.py ekf --plot
python localization.py pf --plot
```

Run without visualization:

```
python localization.py ekf
```

Customize data and filter frequency:

```
python localization.py ekf --data-factor 4 --filter-factor 4
```

Run Particle Filter with custom particle count:

```
python localization.py pf --num-particles 500
python localization.py pf --num-particles 500 --plot
```

**Flags:**

- `--data-factor`: Controls the rate of input data (larger value = slower update)
- `--filter-factor`: Controls the frequency of EKF update steps
- `--num-particles`: Sets the number of particles used in the PF. More particles improve accuracy but increase computation.

---

## Running with Docker

To avoid dealing with Python dependencies manually, you can use Docker to build and run the simulation in a containerized environment.

### Step 1: Build the Docker image

```
docker build -t robot-localization .
```

### Step 2: Run the container

To run EKF with plotting:

```
docker run --rm -it robot-localization python localization.py ekf --plot
```

To run PF with 500 particles and visualization:

```
docker run --rm -it robot-localization python localization.py pf --num-particles 500 --plot
```
---
