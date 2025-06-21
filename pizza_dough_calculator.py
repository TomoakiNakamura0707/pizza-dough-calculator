import streamlit as st

# ---- Yeast calculation ----
def calculate_multistage_yeast(flour_g, hydration_percent, stages):
    base_temp = 20
    base_hours = 6
    base_yeast_percent = 0.5
    Q10 = 2

    total_activity_ratio = 0
    for stage in stages:
        hours = stage['hours']
        temp = stage['temp']
        temp_factor = Q10 ** ((temp - base_temp) / 10)
        activity = temp_factor * hours
        total_activity_ratio += activity

    base_activity = base_hours * 1
    yeast_percent = base_yeast_percent * (base_activity / total_activity_ratio)
    yeast_g = flour_g * (yeast_percent / 100)
    water_g = flour_g * (hydration_percent / 100)

    return round(yeast_percent, 3), round(yeast_g, 2), round(water_g, 2), round(total_activity_ratio, 2)

# ---- Kneading Water Temperature Calculator ----
def calc_water_temp(dough_temp_goal, room_temp, flour_temp, friction=4):
    return round((dough_temp_goal * 3) - room_temp - flour_temp - friction, 1)

# ---- Presets ----
PRESETS = {
    "Neapolitan": {
        "hydration": 70,
        "stages": [
            {"hours": 2, "temp": 25},
            {"hours": 18, "temp": 5},
            {"hours": 2, "temp": 22}
        ]
    },
    "New York Style": {
        "hydration": 62,
        "stages": [
            {"hours": 1, "temp": 25},
            {"hours": 24, "temp": 5},
            {"hours": 1, "temp": 22}
        ]
    },
    "Chicago Deep Dish": {
        "hydration": 55,
        "stages": [
            {"hours": 3, "temp": 25}
        ]
    },
    "Frozen Pizza": {
        "hydration": 58,
        "stages": [
            {"hours": 2, "temp": 30},
            {"hours": 1, "temp": -18}  # Simulated freezing
        ]
    }
}

# ---- UI Starts Here ----

st.set_page_config(page_title="Pizza Dough Fermentation Calculator", page_icon="🍕")
st.title("🍕 Pizza Dough Yeast & Water Calculator")
st.markdown("Calculate optimal **yeast quantity**, **hydration**, and even **kneading water temperature** based on your dough style and fermentation plan.")

# --- Input: Dough Basics ---
st.header("🧾 Dough Recipe Input")

flour_g = st.number_input("Flour Amount (grams)", min_value=100, max_value=2000, value=500, step=50)

# Preset Selector
preset = st.selectbox("Choose a Style Preset (or Manual)", options=["Manual"] + list(PRESETS.keys()))

# Apply preset
if preset != "Manual":
    hydration_percent = PRESETS[preset]["hydration"]
    stages = PRESETS[preset]["stages"]
else:
    hydration_percent = st.slider("Hydration (%)", min_value=50, max_value=100, value=70)
    st.subheader("🧪 Fermentation Stages")
    num_stages = st.number_input("Number of Stages", min_value=1, max_value=5, value=3)

    stages = []
    for i in range(int(num_stages)):
        st.markdown(f"**Stage {i+1}**")
        hours = st.number_input(f"  - Time (hours)", key=f"h_{i}", min_value=0.1, value=2.0, step=0.5)
        temp = st.number_input(f"  - Temperature (°C)", key=f"t_{i}", min_value=0.0, max_value=40.0, value=25.0, step=0.5)
        stages.append({"hours": hours, "temp": temp})

# Calculate button
if st.button("🧮 Calculate Yeast"):
    yeast_percent, yeast_g, water_g, activity = calculate_multistage_yeast(flour_g, hydration_percent, stages)

    st.success("✅ Dough Summary")
    st.write(f"**Flour**: {flour_g}g")
    st.write(f"**Water**: {water_g}g ({hydration_percent}%)")
    st.write(f"**Yeast**: {yeast_g}g ({yeast_percent}%)")
    st.write(f"**Relative Total Fermentation Activity**: {activity}")

    st.subheader("📄 Recipe Overview")
    st.code(f"""
Flour: {flour_g} g
Water: {water_g} g ({hydration_percent}% hydration)
Yeast: {yeast_g} g ({yeast_percent}% of flour)

Fermentation Plan:
""" + "\n".join(
        [f"- Stage {i+1}: {s['hours']} hrs at {s['temp']}°C" for i, s in enumerate(stages)]
    ), language="text")

# --- Optional: Kneading Water Temperature ---
st.header("🌡 Kneading Water Temperature Helper")
st.markdown("Estimate water temperature to hit a desired final dough temperature.")

with st.expander("🔧 Water Temp Calculator"):
    dough_temp_goal = st.number_input("Target Final Dough Temp (°C)", value=24.0)
    room_temp = st.number_input("Room Temp (°C)", value=22.0)
    flour_temp = st.number_input("Flour Temp (°C)", value=22.0)
    friction = st.slider("Friction Factor (°C)", min_value=0.0, max_value=10.0, value=4.0, step=0.5)

    water_temp = calc_water_temp(dough_temp_goal, room_temp, flour_temp, friction)
    st.info(f"Recommended Water Temperature: **{water_temp}°C**")

st.markdown("---")
st.caption("Developed with ❤️ for pizza makers. Powered by Streamlit.")
