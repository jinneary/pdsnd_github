import time
import pandas as pd
import numpy as np

# 도시 이름을 키로 하고 해당 도시의 데이터 파일 경로를 값으로 하는 딕셔너리
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    사용자로부터 분석할 도시, 월, 요일을 입력받습니다.

    Returns:
        city (str): 분석할 도시 이름
        month (str): 필터링할 월 이름 또는 "all" (모든 월)
        day (str): 필터링할 요일 이름 또는 "all" (모든 요일)
    """
    print('hello! 미국 자전거 공유 데이터를 탐색해봅시다!')

    # 도시 이름을 입력받기 위한 초기화
    selected_city = ""
    city_names = list(CITY_DATA.keys())  # CITY_DATA 딕셔너리의 키(도시 이름)들을 리스트로 변환

    # 유효한 도시 이름이 입력될 때까지 반복
    while not (selected_city in city_names):
        selected_city = input(f"분석할 city name을 입력하세요 {city_names}: ").lower()

    # 월을 입력받기 위한 초기화
    selected_month = ""
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
                    'july', 'august', 'september', 'october', 'november', 'december']

    # 유효한 월이 입력될 때까지 반복
    while not (selected_month in valid_months):
        selected_month = input("필터링할 월을 입력하세요 (예: 'all', 'january' ... 'december'): ").lower()

    # 요일을 입력받기 위한 초기화
    selected_day = ""
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # 유효한 요일이 입력될 때까지 반복
    while not (selected_day in valid_days):
        selected_day = input("필터링할 요일을 입력하세요 (예: 'all', 'monday' ... 'sunday'): ").lower()

    # 입력받은 필터 정보를 출력
    print(f"\n입력한 값 - 도시: '{selected_city}', 월: '{selected_month}', 요일: '{selected_day}'")
    print('-'*40)

    return selected_city, selected_month, selected_day

def load_data(city, month, day):
    """
    지정된 도시의 데이터를 불러오고, 선택한 월과 요일로 필터링합니다.

    Args:
        city (str): 분석할 도시 이름
        month (str): 필터링할 월 이름 또는 "all"
        day (str): 필터링할 요일 이름 또는 "all"
    Returns:
        df (DataFrame): 필터링된 데이터프레임
    """

    # 해당 도시의 데이터 파일 경로 가져오기
    file_path = CITY_DATA[city]

    # CSV 파일을 데이터프레임으로 읽어오기
    df_city = pd.read_csv(file_path)

    # 'Start Time' 컬럼을 datetime 형식으로 변환
    df_city['Start Time'] = pd.to_datetime(df_city['Start Time'])

    # 'Start Time'에서 월과 요일 추출하여 새로운 컬럼으로 추가
    df_city['Month'] = df_city['Start Time'].dt.strftime('%B').str.lower()
    df_city['Day'] = df_city['Start Time'].dt.day_name().str.lower()

    # 월과 요일에 따라 데이터 필터링
    if (month == 'all'):
        if (day == 'all'):
            df = df_city  # 모든 월과 요일을 포함
        else:
            df = df_city[df_city['Day'] == day]  # 모든 월, 특정 요일
    else:
        if (day == 'all'):
            df = df_city[df_city['Month'] == month]  # 특정 월, 모든 요일
        else:
            df = df_city[(df_city['Month'] == month) & (df_city['Day'] == day)]  # 특정 월과 요일

    return df

def time_stats(df):
    """가장 빈번한 여행 시간에 대한 통계를 계산하고 출력합니다."""
    print('\n가장 빈번한 여행 시간 통계를 계산 중입니다...\n')
    start_time = time.time()

    # 가장 많이 사용된 월
    common_month = df['Month'].mode()[0]
    print(f"가장 흔한 월은: {common_month}")

    # 가장 많이 사용된 요일
    common_day = df['Day'].mode()[0]
    print(f"가장 흔한 요일은: {common_day}")

    # 가장 많이 사용된 시간
    df['Hour'] = df['Start Time'].dt.hour  # 'Start Time'에서 시간만 추출
    common_hour = df['Hour'].mode()[0]
    print(f"가장 흔한 시간은: {common_hour}시")

    print(f"\n이 통계를 계산하는 데 {time.time() - start_time:.4f}초가 걸렸습니다.")
    print('-'*40)

def station_stats(df):
    """가장 인기 있는 출발지와 도착지, 그리고 여행 경로에 대한 통계를 계산하고 출력합니다."""
    print('\n가장 인기 있는 출발지와 도착지, 그리고 여행 경로 통계를 계산 중입니다...\n')
    start_time = time.time()

    # 가장 많이 사용된 출발지
    common_start_station = df['Start Station'].mode()[0]
    print(f"가장 많이 사용된 출발지는: {common_start_station}")

    # 가장 많이 사용된 도착지
    common_end_station = df['End Station'].mode()[0]
    print(f"가장 많이 사용된 도착지는: {common_end_station}")

    # 가장 빈번한 출발지와 도착지 조합
    start_and_end_station = df['Start Station'] + " -> " + df['End Station']
    freq_start_and_end_station = start_and_end_station.mode()[0]
    print(f"가장 빈번한 출발지와 도착지 조합은: {freq_start_and_end_station}")

    print(f"\n이 통계를 계산하는 데 {time.time() - start_time:.4f}초가 걸렸습니다.")
    print('-'*40)

def trip_duration_stats(df):
    """총 여행 시간과 평균 여행 시간에 대한 통계를 계산하고 출력합니다."""
    print('\n여행 시간 통계를 계산 중입니다...\n')
    start_time = time.time()

    # 총 여행 시간 계산 (초 단위)
    total_travel_time = df['Trip Duration'].sum()
    total_hours, total_mins, total_secs = get_hours_mins_secs(total_travel_time)
    print(f"총 여행 시간은 {total_hours}시간 {total_mins}분 {total_secs}초입니다.")

    # 평균 여행 시간 계산 (초 단위)
    mean_travel_time = df['Trip Duration'].mean()
    mean_hours, mean_mins, mean_secs = get_hours_mins_secs(mean_travel_time)
    print(f"평균 여행 시간은 {mean_hours}시간 {mean_mins}분 {mean_secs}초입니다.")

    print(f"\n이 통계를 계산하는 데 {time.time() - start_time:.4f}초가 걸렸습니다.")
    print('-'*40)

def get_hours_mins_secs(total_time):
    """초 단위의 시간을 시, 분, 초로 변환합니다."""
    hours = int(total_time // 3600)  # 전체 시간을 시간 단위로 변환
    mins = int((total_time % 3600) // 60)  # 나머지 시간을 분 단위로 변환
    secs = round(total_time % 60, 2)  # 남은 초 단위
    return hours, mins, secs

def user_stats(df):
    """사용자 유형, 성별, 출생 연도에 대한 통계를 계산하고 출력합니다."""
    print('\n사용자 통계를 계산 중입니다...\n')
    start_time = time.time()

    # 사용자 유형의 개수 계산 및 출력
    counts_of_user_type = df['User Type'].value_counts()
    print("사용자 유형별 개수:")
    print('-'*40)
    print(f"{counts_of_user_type}\n")

    # 성별 정보가 있는 경우 성별의 개수 계산 및 출력
    if 'Gender' in df.columns:
        counts_of_gender = df['Gender'].value_counts()
        print("성별별 개수:")
        print('-'*40)
        print(f"{counts_of_gender}\n")
    else:
        print("성별 데이터가 없습니다.")

    # 출생 연도 정보가 있는 경우 출생 연도 통계 계산 및 출력
    if 'Birth Year' in df.columns:
        min_birth_year = int(df['Birth Year'].min())
        print(f"가장 오래된 출생 연도: {min_birth_year}")

        max_birth_year = int(df['Birth Year'].max())
        print(f"가장 최근 출생 연도: {max_birth_year}")

        common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"가장 흔한 출생 연도: {common_birth_year}")
    else:
        print("출생 연도 데이터가 없습니다.")

    print(f"\n이 통계를 계산하는 데 {time.time() - start_time:.4f}초가 걸렸습니다.")
    print('-'*40)

def display_raw_data(df):
    """
    사용자 요청에 따라 원시 데이터를 5행씩 출력합니다.

    Args:
        df (DataFrame): 필터링된 데이터프레임
    """
    start_row = 0
    end_row = 5
    while True:
        show_data = input("\n원시 데이터를 5행씩 더 보고 싶으신가요? 'yes' 또는 'no'로 입력하세요: ").lower()
        if show_data == 'yes':
            print(df.iloc[start_row:end_row]) 
            start_row += 5
            end_row += 5
            # 데이터프레임의 끝에 도달했는지 확인하세요
            if start_row >= len(df):
                print("\n더 이상 표시할 데이터가 없습니다.")
                break
        elif show_data == 'no':
            print("\n원시 데이터 표시를 종료합니다.")
            break
        else:
            print("\n잘못된 입력입니다. '네' 또는 '아니오'로 입력해주세요.")

def main():
    """주요 프로그램 실행 루프"""
    while True:
        city, month, day = get_filters()  
        df = load_data(city, month, day)   # 입력받은 필터로 데이터 불러오기

        if len(df) == 0:
            print("입력한 조건에 맞는 데이터가 없습니다.")
        else:
            display_raw_data(df)          # 원시 데이터 표시
            time_stats(df)                # 시간 통계 계산 및 출력
            station_stats(df)             # 역 통계 계산 및 출력
            trip_duration_stats(df)       # 여행 시간 통계 계산 및 출력
            user_stats(df)                # 사용자 통계 계산 및 출력

        # 프로그램을 다시 실행할지 여부 묻기
        restart = input('\nagain? "yes" 또는 "no"를 입력하세요.\n').lower()
        if restart != 'yes':
            print("프로그램을 종료합니다. have a nice day!")
            break

if __name__ == "__main__":
    main()
