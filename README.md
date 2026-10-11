# Rocket Landing Optimiser 🚀

A Python simulation investigating how a rocket can land safely while minimising fuel consumption. The project combines Newtonian mechanics, numerical simulation, a simple feedback controller, and constrained optimisation.

## Overview

A rocket begins at a height of 100 metres with zero initial velocity. Gravity accelerates it towards the ground, while an engine can generate upward thrust to slow its descent. Firing the engine too early can waste fuel; firing it too late can result in an unsafe landing.

The aim is to find a **landing-controller safety factor** that minimises fuel consumption while keeping the magnitude of the rocket's impact velocity at or below **2 m/s**.

The program simulates the descent for different safety factors, identifies the lowest-fuel safe landing among those tested, and plots the resulting height and velocity over time.

## Mathematical Model

The simulation considers one-dimensional vertical motion. Upward is the positive direction.

### Newton's second law

When the engine is off, the rocket accelerates downwards:

$$
a=-g
$$

When the engine is on, its upward acceleration is:

$$
a=\frac{T}{m}-g
$$

where:

- $T$ is the engine thrust (15,000 N),
- $m$ is the rocket's current mass (kg),
- $g$ is gravitational acceleration (9.81 m/s²).

The mass changes as fuel is consumed:

$$
m=m_{\mathrm{dry}}+m_{\mathrm{fuel}}
$$

The model uses a constant fuel-burn rate of 10 kg/s whenever the engine is firing. Because the mass decreases during a burn, the acceleration produced by a fixed thrust increases slightly over time.

### Numerical simulation

The motion is calculated in small time steps of $\Delta t=0.001$ s. Over each step, acceleration is treated as constant:

$$
h_{\mathrm{next}}=h+v\Delta t+\frac12 a(\Delta t)^2
$$

$$
v_{\mathrm{next}}=v+a\Delta t
$$

The program updates the rocket's height, velocity, remaining fuel and elapsed time until it reaches the ground (or the simulation time limit is reached). It also shortens the final time step approximately when the calculated height crosses zero.

## Landing Controller

The engine is controlled using an estimate of the distance required to stop the rocket.

From the constant-acceleration equation

$$
v_f^2=v_i^2+2as,
$$

setting the final velocity to zero gives the estimated stopping distance:

$$
d_{\mathrm{stop}}=\frac{v^2}{2a_{\mathrm{brake}}},
\qquad
a_{\mathrm{brake}}=\frac{T}{m}-g.
$$

This estimate is used only while the rocket is descending and the available thrust produces a positive upward acceleration.

The controller switches the engine on when

$$
h\leq k\,d_{\mathrm{stop}},
$$

provided fuel remains and the rocket is descending. Here, $k$ is a **safety factor**. The condition is checked again at every time step, so the engine can switch on and off during descent.

The stopping-distance formula is an approximation because it assumes constant acceleration, whereas the rocket's mass changes as fuel burns.

## Fuel Optimisation

For each candidate safety factor $k$, the program simulates a complete descent and measures the fuel consumed, $F(k)$.

The numerical optimisation problem is:

$$
\min_k F(k)
$$

subject to

$$
|v_{\mathrm{impact}}(k)|\leq 2\ \mathrm{m/s}
$$

and the rocket successfully reaching the ground.

The program searches **201 safety factors from 0.900 to 1.100 inclusive, in increments of 0.001**. It selects the safe result with the lowest fuel consumption in this tested range. This is a discrete parameter search, not a proof of a globally optimal landing strategy.

## Results

With the parameters in `rocket.py`, the best result found in the search is:

| Quantity | Value |
| --- | ---: |
| Initial height | 100 m |
| Initial mass | 1,000 kg |
| Initial fuel | 300 kg |
| Maximum allowed impact speed | 2.000 m/s |
| Best safety factor tested | **0.960** |
| Impact speed | **1.975 m/s** |
| Fuel consumed | **44.339 kg** |
| Flight time | 7.136 s |
| Engine burn time | 4.434 s |
| Final mass | 955.661 kg |

The selected controller satisfies the landing-speed constraint while using the least fuel of the safe candidates tested. This illustrates an important trade-off: achieving the softest possible landing is not necessarily the same as minimising fuel consumption.

The script also displays two plots for the selected trajectory:

- **Height against time**, showing the descent to ground level.
- **Velocity against time**, showing the acceleration and braking behaviour.

## Assumptions and Limitations

This is an educational model rather than a realistic rocket flight simulator. In particular:

- Motion is restricted to **one vertical dimension**; horizontal motion and rotation are ignored.
- Gravitational acceleration is constant, and **air resistance is neglected**.
- The engine provides either a fixed 15,000 N of thrust or no thrust; intermediate thrust settings are not modelled.
- Fuel burns at a constant rate whenever the engine is on.
- The stopping-distance calculation assumes constant acceleration, even though the mass changes during a burn.
- The numerical model uses finite time steps and an approximate final-step correction.
- The optimisation searches a **limited, discrete range of safety factors** rather than all possible control strategies.

Possible extensions include testing different initial conditions, measuring sensitivity to time-step size, comparing alternative control laws, and optimising a variable-thrust profile.

## How to Run

**Requirements:** Python 3 and Matplotlib.

1. Download or clone this repository.
2. Install Matplotlib:

   ```bash
   python3 -m pip install matplotlib
   ```

3. Run the simulation:

   ```bash
   python3 rocket.py
   ```

The program prints results for each tested safety factor, displays the best safe result, and opens two Matplotlib plots.

## Project Notes

This project was developed as an exploration of the relationship between mathematical modelling, feedback control, and numerical optimisation. AI assistance was used during debugging.

