from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def random_wait(min_time=2, max_time=5):
    time.sleep(random.uniform(min_time, max_time))

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.get('https://www.commencis.com')
print("Ana sayfa açıldı.")

wait = WebDriverWait(driver, 10) 

try:
    insights_menu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='insights']")))
    insights_menu.click()
    print("Insights menüsüne tıklandı.")

    blogs_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Blog')]")))
    blogs_link.click()
    print("Blogs sayfasına tıklandı.")

    popular_blogs_xpath = "/html/body/div[3]/div/div[2]/div/div/div/article/div/div/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div/div/div//h3/a"
    popular_blogs = wait.until(EC.presence_of_all_elements_located((By.XPATH, popular_blogs_xpath)))
    assert len(popular_blogs) >= 4, "En az 4 popüler blog girdisi bulunamadı"
    print("Popüler blog girdileri başarıyla bulundu.")

    for i in range(0, 4): 
        popular_blogs = wait.until(EC.presence_of_all_elements_located((By.XPATH, popular_blogs_xpath)))
        blog = popular_blogs[i]
        blog_title = blog.text.strip()
        print(f"\n{i+1}. popüler blog başlığı: {blog_title}")
        
        driver.execute_script("arguments[0].click();", blog)
        random_wait(3, 5)
        
        try:
            author_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-article-section"]/div/div/div[2]/div/div/div/div/div[7]/div[2]/div/h3')))
            author_name = author_element.text.strip()
            print(f"{i+1}. popüler blog yazısının yazarı: {author_name}")
        except Exception as e:
            print(f"{i+1}. popüler blog yazısının yazarı bulunamadı: {e}")
        
        try:
            favicon_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-article-section"]/div/div/div[2]/div/div/div/div/div[7]/div[1]/span/picture/img')))
            favicon_src = favicon_element.get_attribute('src')
            if 'favicon_commencis.png' in favicon_src:
                print("Commencis Favicon Bulundu")
            else:
                print("Commencis Favicon Bulunamadı")
        except Exception as e:
            print(f"Favicon kontrolü yapılırken hata oluştu: {e}")

        try:
            context_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-article-section"]/div/div/div[2]/div/div/div/div/div[2]/p/span/span[2]')))
            context_value = int(context_element.text.strip())
            if context_value > 0:
                print("Blog'da Context Bulundu!")
            else:
                print("Blog'da Context Bulunamadı.")
        except Exception as e:
            print(f"Context kontrolü yapılırken hata oluştu: {e}")

        try:
            date_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'date-info')))
            date_text = date_element.text.strip()
            print(f"Blog tarihi: {date_text}")
        except Exception as e:
            print("Tarih bulunamadı")

        try:
            email_input = driver.find_element(By.XPATH, "//input[@placeholder='Your e-mail']")
            print("E-posta input alanı bulundu.")
        except Exception as e:
            print("E-posta input alanı bulunamadı.")

        try:
            submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
            print("Stay Tuned Butonu bulundu")
        except Exception as e:
            print("Stay Tuned Butonu bulunamadı.")

        driver.back()
        random_wait(2, 4)

        wait.until(EC.presence_of_element_located((By.XPATH, popular_blogs_xpath)))

except Exception as e:
    print(f"Bir hata oluştu: {e}")
finally:
    driver.quit()