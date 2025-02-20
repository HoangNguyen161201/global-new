# tool-news-linux

vpsdime.com

1 cấu hình:
- cập nhật lại vps: sudo apt update
- cài đặt git: sudo apt install git (git --version)
- cài đặt python: sudo apt install python3 (python3 --version)
- cài đặt pip: sudo apt install python3-pip (pip3 --version)
- sudo apt install libglib2.0-0 (nếu cv2 không chạy được)
- sudo apt install libgl1-mesa-glx (nếu cv2 không chạy được)
- tải chrome: sudo apt install chromium-browser, nếu không chạy được phải tải thêm các thư viện phụ thuộc:
-- sudo apt install xdg-utils
-- sudo apt install -y libx11-xcb1 libglu1-mesa libxss1
-- tính năng khác:
--- which chromium-browser (xem path)
--- chromium-browser --version (xem version để dán vào main)
- sudo apt install -y libnss3 libgdk-pixbuf2.0-0 libatk-bridge2.0-0 libatk1.0-0 libgbm1

- tải espeak-ng: sudo apt-get install espeak-ng
- tải screen: sudo apt install screen (
    tạo: screen -S <name>
    thoát mà không tắt screen: Ctrl + A, sau đó nhấn D
    quay lại xem screen: screen -r <name>
    xem danh sách: screen -ls
    xóa: screen -X -S [PID hoặc tên phiên] quit
)

2 clone github: git clone https://github.com/HoangNguyen161201/tool-news-linux.git

3 install libraries:
- tao nơi lưu trữ cache cho pip:
--  mkdir  /pip_cache
--  export TMPDIR=/pip_cache
- sau đó mới tải thư viện:
--  pip install --break-system-packages selenium==4.27.1

4 cách chạy file:
python3 main.py

5 khác:
- rm -r tên_thư_mục: xóa tên thư mục
- mv thumuc_cu thumuc_moi: đổi tên thư mục
