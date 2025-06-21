# (C) Copyright All Rights Reserved. Tomoaki Nakamura 2025/06/22
import streamlit as st


st.set_page_config(page_title="Pizza Dough Calculator", page_icon="🍕", layout="centered")
lang = st.radio("🌐 Language / 言語", ["English", "日本語"], horizontal=True)
lang_code = "en" if lang == "English" else "ja"

def t(key, lang='en'):
    texts = {
        "title": {"en": "🍕 Pizza Dough Calculator", "ja": "🍕 ピザ生地計算ツール"},
        "balls": {"en": "Number of Dough Balls", "ja": "ドウボールの個数"},
        "weight": {"en": "Weight per Dough Ball (grams)", "ja": "1個あたりの重さ（g）"},
        "preset": {"en": "Dough Style Preset", "ja": "ドウスタイルのプリセット"},
        "hydration": {"en": "Hydration (%)", "ja": "加水率（%）"},
        "salt": {"en": "Salt (%)", "ja": "塩分（%）"},
        "fermentation": {"en": "Fermentation Schedule", "ja": "発酵スケジュール"},
        "calculate": {"en": "Calculate", "ja": "計算する"},
        "summary": {"en": "Dough Summary", "ja": "生地の概要"},
        "flour_choice": {"en": "Flour Recommendation", "ja": "おすすめ小麦粉"},
        "manual_flour": {"en": "Manually select flour", "ja": "手動で小麦粉を選ぶ"},
        "water_temp": {"en": "Kneading Water Temperature Helper", "ja": "こね水の温度計算"},
    }
    return texts.get(key, {}).get(lang, key)

st.title(t("title", lang_code))

col1, col2 = st.columns(2)
with col1:
    dough_balls = st.number_input(t("balls", lang_code), 1, 50, 4)
with col2:
    weight_per_ball = st.number_input(t("weight", lang_code), 100, 1000, 250)

style_options = ["Neapolitan", "New York Style", "Chicago Deep Dish", "Frozen Pizza", "Manual"]
preset = st.selectbox(t("preset", lang_code), style_options)

hydration_defaults = {
    "Neapolitan": 65,
    "New York Style": 62,
    "Chicago Deep Dish": 55,
    "Frozen Pizza": 60,
    "Manual": 60,
}
hydration = st.slider(t("hydration", lang_code), 50, 100, hydration_defaults[preset])
salt_percent = st.slider(t("salt", lang_code), 0.0, 5.0, 2.2)

# Fermentation schedule
st.subheader(t("fermentation", lang_code))
fermentation_schedule = []
for i, label in enumerate(["Room Temp 1", "Cold Ferment", "Room Temp 2"]):
    col1, col2 = st.columns(2)
    with col1:
        time = st.number_input(f"{label} - {t('fermentation', lang_code)} (h)", 0.0, 168.0, [2, 24, 2][i], key=f"t_{i}")
    with col2:
        temp = st.number_input(f"{label} Temp (°C)", 0.0, 40.0, [25, 4, 23][i], key=f"temp_{i}")
    fermentation_schedule.append((time, temp))

# Dough calculation
total_time = sum([h for h, _ in fermentation_schedule])
total_flour = dough_balls * weight_per_ball / (1 + hydration / 100)
total_water = total_flour * hydration / 100
yeast_percent = max(0.01, min(3.0, 1.5 / total_time))
yeast_grams = total_flour * yeast_percent / 100
salt_grams = total_flour * salt_percent / 100

if st.button(t("calculate", lang_code)):
    st.subheader(t("summary", lang_code))
    st.markdown(f"**Flour**: {total_flour:.1f} g")
    st.markdown(f"**Water**: {total_water:.1f} g")
    st.markdown(f"**Yeast**: {yeast_grams:.2f} g ({yeast_percent:.2f}%)")
    st.markdown(f"**Salt**: {salt_grams:.1f} g ({salt_percent:.2f}%)")

    FLOURS = [
        {"key": "nuvola", "en": 'Caputo "0" Nuvola', "ja": "カプート ヌーヴォラ", "protein": 12.5, "ash": 0.50, "styles": ["Neapolitan"]},
        {"key": "cuoco", "en": 'Caputo "00" Chef's Flour', "ja": "カプート クオーコ", "protein": 13.0, "ash": 0.55, "styles": ["Neapolitan", "Long Fermentation"]},
        {"key": "pizzeria", "en": 'Caputo "00" Pizzeria', "ja": "カプート ピッツェリア", "protein": 12.75, "ash": 0.50, "styles": ["Neapolitan", "General Pizza"]},
        {"key": "americana", "en": "Caputo Americana", "ja": "カプート アメリカーナ", "protein": 13.5, "ash": 0.55, "styles": ["New York Style"]},
        {"key": "manitoba", "en": "Caputo Manitoba Oro", "ja": "カプート マニトバ オーロ", "protein": 14.5, "ash": 0.65, "styles": ["Chicago Deep Dish", "Frozen Pizza"]},
        {"key": "camellia", "en": "Nisshin Camellia", "ja": "カメリア（日清）", "protein": 11.5, "ash": 0.40, "styles": ["All"]},
        {"key": "lis_dor", "en": "Nisshin Lis D’or", "ja": "リスドォル（日清）", "protein": 11.8, "ash": 0.45, "styles": ["Neapolitan", "French", "Light Crust"]},
    ]

    manual = st.checkbox(t("manual_flour", lang_code))
    if manual:
        name_list = [f[lang_code] for f in FLOURS]
        selected = st.selectbox("Choose flour", name_list)
        flour = next(f for f in FLOURS if f[lang_code] == selected)
    else:
        matches = [f for f in FLOURS if preset in f["styles"] or "All" in f["styles"]]
        flour = matches[0] if matches else None

    if flour:
        st.subheader("🧂 " + t("flour_choice", lang_code))
        st.markdown(f"**{flour[lang_code]}**  
Protein: {flour['protein']}%  
Ash: {flour['ash']}%")

# Water temperature calculator
st.subheader("💧 " + t("water_temp", lang_code))
target_temp = st.slider("🎯 Target Dough Temperature (°C)", 20, 30, 25)
room_temp = st.number_input("🌡️ Room Temperature (°C)", 0.0, 40.0, 24.0)
flour_temp = st.number_input("🌾 Flour Temperature (°C)", 0.0, 40.0, 22.0)
friction = st.slider("🌀 Friction Factor (°C)", 0, 10, 5)
water_temp = target_temp * 3 - (room_temp + flour_temp + friction)
st.markdown(f"💧 **Recommended Water Temperature**: `{water_temp:.1f} °C`")
