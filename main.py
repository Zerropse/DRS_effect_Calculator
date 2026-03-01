import math
import numpy as np
import matplotlib.pyplot as plt

# --- CONSTANTS ---
AIR_DENSITY = 1.225
FRONTAL_AREA = 1.5
ENGINE_FORCE = 9000


def calculate_speed(cd):
    return math.sqrt((2 * ENGINE_FORCE) / (AIR_DENSITY * cd * FRONTAL_AREA))


def simulate_motion(v, distance):
    """Simulate constant speed motion"""
    distances = np.linspace(0, distance, 100)
    times = distances / v
    return distances, times


def drs_simulation(cd_no_drs, cd_drs, distance):
    v_no_drs = calculate_speed(cd_no_drs)
    v_drs = calculate_speed(cd_drs)

    t_no_drs = distance / v_no_drs
    t_drs = distance / v_drs

    speed_gain = v_drs - v_no_drs
    time_saved = t_no_drs - t_drs
    efficiency = (time_saved / t_no_drs) * 100

    return v_no_drs, v_drs, speed_gain, time_saved, efficiency


def plot_results(v_no_drs, v_drs, distance):
    d1, t1 = simulate_motion(v_no_drs, distance)
    d2, t2 = simulate_motion(v_drs, distance)

    plt.figure()

    plt.plot(t1, d1, label="No DRS")
    plt.plot(t2, d2, label="DRS")

    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.title("DRS vs No DRS Performance")

    plt.legend()
    plt.grid()

    plt.show()


def get_user_input():
    try:
        print("\n--- Enter Aerodynamic Values ---")
        cd_no_drs = float(input("Cd WITHOUT DRS (e.g. 1.0): "))
        cd_drs = float(input("Cd WITH DRS (e.g. 0.85): "))
        distance = float(input("Straight length (meters): "))

        if cd_drs >= cd_no_drs:
            print("⚠️ Warning: DRS should LOWER drag coefficient.\n")

        if distance <= 0:
            raise ValueError("Distance must be positive.")

        return cd_no_drs, cd_drs, distance

    except ValueError as e:
        print(f"\n❌ Invalid input: {e}\n")
        return None


def display_results(v_no_drs, v_drs, speed_gain, time_saved, efficiency):
    print("\n==============================")
    print("   DRS VISUAL REPORT")
    print("==============================")

    print(f"Top Speed (No DRS) : {v_no_drs*3.6:.2f} km/h")
    print(f"Top Speed (DRS)    : {v_drs*3.6:.2f} km/h")

    print(f"\nSpeed Gain         : {speed_gain:.2f} m/s")
    print(f"Time Saved         : {time_saved:.4f} s")
    print(f"Efficiency Gain    : {efficiency:.2f} %")

    print("==============================\n")


def main():
    print("🏎️ DRS Visual Simulator (Step 3)\n")

    while True:
        user_input = get_user_input()

        if user_input:
            cd_no_drs, cd_drs, distance = user_input

            v_no_drs, v_drs, speed_gain, time_saved, efficiency = drs_simulation(
                cd_no_drs, cd_drs, distance
            )

            display_results(v_no_drs, v_drs, speed_gain, time_saved, efficiency)

            # 📊 SHOW GRAPH
            plot_results(v_no_drs, v_drs, distance)

        choice = input("Run again? (y/n): ").lower()
        if choice != 'y':
            print("\n👋 Exiting... This is real engineering work now.")
            break


if __name__ == "__main__":
    main()