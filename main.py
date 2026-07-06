import psutil
from datetime import datetime


# ==================================================
# 시스템 정보 가져오기
# ==================================================

def get_system_info():
    """
    컴퓨터의 현재 상태를 가져온다.
    """

    battery = psutil.sensors_battery()

    if battery is not None:
        battery_percent = battery.percent

        if battery.power_plugged:
            charging_status = "충전 중"
        else:
            charging_status = "배터리 사용 중"

    else:
        battery_percent = "알 수 없음"
        charging_status = "알 수 없음"

    cpu_usage = psutil.cpu_percent(interval=1)

    ram_usage = psutil.virtual_memory().percent

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "battery": battery_percent,
        "charging": charging_status,
        "cpu": cpu_usage,
        "ram": ram_usage,
        "time": current_time
    }


# ==================================================
# 사용자 입력
# ==================================================

def get_user_input():
    """
    사용자가 직접 입력하는 정보
    """

    print("\n========== 사용자 입력 ==========\n")

    while True:

        fast_charge = input("고속충전을 사용했나요? (Y/N) : ").strip().upper()

        if fast_charge in ("Y", "N"):
            break

        print("Y 또는 N만 입력하세요.")

    while True:

        try:

            brightness = int(input("평균 화면 밝기(0~100) : "))

            if 0 <= brightness <= 100:
                break

            print("0~100 사이를 입력하세요.")

        except ValueError:

            print("숫자를 입력하세요.")

    while True:

        try:

            charge_count = int(input("오늘 충전 횟수 : "))

            if charge_count >= 0:
                break

            print("0 이상을 입력하세요.")

        except ValueError:

            print("숫자를 입력하세요.")

    return {
        "fast_charge": fast_charge,
        "brightness": brightness,
        "charge_count": charge_count
    }


# ==================================================
# 실행 중인 프로그램 분석
# ==================================================

def get_running_programs():
    """
    현재 실행 중인 프로그램을 분석한다.
    """

    categories = {
        "browser": False,
        "game": False,
        "development": False,
        "messenger": False
    }

    browser_keywords = [
        "chrome",
        "msedge",
        "firefox"
    ]

    game_keywords = [
        "steam",
        "league",
        "valorant"
    ]

    development_keywords = [
        "code",
        "pycharm"
    ]

    messenger_keywords = [
        "discord",
        "kakaotalk"
    ]

    process_list = []

    for process in psutil.process_iter(["name"]):

        try:

            name = process.info["name"]

            if not name:
                continue

            name = name.lower()

            process_list.append(name)

            if any(keyword in name for keyword in browser_keywords):
                categories["browser"] = True

            if any(keyword in name for keyword in game_keywords):
                categories["game"] = True

            if any(keyword in name for keyword in development_keywords):
                categories["development"] = True

            if any(keyword in name for keyword in messenger_keywords):
                categories["messenger"] = True

        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            continue

    return categories, process_list
# ==================================================
# Battery Stress Index 계산
# ==================================================

def calculate_battery_stress(system_info, user_input, categories):
    """
    Battery Stress Index 계산
    """

    stress = 0

    reasons = []

    recommendations = []

    cpu = system_info["cpu"]
    ram = system_info["ram"]

    brightness = user_input["brightness"]
    fast_charge = user_input["fast_charge"]
    charge_count = user_input["charge_count"]

    # -------------------------
    # CPU
    # -------------------------

    if cpu >= 80:
        stress += 30
        reasons.append("CPU 사용량이 매우 높습니다.")
        recommendations.append("불필요한 프로그램을 종료하세요.")

    elif cpu >= 60:
        stress += 20
        reasons.append("CPU 사용량이 높습니다.")

    elif cpu >= 30:
        stress += 10

    # -------------------------
    # RAM
    # -------------------------

    if ram >= 85:
        stress += 15
        reasons.append("RAM 사용량이 매우 높습니다.")
        recommendations.append("브라우저 탭을 줄여보세요.")

    elif ram >= 70:
        stress += 10

    elif ram >= 50:
        stress += 5

    # -------------------------
    # 화면 밝기
    # -------------------------

    if brightness >= 80:
        stress += 10
        reasons.append("화면 밝기가 매우 높습니다.")
        recommendations.append("밝기를 60% 정도로 낮춰보세요.")

    elif brightness >= 50:
        stress += 5

    # -------------------------
    # 고속충전
    # -------------------------

    if fast_charge == "Y":
        stress += 20
        reasons.append("고속충전을 사용했습니다.")
        recommendations.append("가능하면 일반 충전을 권장합니다.")

    # -------------------------
    # 충전 횟수
    # -------------------------

    if charge_count >= 3:
        stress += 10
        reasons.append("충전 횟수가 많습니다.")
        recommendations.append("짧은 시간 여러 번 충전하는 습관을 줄여보세요.")

    elif charge_count == 2:
        stress += 5

    # -------------------------
    # 실행 프로그램 분석
    # -------------------------

    if categories["game"]:
        stress += 20
        reasons.append("게임이 실행 중입니다.")
        recommendations.append("게임 종료 후 충전하면 발열을 줄일 수 있습니다.")

    if categories["browser"]:
        stress += 5
        reasons.append("브라우저가 실행 중입니다.")

    if categories["development"]:
        stress += 5
        reasons.append("개발 프로그램이 실행 중입니다.")

    if categories["messenger"]:
        stress += 2

    # -------------------------
    # 점수 제한
    # -------------------------

    if stress > 100:
        stress = 100

    # -------------------------
    # 상태 판정
    # -------------------------

    if stress >= 60:
        status = "🔴 위험"

    elif stress >= 30:
        status = "🟡 주의"

    else:
        status = "🟢 양호"

    return {
        "stress": stress,
        "status": status,
        "reasons": reasons,
        "recommendations": recommendations
    }
