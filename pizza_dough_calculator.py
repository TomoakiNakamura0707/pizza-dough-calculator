import streamlit as st
#(C) Copyright All Righs Reserved.  Tomoaki Nakamura 2025/6/22

# 🌐 Language toggle
lang = st.radio("🌐 Language / 言語", ["日本語", "English"], horizontal=True)
lang_code = "ja" if lang == "日本語" else "en"

# 🌡 Temperature unit toggle
unit = st.radio("Temperature Unit / 温度単位", ["C", "F"], horizontal=True)
use_fahrenheit = unit == "F"

def convert_to_c(f):
    return (f - 32) * 5.0 / 9.0

def convert_to_f(c):
    return c * 9.0 / 5.0 + 32

# 🔤 Text translation
def t(key, lang='en'):
    texts = {
        "title": {"en": "🍕 Pizza Dough Calculator", "ja": "🍕 ピザ生地計算ツール"},
        "balls": {"en": "Number of Dough Balls", "ja": "ドウボールの個数"},
        "weight": {"en": "Weight per Dough Ball (grams)", "ja": "1個あたりの重さ（g）"},
        "preset": {"en": "Dough Style Preset", "ja": "ドウスタイルのプリセット"},
        "hydration": {"en": "Hydration (%)", "ja": "加水率（%）"},
        "salt": {"en": "Salt (%)", "ja": "塩分（%）"},
        "olive_oil": {"en": "Olive Oil (%)", "ja": "オリーブオイル（%）"},
        "fermentation": {"en": "Fermentation Schedule", "ja": "発酵スケジュール"},
        "calculate": {"en": "Calculate", "ja": "計算する"},
        "summary": {"en": "Dough Summary", "ja": "生地の概要"},
        "flour_choice": {"en": "Flour Recommendation", "ja": "おすすめ小麦粉"},
        "manual_flour": {"en": "Manually select flour", "ja": "手動で小麦粉を選ぶ"},
        "choose_flour": {"en": "Choose Flour", "ja": "小麦粉を選択"},
        "water_temp": {"en": "Kneading Water Temperature Helper", "ja": "こね水の温度計算"},
    }
    return texts.get(key, {}).get(lang, key)

st.set_page_config(page_title=t("title", lang_code), page_icon="🍕", layout="centered")
st.title(t("title", lang_code))

col1, col2 = st.columns(2)
with col1:
    dough_balls = st.number_input(t("balls", lang_code), 1, 50, 3)
with col2:
    weight_per_ball = st.number_input(t("weight", lang_code), 100, 1000, 183)

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

olive_oil_percent = 0.0
if preset == "New York Style":
    olive_oil_percent = st.slider(t("olive_oil", lang_code), 0.0, 5.0, 2.0)

st.subheader(t("fermentation", lang_code))
fermentation_schedule = []
for i, label in enumerate(["Room Temp 1", "Cold Ferment", "Room Temp 2"]):
    col1, col2 = st.columns(2)
    with col1:
        time = st.number_input(f"{label} - {t('fermentation', lang_code)} (h)", 0.0, 168.0, float([2, 24, 2][i]), key=f"t_{i}")
    with col2:
        temp = st.number_input(f"{label} Temp (°{'F' if use_fahrenheit else 'C'})", 0.0, 120.0 if use_fahrenheit else 40.0, float([77, 39, 73][i]) if use_fahrenheit else float([25, 4, 23][i]), key=f"temp_{i}")
        if use_fahrenheit:
            temp = convert_to_c(temp)
    fermentation_schedule.append((time, temp))

total_time = sum([h for h, _ in fermentation_schedule])
total_flour = dough_balls * weight_per_ball / (1 + hydration / 100)
total_water = total_flour * hydration / 100
yeast_percent = max(0.01, min(3.0, 1.5 / total_time))
yeast_grams = total_flour * yeast_percent / 100
salt_grams = total_flour * salt_percent / 100
olive_oil_grams = total_flour * olive_oil_percent / 100

if st.button(t("calculate", lang_code)):
    st.subheader(t("summary", lang_code))
    st.markdown(f"**Flour**: {total_flour:.1f} g")
    st.markdown(f"**Water**: {total_water:.1f} g")
    st.markdown(f"**Yeast**: {yeast_grams:.2f} g ({yeast_percent:.2f}%)")
    st.markdown(f"**Salt**: {salt_grams:.1f} g ({salt_percent:.2f}%)")
    if olive_oil_percent > 0:
        st.markdown(f"**Olive Oil**: {olive_oil_grams:.1f} g ({olive_oil_percent:.2f}%)")

    FLOURS = [
        {"key": "nuvola", "en": "Caputo 0 Nuvola", "ja": "ヌーヴォラ(カプート)", "protein": 12.5, "ash": 0.50, "styles": ["Neapolitan"]},
        {"key": "cuoco", "en": "Caputo 00 Chef's Flour", "ja": "サッコロッソクォーコ(カプート)", "protein": 13.0, "ash": 0.55, "styles": ["Neapolitan", "Long Fermentation"]},
        {"key": "pizzeria", "en": "Caputo 00 Pizzeria Blue", "ja": "ピッツェリア(カプート)", "protein": 12.75, "ash": 0.50, "styles": ["Neapolitan", "All"]},
        {"key": "americana", "en": "Caputo Americana", "ja": "アメリカーナ(カプート)", "protein": 13.5, "ash": 0.55, "styles": ["New York Style"]},
        {"key": "manitoba", "en": "Caputo Manitoba Oro", "ja": "マニトバ オーロ(カプート)", "protein": 14.5, "ash": 0.65, "styles": ["Chicago Deep Dish", "Frozen Pizza"]},
        {"key": "camellia", "en": "Nisshin Camellia", "ja": "カメリア（日清）", "protein": 11.5, "ash": 0.40, "styles": ["All"]},
        {"key": "lis_dor", "en": "Nisshin Lis D’or", "ja": "リスドォル（日清）", "protein": 11.8, "ash": 0.45, "styles": ["Neapolitan", "French", "Light Crust"]},
    ]


        matches = [f for f in FLOURS if preset in f["styles"] or "All" in f["styles"]]
        st.subheader("🧂 " + t("flour_choice", lang_code))
        for flour in matches:
            st.markdown(f"**{flour[lang_code]}**  Protein: {flour['protein']}%  Ash: {flour['ash']}%")

# 水温計算
st.subheader("💧 " + t("water_temp", lang_code))
target_temp = st.slider("🎯 Target Dough Temperature", 20, 30, 25) if not use_fahrenheit else st.slider("🎯 Target Dough Temperature", 68, 86, 77)
room_temp = st.number_input("🌡️ Room Temperature", value=24.0 if not use_fahrenheit else 75.2)
flour_temp = st.number_input("🌾 Flour Temperature", value=22.0 if not use_fahrenheit else 71.6)
friction = st.slider("🌀 Friction Factor", 0, 10, 5)

# 温度を °C に換算して計算
if use_fahrenheit:
    target_temp = convert_to_c(target_temp)
    room_temp = convert_to_c(room_temp)
    flour_temp = convert_to_c(flour_temp)

water_temp = target_temp * 3 - (room_temp + flour_temp + friction)
water_display = f"{convert_to_f(water_temp):.1f} °F" if use_fahrenheit else f"{water_temp:.1f} °C"
st.markdown(f"💧 **Recommended Water Temperature**: `{water_display}`")
