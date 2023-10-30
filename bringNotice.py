from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
import glob
from datetime import datetime

class UOSNoticeScraper:
    def __init__(self, save_dir='UOS_DB'):
        self.driver = webdriver.Chrome()
        self.current_date = datetime.now().strftime("%Y_%m_%d")
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def init_driver(self):
        self.driver.get('https://www.uos.ac.kr/korNotice/list.do?list_id=FA1')
        self.driver.implicitly_wait(8)

    def extract_notice_data(self):
        data = {'공지사항': []}

        for i in range(1, 11): # 10개의 공지를 확인한다고 가정 (필요에 따라 조정 가능)
            try:
                # '공지' 텍스트가 있는지 확인
                notice_span = self.driver.find_element(By.XPATH, f'//*[@id="contents"]/ul/li[{i}]/div/p/span')
                if notice_span.text == '공지':
                    # 제목 추출
                    title = self.driver.find_element(By.XPATH, f'//*[@id="contents"]/ul/li[{i}]/div/div/div[1]/a').text
                    cleaned_title = title.replace("★", "").strip()
                    cleaned_title = cleaned_title.replace("☆", "").strip()
                    data['공지사항'].append(cleaned_title)
            except:
                # 해당 XPath가 존재하지 않을 경우, 다음 항목으로 넘어간다.
                continue

        return data
    
    def remove_old_files(self):
        for f in glob.glob(f"{self.save_dir}/공지사항*.md"):
            os.remove(f)

    def save_to_md(self, data):
        filename = f"공지사항_{self.current_date}.md"
        full_path = os.path.join(self.save_dir, filename)
        df = pd.DataFrame(data)
        df.to_csv(full_path, index=False, encoding='utf-8')
        # df.to_csv(full_path, index=False, encoding='utf-8-sig')  # 윈도우 환경 한글 깨짐 방지

    def run(self):
        self.init_driver()
        self.remove_old_files()
        notice_data = self.extract_notice_data()
        self.save_to_md(notice_data)
        self.driver.implicitly_wait(10)
        self.driver.quit()

if __name__ == '__main__':
    scraper = UOSNoticeScraper(save_dir='UOS_DB')
    scraper.run()
