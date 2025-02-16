from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess
from selenium.webdriver.common.by import By


# Đường dẫn đến thư mục user data của Chrome
user_data_dir = "C:/Path/To/Chrome/news-us"

# Tạo đối tượng ChromeOptions
chrome_options = Options()

# Chỉ định đường dẫn đến thư mục user data
chrome_options.add_argument(f"user-data-dir={user_data_dir}")
chrome_options.add_argument("profile-directory=Default")  # Nếu bạn muốn sử dụng profile mặc định
chrome_options.add_argument("--headless")  # Chạy trong chế độ không giao diện
chrome_options.add_argument("--disable-gpu")  # Tắt GPU (thường dùng trong môi trường máy chủ)

# Sử dụng Service để chỉ định ChromeDriver
service = Service(ChromeDriverManager().install())


# Khởi tạo WebDriver với các tùy chọn
driver = webdriver.Chrome(service=service, options=chrome_options)

# Mở trang web
driver.get("https://youtube.com")


