import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# --- CONSTANTS ---
AIR_DENSITY = 1.225
FRONTAL_AREA = 1.5
ENGINE_FORCE = 8000
MASS = 800
DT = 0.05


# =========================
# SINGLE CAR SIM
# =========================
def simulate_run(cd, distance):
    v = 0
    x = 0
    t = 0

    speeds = []
    distances = []
    times = []

    while x < distance:
        drag = 0.5 * AIR_DENSITY * cd * FRONTAL_AREA * v**2
        a = (ENGINE_FORCE - drag) / MASS

        v = max(v + a * DT, 0)
        x += v * DT
        t += DT

        speeds.append(v)
        distances.append(x)
        times.append(t)

    return np.array(times), np.array(distances), np.array(speeds)


# =========================
# TWO CAR OVERTAKE SIM
# =========================
def simulate_overtake(cd_no_drs, cd_drs, distance, gap):
    v1 = 0
    v2 = 0

    x1 = gap  # lead car ahead
    x2 = 0

    t = 0

    times = []
    gaps = []

    while x2 < distance and x1 < distance + gap:
        # Lead car
        drag1 = 0.5 * AIR_DENSITY * cd_no_drs * FRONTAL_AREA * v1**2
        a1 = (ENGINE_FORCE - drag1) / MASS
        v1 = max(v1 + a1 * DT, 0)
        x1 += v1 * DT

        # Chasing car (DRS)
        drag2 = 0.5 * AIR_DENSITY * cd_drs * FRONTAL_AREA * v2**2
        a2 = (ENGINE_FORCE - drag2) / MASS
        v2 = max(v2 + a2 * DT, 0)
        x2 += v2 * DT

        current_gap = x1 - x2

        times.append(t)
        gaps.append(current_gap)

        if current_gap <= 0:
            return True, np.array(times), np.array(gaps)

        t += DT

    return False, np.array(times), np.array(gaps)


# =========================
# UI
# =========================
st.set_page_config(page_title="DRS Simulator", layout="centered")

st.title("🏎️ DRS Effectiveness + Overtake Tool")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Inputs")

cd_display = st.sidebar.slider("Base Drag Co-efficient", 0.85, 1.20, 1.0, 0.01)
cd_no_drs = 1.20 - (cd_display - 0.85)

st.sidebar.markdown("Actual Drag Co-efficient Used")
st.sidebar.markdown(f"# {cd_no_drs:.2f}")

drs_reduction = st.sidebar.slider("DRS Effect (%)", 5, 20, 15)
cd_drs = cd_no_drs * (1 - drs_reduction / 100)

st.sidebar.markdown("Drag Coefficient with DRS")
st.sidebar.markdown(f"# {cd_drs:.2f}")

distance = st.sidebar.slider("Straight Length (m)", 200, 2000, 800, 50)

# 🔥 NEW INPUT
gap = st.sidebar.slider("Initial Gap (m)", 0, 50, 20)


# =========================
# RUN SIMS
# =========================
t1, d1, v1 = simulate_run(cd_no_drs, distance)
t2, d2, v2 = simulate_run(cd_drs, distance)

time_saved = t1[-1] - t2[-1]
efficiency = (time_saved / t1[-1]) * 100

overtake, t_gap, gap_vals = simulate_overtake(cd_no_drs, cd_drs, distance, gap)


# =========================
# RESULTS
# =========================
st.subheader("📊 Performance Results")

col1, col2 = st.columns(2)

with col1:
    st.metric("Final Speed (No DRS)", f"{v1[-1]*3.6:.1f} km/h")

with col2:
    st.metric("Final Speed (DRS)", f"{v2[-1]*3.6:.1f} km/h")

st.metric("⏱️ Time Saved", f"{time_saved:.4f} s")
st.metric("📈 Efficiency Gain", f"{efficiency:.2f} %")


# =========================
# GRAPH 1
# =========================
st.subheader("📉 Distance vs Time")

fig1, ax1 = plt.subplots()
ax1.plot(t1, d1, label="No DRS")
ax1.plot(t2, d2, label="DRS")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Distance (m)")
ax1.legend()
ax1.grid()

st.pyplot(fig1)


# =========================
# GRAPH 2
# =========================
st.subheader("📈 Speed vs Time")

fig2, ax2 = plt.subplots()
ax2.plot(t1, v1 * 3.6, label="No DRS")
ax2.plot(t2, v2 * 3.6, label="DRS")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Speed (km/h)")
ax2.legend()
ax2.grid()

st.pyplot(fig2)


# =========================
# 🔥 OVERTAKE GRAPH
# =========================
st.subheader("🏁 Overtake Analysis")

if overtake:
    st.success("✅ OVERTAKE POSSIBLE")
else:
    st.error("❌ OVERTAKE NOT POSSIBLE")

fig3, ax3 = plt.subplots()
ax3.plot(t_gap, gap_vals)
ax3.axhline(0, linestyle="--")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Gap (m)")
ax3.set_title("Gap Closing (Lead - Chase)")
ax3.grid()

st.pyplot(fig3)


# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("Race Strategy Tool 🏎️")