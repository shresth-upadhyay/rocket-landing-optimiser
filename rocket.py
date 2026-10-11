
import matplotlib.pyplot as plt

# --------------------
# Rocket constants
# --------------------

THRUST = 15000.0          # Newtons
GRAVITY = 9.81            # m/s^2
DT = 0.001                # seconds
FUEL_BURN_RATE = 10.0     # kg/s

DRY_MASS = 700.0          # kg
INITIAL_FUEL = 300.0      # kg
INITIAL_HEIGHT = 100.0    # metres

SAFE_LANDING_SPEED = 2.0  # m/s


# --------------------
# Rocket simulation
# --------------------

def simulate(safety_factor):

    # Initial state
    height = INITIAL_HEIGHT
    velocity = 0.0
    time = 0.0

    fuel = INITIAL_FUEL
    burn_time = 0.0

    # Record the rocket's trajectory
    times = [time]
    heights = [height]
    velocities = [velocity]
    masses = [DRY_MASS + fuel]

    # Continue until landing (or the time limit)
    while height > 0 and time < 120:

        mass = DRY_MASS + fuel

        # Acceleration when the engine is firing
        braking_acceleration = THRUST / mass - GRAVITY

        # Calculate the distance required to stop
        if velocity < 0 and braking_acceleration > 0:
            stopping_distance = velocity**2 / (2 * braking_acceleration)
        else:
            stopping_distance = 0.0

        # Decide whether to fire the engine
        engine_on = (
            fuel > 0
            and velocity < 0
            and height <= safety_factor * stopping_distance
        )

        # Calculate actual acceleration
        if engine_on:
            acceleration = braking_acceleration
        else:
            acceleration = -GRAVITY

        # Predict the next height
        next_height = (
            height
            + velocity * DT
            + 0.5 * acceleration * DT**2
        )

        # Shorten the last step if the rocket reaches the ground
        step_dt = DT

        if next_height <= 0:
            fraction = height / (height - next_height)
            step_dt = DT * fraction
            next_height = 0.0

        # Update velocity
        next_velocity = velocity + acceleration * step_dt

        # Consume fuel only when the engine is firing
        if engine_on:
            fuel_used_this_step = min(
                fuel,
                FUEL_BURN_RATE * step_dt
            )

            fuel -= fuel_used_this_step
            burn_time += step_dt

        # Update the rocket's state
        time += step_dt
        height = next_height
        velocity = next_velocity

        # Store values for plotting
        times.append(time)
        heights.append(height)
        velocities.append(velocity)
        masses.append(DRY_MASS + fuel)

    # Return the results in a dictionary
    return {
        "impact_velocity": velocity,
        "flight_time": time,
        "fuel_used": INITIAL_FUEL - fuel,
        "burn_time": burn_time,
        "final_mass": DRY_MASS + fuel,
        "times": times,
        "heights": heights,
        "velocities": velocities,
        "masses": masses,
        "landed": height == 0
    }


# --------------------
# Optimisation
# --------------------

safety_factors = [i / 1000 for i in range(900, 1101)]

best_safety_factor = None
best_fuel = float("inf")

for safety_factor in safety_factors:

    result = simulate(safety_factor)

    impact_speed = abs(result["impact_velocity"])
    fuel_used = result["fuel_used"]

    print(f"Safety factor: {safety_factor:.1f}")
    print(f"Impact speed: {impact_speed:.3f} m/s")
    print(f"Fuel used: {fuel_used:.3f} kg")
    print()

    # Accept only successful, safe landings
    if result["landed"] and impact_speed <= SAFE_LANDING_SPEED:

        if fuel_used < best_fuel:
            best_fuel = fuel_used
            best_safety_factor = safety_factor


# --------------------
# Display the best result
# --------------------

if best_safety_factor is not None:

    best_result = simulate(best_safety_factor)

    print("--------------------")
    print("BEST RESULT")
    print("--------------------")

    print(f"Safety factor: {best_safety_factor:.3f}")
    print(f"Impact speed: {abs(best_result['impact_velocity']):.3f} m/s")
    print(f"Fuel used: {best_result['fuel_used']:.3f} kg")
    print(f"Flight time: {best_result['flight_time']:.3f} s")
    print(f"Burn time: {best_result['burn_time']:.3f} s")
    print(f"Final mass: {best_result['final_mass']:.3f} kg")

    # Height graph
    plt.figure()
    plt.plot(best_result["times"], best_result["heights"])
    plt.xlabel("Time (s)")
    plt.ylabel("Height (m)")
    plt.title("Optimised Rocket Landing: Height")
    plt.grid(True)

    # Velocity graph
    plt.figure()
    plt.plot(best_result["times"], best_result["velocities"])
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Optimised Rocket Landing: Velocity")
    plt.grid(True)

    plt.show()

else:
    print("No safe landing found.")
