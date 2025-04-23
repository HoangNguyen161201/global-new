from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Khởi tạo trình duyệt
options = Options()
options.add_argument("--start-maximized")  # Tùy chọn: mở rộng trình duyệt
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Link Amazon cần mở (rút gọn)
url = "https://www.amazon.com/Crocs-Unisex-Classic-Black-Women/dp/B0014C2NBC/ref=zg_bs_c_fashion_d_sccl_2/141-6250380-7856552?pd_rd_w=QxANf&content-id=amzn1.sym.7379aab7-0dd8-4729-b0b5-2074f1cb413d&pf_rd_p=7379aab7-0dd8-4729-b0b5-2074f1cb413d&pf_rd_r=3G2C974ARBS64BXDZPYY&pd_rd_wg=A9qdA&pd_rd_r=d5149036-2913-475c-84c8-da0d40c49dfb&pd_rd_i=B0014C2NBC&psc=1"

# Mở trang
driver.get(url)
time.sleep(10)
