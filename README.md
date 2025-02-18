# tool-news-linux

1 cấu hình:
- cập nhật lại vps: sudo apt update
- cài đặt git: sudo apt install git (git --version)
- cài đặt python: sudo apt install python3 (python3 --version)
- cài đặt pip: sudo apt install python3-pip (pip3 --version)
- tải chrome: sudo apt install chromium-browser
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

5 tải kokoro-82m:
- cd global-new
- git clone https://github.com/zboyles/Kokoro-82M.git