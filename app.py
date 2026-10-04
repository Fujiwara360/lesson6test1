# app.py
# Streamlit版 BMI計算機
# streamlit run app.py で起動（ローカル／Streamlit Cloud共通）

import streamlit as st


def calc_bmi(height_cm, weight_kg):
    """BMIと評価を計算する。例外時は0扱いにする簡易ハンドリング"""
    try:
        height_m = float(height_cm) / 100
        weight = float(weight_kg)
        if height_m <= 0 or weight <= 0:
            return 0.0, "入力値を正しく入力してください"
        bmi = weight / (height_m ** 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0, "入力値を正しく入力してください"

    if bmi < 18.5:
        judge = "低体重（やせ型）"
    elif bmi < 25:
        judge = "普通体重"
    elif bmi < 30:
        judge = "肥満（1度）"
    elif bmi < 35:
        judge = "肥満（2度）"
    elif bmi < 40:
        judge = "肥満（3度）"
    else:
        judge = "肥満（4度）"

    return round(bmi, 2), judge


def clear_inputs():
    """入力値をすべて削除する"""
    st.session_state["height"] = ""
    st.session_state["weight"] = ""


def main():
    st.set_page_config(page_title="BMI計算機", page_icon="⚖️")

    st.title("BMI計算機")

    if "height" not in st.session_state:
        st.session_state["height"] = ""
    if "weight" not in st.session_state:
        st.session_state["weight"] = ""

    height_raw = st.text_input("身長 (cm)", key="height", placeholder="例: 170")
    weight_raw = st.text_input("体重 (kg)", key="weight", placeholder="例: 60")

    col1, col2 = st.columns(2)
    with col1:
        calc_clicked = st.button("計算する", type="primary", use_container_width=True)
    with col2:
        st.button("クリア", on_click=clear_inputs, use_container_width=True)

    if calc_clicked:
        bmi, judge = calc_bmi(height_raw, weight_raw)
        st.success(f"BMI: **{bmi}**　判定: **{judge}**")


if __name__ == "__main__":
    main()
