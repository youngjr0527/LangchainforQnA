#pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
from datetime import datetime, timedelta
import os
import glob

class UOSMenuScraper:
    def __init__(self, save_dir='DB'):
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

    def extract_meal_data(self):
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
                meals = ['Not Provided' if len(meal) == 0 else meal for meal in meals]
                data['Morning'].append(meals[0] if len(meals) > 0 else None)
                data['Lunch'].append(meals[1] if len(meals) > 1 else None)
                data['Dinner'].append(meals[2] if len(meals) > 2 else None)

        return data
    
    def remove_old_files(self):
        for f in glob.glob(f"{self.save_dir}/*weekly_menu.csv"):
            os.remove(f)

    def save_to_csv(self, data):
        monday_date = datetime.now() - timedelta(days=self.current_weekday)
        friday_date = monday_date + timedelta(days=4)
        filename = f"{monday_date.strftime('%y%m%d')}-{friday_date.strftime('%y%m%d')}_{self.building_name}_weekly_menu.csv"
        full_path = os.path.join(self.save_dir, filename)
        df = pd.DataFrame(data)
        df.to_csv(full_path, index=False, encoding='utf-8')
        # df.to_csv(full_path, index=False, encoding='utf-8-sig')  # 윈도우 환경 한글 깨짐 방지

    def run(self):
        self.init_driver()
        self.remove_old_files()

        for building_id, building_name in self.buildings.items():
            self.building_name = building_name
            self.search_building(building_id)
            self.enter_weekly_menu()
            meal_data = self.extract_meal_data()
            self.save_to_csv(meal_data)

        self.driver.implicitly_wait(10)
        self.driver.quit()

if __name__ == '__main__':
    scraper = UOSMenuScraper(save_dir='DB')
    scraper.run()