# ==================================================
# 보고서 저장
# ==================================================

def save_report(system_info,
                user_input,
                categories,
                result):

    program_names = {
        "browser": "브라우저",
        "game": "게임",
        "development": "개발 프로그램",
        "messenger": "메신저"
    }

    with open("report.txt",
              "w",
              encoding="utf-8") as file:

        file.write("=" * 60 + "\n")
        file.write("Battery Guardian AI 분석 보고서\n")
        file.write("=" * 60 + "\n\n")

        file.write("[자동 분석]\n\n")

        file.write(f"현재 시간 : {system_info['time']}\n")
        file.write(f"배터리 : {system_info['battery']}%\n")
        file.write(f"충전 상태 : {system_info['charging']}\n")
        file.write(f"CPU : {system_info['cpu']}%\n")
        file.write(f"RAM : {system_info['ram']}%\n\n")

        file.write("[사용자 입력]\n\n")

        file.write(f"고속충전 : {user_input['fast_charge']}\n")
        file.write(f"화면 밝기 : {user_input['brightness']}%\n")
        file.write(f"충전 횟수 : {user_input['charge_count']}회\n\n")

        file.write("[실행 프로그램]\n\n")

        found = False

        for key in program_names:

            if categories[key]:

                file.write(f"• {program_names[key]}\n")

                found = True

        if not found:
            file.write("특별한 프로그램 없음\n")

        file.write("\n")

        file.write("[Battery Stress Index]\n\n")

        file.write(f"점수 : {result['stress']}점\n")
        file.write(f"상태 : {result['status']}\n\n")

        file.write("원인\n")

        if result["reasons"]:

            for reason in result["reasons"]:
                file.write(f"• {reason}\n")

        else:

            file.write("• 이상 없음\n")

        file.write("\n")

        file.write("AI 추천\n")

        if result["recommendations"]:

            for recommendation in result["recommendations"]:
                file.write(f"• {recommendation}\n")

        else:

            file.write("• 현재 습관 유지\n")
# ==================================================
# 메인 함수
# ==================================================

def main():

    # -------------------------
    # 정보 수집
    # -------------------------

    system_info = get_system_info()

    categories, process_list = get_running_programs()

    user_input = get_user_input()

    result = calculate_battery_stress(
        system_info,
        user_input,
        categories
    )

    save_report(
    system_info,
    user_input,
    categories,
    result
    )

    # -------------------------
    # 출력
    # -------------------------

    print("\n" + "=" * 60)
    print("           Battery Guardian AI v1.0")
    print("=" * 60)

    print("\n[자동 분석]")

    print(f"현재 시간 : {system_info['time']}")
    print(f"배터리 : {system_info['battery']}%")
    print(f"충전 상태 : {system_info['charging']}")
    print(f"CPU 사용량 : {system_info['cpu']}%")
    print(f"RAM 사용량 : {system_info['ram']}%")

    print("\n" + "-" * 60)

    print("\n[사용자 입력]")

    print(f"고속충전 : {user_input['fast_charge']}")
    print(f"화면 밝기 : {user_input['brightness']}%")
    print(f"오늘 충전 횟수 : {user_input['charge_count']}회")

    print("\n" + "-" * 60)

    print("\n[실행 중인 프로그램]")

    program_names = {
        "browser": "브라우저",
        "game": "게임",
        "development": "개발 프로그램",
        "messenger": "메신저"
    }

    found = False

    for key in program_names:

        if categories[key]:
            print(f"✔ {program_names[key]}")
            found = True

    if not found:
        print("특별한 프로그램이 감지되지 않았습니다.")

    print("\n" + "-" * 60)

    print("\nBattery Stress Index")

    print(f"\n점수 : {result['stress']}점")
    print(f"상태 : {result['status']}")

    print("\n원인 분석")

    if result["reasons"]:

        for reason in result["reasons"]:
            print(f"• {reason}")

    else:
        print("• 특별한 문제가 발견되지 않았습니다.")

    print("\nAI 추천")

    if result["recommendations"]:

        for recommendation in result["recommendations"]:
            print(f"• {recommendation}")

    else:
        print("• 현재 사용 습관을 유지하세요.")

    print("\n" + "=" * 60)

    print("\n보고서(report.txt)가 저장되었습니다.")

    print("\nEnter 키를 누르면 프로그램이 종료됩니다...")
    input()
    # ==================================================
# 프로그램 시작
# ==================================================

if __name__ == "__main__":
    main()


