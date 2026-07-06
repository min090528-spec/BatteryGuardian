import streamlit as st

from main import (
    get_system_info,
    get_running_programs,
    calculate_battery_stress,
    save_report
)

st.set_page_config(
    page_title="Battery Guardian AI",
    page_icon="🔋",
    layout="centered"
)

st.title("🔋 Battery Guardian AI")

st.write("배터리 사용 습관을 AI가 분석합니다.")

st.divider()

fast_charge = st.radio(
    "고속충전을 사용했나요?",
    ["Y", "N"]
)

brightness = st.slider(
    "평균 화면 밝기",
    0,
    100,
    50
)

charge_count = st.number_input(
    "오늘 충전 횟수",
    min_value=0,
    value=1
)

if st.button("🔍 분석 시작", use_container_width=True):

    system_info = get_system_info()

    categories, process_list = get_running_programs()

    user_input = {
        "fast_charge": fast_charge,
        "brightness": brightness,
        "charge_count": charge_count
    }

    result = calculate_battery_stress(
        system_info,
        user_input,
        categories
    )

    report_file = save_report(
        system_info,
        user_input,
        categories,
        result
    )

    st.success("분석 완료!")

    st.subheader("Battery Stress Index")

    st.metric(
        "점수",
        f"{result['stress']}점"
    )

    st.metric(
        "상태",
        result["status"]
    )

    st.subheader("원인")

    if result["reasons"]:

        for reason in result["reasons"]:
            st.write("•", reason)

    else:

        st.write("이상 없음")

    st.subheader("AI 추천")

    if result["recommendations"]:

        for recommendation in result["recommendations"]:
            st.write("•", recommendation)

    else:

        st.write("현재 사용 습관 유지")

    with open(report_file, "rb") as file:

        st.download_button(
            "📄 보고서 다운로드",
            file,
            file_name="BatteryGuardian_Report.txt"
        )