from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
from datetime import datetime
import os
import glob
import re

class UOSMenuScraper:
    def __init__(self, save_dir='UOS_DB'):
        self.driver = webdriver.Chrome()
        self.buildings = {
            'tab11': '학생회관',
            'tab12': '본관',
            'tab13': '양식당(아느칸)',
            'tab14': '자연과학관'
        }
        self.current_weekday = datetime.now().weekday()
        self.current_date = datetime.now().strftime("%Y%m%d")
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def init_driver(self):
        self.driver.get("https://www.uos.ac.kr/food/placeList.do")
        self.driver.implicitly_wait(10)

    def search_building(self, building_id):
        button = self.driver.find_element(By.ID, building_id)
        button.click()
        self.driver.implicitly_wait(1)

    def enter_weekly_menu(self):
        button = self.driver.find_element(By.ID, 'tab2')
        button.click()
        self.driver.implicitly_wait(1)

    def extract_meal_data_for_csv(self):
        table_element = self.driver.find_element(By.XPATH, "//*[@id='week']/table/tbody")
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        weekdays = ['월', '화', '수', '목', '금']
        data = {'Building': [], 'Day': [], 'Weekday': [], 'Morning': [], 'Lunch': [], 'Dinner': []}

        for i, row in enumerate(rows):
            ths = row.find_elements(By.TAG_NAME, "th")
            tds = row.find_elements(By.TAG_NAME, "td")
            day = ths[0].text if ths else None
            weekday = weekdays[i]
            meals = [re.sub('<br>', ' ', td.get_attribute("innerHTML")).strip() for td in tds]

            if day:
                data['Building'].append(self.building_name)
                data['Day'].append(day.split(' ')[0])
                data['Weekday'].append(weekday)
                meals = ['없음' if len(meal) == 0 else meal for meal in meals]
                data['Morning'].append(meals[0] if len(meals) > 0 else None)
                data['Lunch'].append(meals[1] if len(meals) > 1 else None)
                data['Dinner'].append(meals[2] if len(meals) > 2 else None)

        return data
    
    def clean_text(self, text):
        # '&amp;' 제거
        text = text.replace('&amp;', ',')
        # 콜론(:)과 그 앞뒤 단어 제거
        text = re.sub(r"\S*\s*:\s*\S*", "", text)
        # 시간, 가격, 칼로리, 그램 정보 제거
        text = re.sub(r"\d{1,2}:\d{2}~\d{1,2}:\d{2} \(\d{1,3},?\d{0,3}원\)|\d{3,4}kcal/\d{1,3}g|\d{3,4}kcal|\d{1,3},?\d{0,3}원", "", text)
        # 영어로 번역된 음식 이름 제거 (단, '코너 A', '코너 B', '코너 C'는 유지)
        # text = re.sub(r"(?<!코너 )[A-Za-z\s]*\([A-Za-z\s]*\)", "", text)
        text = re.sub(r"\b(?!코너 )[A-Za-z]{2,}\b", "", text)
        # 소괄호와 그 내용 제거
        text = re.sub(r"\([^)]*\)", "", text)

        return text.strip()  # 앞뒤 공백 제거
    

    def extract_meal_data_for_md(self):
        table_element = self.driver.find_element(By.XPATH, "//*[@id='week']/table/tbody")
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        weekdays = ['월요일', '화요일', '수요일', '목요일', '금요일']
        data_md = ""

        header = "| Building | Day | Weekday | Morning | Lunch | Dinner |\n"
        separator = "| -------- | --- | ------- | ------- | ----- | ------ |\n"
        data_md += header + separator

        for i, row in enumerate(rows):
            ths = row.find_elements(By.TAG_NAME, "th")
            tds = row.find_elements(By.TAG_NAME, "td")
            day = ths[0].text if ths else None
            weekday = weekdays[i]
            meals = [self.clean_text(re.sub('<br>', ' ', td.get_attribute("innerHTML")).strip()) for td in tds]  # clean_text 호출

            if day:
                morning = meals[0] if len(meals) > 0 else None
                lunch = meals[1] if len(meals) > 1 else None
                dinner = meals[2] if len(meals) > 2 else None
                row_data = f"| {self.building_name} | {day.split(' ')[0]} | {weekday} | {morning} | {lunch} | {dinner} |\n"
                data_md += row_data

        return data_md

    def remove_old_files(self):
        for f in glob.glob(f"{self.save_dir}/*weekly_menu.csv"):
            os.remove(f)

    def save_to_csv(self, data):
        filename = f"{self.building_name}_weekly_menu.csv"
        full_path = os.path.join(self.save_dir, filename)
        df = pd.DataFrame(data)
        df.to_csv(full_path, index=False, encoding='utf-8')
        # df.to_csv(full_path, index=False, encoding='utf-8-sig')  # 윈도우 환경 한글 깨짐 방지

    def save_to_md(self, data_md):
        filename = f"{self.building_name}_weekly_menu.md"
        full_path = os.path.join(self.save_dir, filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(data_md)

    def run(self):
        self.init_driver()
        self.remove_old_files()

        for building_id, building_name in self.buildings.items():
            self.building_name = building_name
            self.search_building(building_id)
            self.enter_weekly_menu()
            meal_data_csv = self.extract_meal_data_for_csv()
            self.save_to_csv(meal_data_csv)
            meal_data_md = self.extract_meal_data_for_md()
            self.save_to_md(meal_data_md)

        self.driver.implicitly_wait(20)
        self.driver.quit()

if __name__ == '__main__':
    scraper = UOSMenuScraper(save_dir='UOS_DB')
    scraper.run()
