from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# WebDriver 설정 (크롬 드라이버 경로를 입력해주세요)
# driver_path = './chromedriver.exe'  # 크롬 드라이버의 경로로 변경
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome('./chromedriver.exe')

# 구글 지도 URL
url = 'https://www.google.com/maps/d/u/0/viewer?mid=1XNvlhjVsrQFtelWfLapc76MiJ9c&femb=1&ll=37.506849700000004%2C127.09357109999993&z=8'
driver.get(url)

# 페이지 로드 대기
time.sleep(5)

# 가게 이름과 주소를 저장할 리스트
shop_names = []
shop_addresses = []


# 미리 클릭해둘거 세팅
try:
    button1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[3]/div/div[1]') # 키즈존 체크
    button1.click()
    time.sleep(1)
    button2 = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[4]/div/div[1]') # 기타 체크
    button2.click()
    time.sleep(1)
    button3 = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div') # 노키즈2 목록늘림
    button3.click()
    time.sleep(1)
    button4 = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[2]/div/div') # 노키즈1 목록늘림
    button4.click()
    time.sleep(1)  # 클릭 후 로딩 시간 대기
except Exception as e:
    print(f"setting error.")


# 매장 리스트 요소들의 XPATH
xpath_patterns = ['/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[{}]/div[2]',
                '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[{}]']

for xpath_pattern in xpath_patterns:
    index = 3
    while True:
        try:
            # XPATH 기반 요소 찾기
            xpath = xpath_pattern.format(index)
            marker = driver.find_element(By.XPATH, xpath)
            marker.click()
            time.sleep(1)

            # 가게 이름 추출
            try:
                shop_name = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div/div[2]'))
                ).text
            except:
                try:
                    shop_name = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[1]/div[2]'))
                    ).text
                except:
                    continue
            shop_names.append(shop_name)

            # 가게 주소 추출
            try:
                shop_address = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[2]/div[2]'))
                ).text
            except:
                try:
                    shop_address = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[2]/div[2]'))
                    ).text
                except:
                    shop_address = "."
            shop_addresses.append(shop_address)

            # 뒤로가기 버튼 클릭
            close_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[3]/div[1]/div'))
            )
            close_button.click()
            time.sleep(2)

            index += 1

        except Exception as e:
            print(f"No more elements at index {index}. Ending process.")
            break

# 데이터프레임 생성
df = pd.DataFrame({
    'Name': shop_names,
    'Address': shop_addresses
})

# CSV 파일로 저장
df.to_csv('nokidsZone.csv', encoding='utf-8-sig', index=False)

# 웹 드라이버 종료
driver.quit()
