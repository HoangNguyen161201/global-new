import google.generativeai as genai
import asyncio
import edge_tts
import cv2
import requests
from moviepy import TextClip, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, concatenate_audioclips
import os
from PIL import Image, ImageDraw, ImageFont
from data import edge_voice_data
import subprocess
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import base64
import ffmpeg
import numpy as np
from datetime import datetime, timedelta
import random
import textwrap
import pillow_avif
from io import BytesIO
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import uuid
import pyperclip
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import shutil
from bson import ObjectId

# # nếu tải pip install kokoro
from kokoro import KPipeline
from moviepy import AudioFileClip, concatenate_audioclips
import soundfile as sf
from data import gif_paths, person_img_paths, gemini_keys



# lấy tất cả các link có trong tin tức
def get_all_link_in_theguardian_new():
    url = 'https://www.theguardian.com/world'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    link = []
    # Lọc các thẻ <a> thỏa điều kiện
    for a in soup.find_all('a', href=True):
        data_link = a.get('data-link-name', '')
        if 'card-@1' in data_link and 'live' not in data_link:
            link.append(a['href'])
    return link


# lấy thông tin của tin tức bao gồm title, des, tags, content, img
def get_info_new(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # title, description and content
        title = None
        meta_tag = soup.find('meta', attrs={'property': 'og:title'})
        if meta_tag:
            title = meta_tag.get('content', None)

        description = None
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            description = meta_tag.get('content', None)

        tags = None
        meta_tag = soup.find('meta', attrs={'property': 'article:tag'})
        if meta_tag:
            tags = meta_tag.get('content', None)

        content = soup.find('div', {'id': 'maincontent'}).get_text()

        # pictures
        pictures = soup.find_all('picture', class_='dcr-evn1e9')
        picture_links = []
        for item in pictures:
            source = item.find(['source', 'img'], srcset = True)
            picture_links.append(source['srcset'])
        if(picture_links.__len__() == 0 or content is None or content is None or content is None or content is None):
            return None
        
        return {
            "content": content,
            "title": title,
            "description": description,
            "tags": tags,
            "picture_links": picture_links
        }
    except:
      return None

# đếm số lượng thư mục có trong thư mục chính
def count_folders(path):
    # Kiểm tra xem đường dẫn tồn tại không
    if not os.path.exists(path):
        print(fr"Đường dẫn không tồn tại {path}")
        return
    
    # Đếm số lượng thư mục
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return len(folders)

# # lấy ngẫu nhiên đường dẫn hình ảnh và hình động người thuyết trình
def get_img_gif_person():
    index_path = random.randint(0, 3)
    return {
        'person_img_path': person_img_paths[index_path],
        'person_gif_path': gif_paths[index_path]    
    } 

# tải và tạo ra hình ảnh gốc và hình ảnh mờ 
def generate_image(link, out_path, out_blur_path, width=1920, height=1080):
    def resize_to_fit(image, max_width, max_height):
        h, w = image.shape[:2]
        scale = min(max_width / w, max_height / h, 1.0)  # chỉ scale nhỏ
        return cv2.resize(image, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    response = requests.get(link)
    if response.status_code != 200:
        print("Yêu cầu không thành công. Mã trạng thái:", response.status_code)
        return

    with open(out_path, "wb") as f:
        f.write(response.content)

    image = cv2.imread(out_path)
    image = image[150:-150, 150:-150]

    # === ẢNH BLUR ===
    blurred = cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_AREA)
    blurred = cv2.copyMakeBorder(blurred, 25, 25, 25, 25, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    blurred = cv2.GaussianBlur(blurred, (0, 0), 15)

    # === ẢNH CHÍNH ===
    image_resized = resize_to_fit(image, 1840, 1000)
    image_with_border = cv2.copyMakeBorder(image_resized, 25, 25, 25, 25, cv2.BORDER_CONSTANT, value=(255, 255, 255))

    # Ghi kết quả
    cv2.imwrite(out_path, image_with_border)
    cv2.imwrite(out_blur_path, blurred)


# tạo ra các phần nhỏ video từ hình ảnh đã tải về
def generate_video_by_image(zoom_in, in_path, blur_in_path, out_path, second, gif_path):
    width, height = 1920, 1080
    duration = second

    os.makedirs('./temp', exist_ok=True)

    cmd = [
        'ffmpeg',
        '-y',
        '-loop', '1', '-t', str(duration), '-i', blur_in_path,           # [0] blur background
        '-loop', '1', '-t', str(duration), '-i', in_path,                # [1] foreground
        '-stream_loop', '-1', '-i', gif_path,                            # [2] gif looped
        '-loop', '1', '-t', str(duration), '-i', './public/avatar.png',  # [3] avatar
        '-filter_complex',
        f"""
        [0:v]setsar=1,setpts=PTS-STARTPTS[bg];
        [1:v]setsar=1,setpts=PTS-STARTPTS[fg];
        [2:v]scale={int(width*0.8)}:{int(height*0.8)},trim=duration={duration},setpts=PTS-STARTPTS[gif];
        [3:v]scale=200:200,format=rgba,colorchannelmixer=aa=0.7,setsar=1[avatar];
        [bg][fg]overlay=(W-w)/2:(H-h)/2[tmp1];
        [tmp1][gif]overlay=0:250[tmp2];
        [tmp2][avatar]overlay=1650:50
        """.replace('\n', ''),
        '-t', str(duration),
        '-r', '24',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        out_path
    ]

    # === Run FFmpeg with progress ===
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    total_frames = duration * 24
    pbar = tqdm(total=total_frames, desc="Rendering", unit="frame")

    for line in process.stderr:
        if "frame=" in line:
            parts = line.strip().split()
            for part in parts:
                if part.startswith("frame="):
                    try:
                        frame_number = int(part.split('=')[1])
                        pbar.n = frame_number
                        pbar.refresh()
                    except:
                        pass
    pbar.close()

    process.wait()
    if process.returncode != 0:
        raise Exception("FFmpeg failed")


# tạo lại title và description
def generate_title_description_improved(title, description):
    while True:
        title_des = generate_content(f'''tôi đang có các thông tin như sau:
                                    - title: {title}
                                    - description: {description}
                                    hãy generate lại các thông tin trên cho tôi bằng tiếng anh sao cho hay và nổi bật, chuẩn seo youtube.
                                    Trả ra dưới định dạng như sau:
                                    Dòng 1: là title (trên 50 ký tự và không quá 100 ký tự, không được có dấu : trong title).
                                    Từ dòng thứ 2 trở đi: là description. 
                                    Trả ra kết quả cho tôi luôn, không cần phải giải thích hay ghi thêm gì hết.''',
                                    api_key= gemini_keys[2]
                        )
        
        lines = title_des.splitlines()
        title_line = lines[0].strip()
        if len(title_line) < 100:
            desc = "\n".join(lines[1:]).strip()
            desc = re.sub(r'[ \t]+', ' ', desc)
            return {
                "title": title_line,
                "description": desc
            }

# tạo lại nội dung content
def generate_content_improved(content, title):
    return generate_content(f'''
        Tôi có một bản tin mới. Hãy viết lại bằng tiếng Anh sao cho hấp dẫn, súc tích và phù hợp để đọc lên trong một video tin tức trên YouTube (voice-over). Nội dung cần được viết dưới dạng khách quan ở ngôi thứ ba, không dùng "I", "my", "we", hay bất kỳ đại từ ngôi thứ nhất nào.
        title là: {title},
        Nội dung là: {content}

        Yêu cầu:
        - độ dài ký tự bằng hoặc trên {content.__len__()} ký tự.
        - Viết thành một đoạn văn liền mạch, không chia cảnh, không dùng markdown, không có dấu *, **, hoặc [Scene:].
        - Phong cách giống người dẫn bản tin truyền hình, mang tính tường thuật khách quan nhưng thu hút, gây tò mò và khơi gợi cảm xúc.
        - Không thêm bất kỳ lời giải thích nào. Chỉ trả về nội dung đã viết lại.
        ''', api_key= gemini_keys[2])
        
        


# tạo voice thông qua microsoft voice
def generate_to_voice_edge(content: str, output_path: str, voice: str = "en-US-AriaNeural", rate="+5%", pitch="-5Hz", chunk_size=500):
    def split_text_by_dot(text, max_length):
        sentences = text.split(".")
        chunks = []
        current = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            if len(current) + len(sentence) + 1 <= max_length:
                current += sentence + ". "
            else:
                chunks.append(current.strip())
                current = sentence + ". "
        if current:
            chunks.append(current.strip())
        return chunks

    async def _run():
        temp_dir = "__temp_voice_edge__"
        os.makedirs(temp_dir, exist_ok=True)
        temp_files = []

        chunks = split_text_by_dot(content, chunk_size)

        for i, chunk in enumerate(tqdm(chunks, desc="TTS Chunks")):
            file_path = os.path.join(temp_dir, f"chunk_{i}_{uuid.uuid4().hex}.mp3")
            tts = edge_tts.Communicate(text=chunk, voice=voice, rate=rate, pitch=pitch)
            await tts.save(file_path)
            temp_files.append(file_path)

        # Tạo concat list
        concat_path = os.path.join(temp_dir, "concat.txt")
        with open(concat_path, "w", encoding="utf-8") as f:
            for file in temp_files:
                f.write(f"file '{os.path.abspath(file).replace('\\', '/')}'\n")

        print("🔊 Merging audio files...")
        process = subprocess.Popen(
            [
                "ffmpeg", "-f", "concat", "-safe", "0",
                "-i", concat_path,
                "-c", "copy", "-y", output_path
            ],
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        for line in tqdm(process.stderr, desc="Merging", unit="line"):
            pass

        process.wait()

        # Cleanup
        for file in temp_files + [concat_path]:
            try: os.remove(file)
            except: pass
        try: os.rmdir(temp_dir)
        except: pass

        print(f"✅ Done! Saved to {output_path}")

    asyncio.run(_run())


def normalize_audio(input_audio, output_audio):
    command = [
        "ffmpeg", "-y",
        "-i", input_audio,
        "-ac", "2",
        "-ar", "44100",
        "-c:a", "aac",
        "-b:a", "192k",
        output_audio
    ]
    subprocess.run(command)

# gắn âm thanh vào video
def import_audio_to_video(in_path, out_path, audio_duration, audio_path):
    command = [
        "ffmpeg", "-y",
        "-i", in_path,               # Đường dẫn video đầu vào
        "-i", audio_path,            # Đường dẫn âm thanh đầu vào
        "-t", str(audio_duration),   # Đặt thời gian cho video theo độ dài âm thanh
        "-filter:v", "scale=1920:1080,fps=30",  # Bộ lọc video
        "-c:v", "libx264",           # Sử dụng codec video h.264
        "-c:a", "aac",               # Sử dụng codec âm thanh AAC
        "-b:a", "192k",              # Cài đặt bitrate âm thanh
        "-preset", "fast",           # Cài đặt preset nhanh
        "-map", "0:v:0",             # Chỉ định video từ stream đầu tiên (video)
        "-map", "1:a:0",             # Chỉ định audio từ stream thứ hai (audio)
        out_path                     # Đường dẫn đầu ra
    ]
    subprocess.run(command)

# hoàn thành video
def concat_content_videos(intro_path, short_link_path, audio_path, audio_out_path, video_path_list, out_path, draf_out_path, draf_out_path_2):
    # Load âm thanh
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration

    duration_video = 0
    index = 0
    video_path_list_concat = []

    normalize_audio(audio_path, audio_out_path)

    while duration_video < audio_duration:
        video = VideoFileClip(video_path_list[index])
        video_path_list_concat.append(video_path_list[index])
        duration_video += video.duration
        if(index + 1 == video_path_list.__len__()):
            index = 0
        else:
            index += 1
        video.close()

    # Tạo file danh sách tạm thời
    list_file = "video_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for path in video_path_list_concat:
            f.write(f"file '{os.path.abspath(path)}'\n")

    # nối các video lại với nhau
    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        draf_out_path,
        "-progress", "-",
        "-nostats"
    ]

    # Chạy và hiển thị tiến trình
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        line = line.strip()
        if line.startswith("frame=") or "out_time=" in line or "progress=" in line:
            print(line)

    process.wait()

    # cắt đúng duration và gắn âm thanh
    import_audio_to_video(draf_out_path, draf_out_path_2, audio_duration, audio_out_path)


    # nối intro với video
    with open(list_file, "w", encoding="utf-8") as f:
        f.write(f"file '{os.path.abspath(intro_path)}'\n")
        if short_link_path is not None:
            f.write(f"file '{os.path.abspath(short_link_path)}'\n")
        f.write(f"file '{os.path.abspath(draf_out_path_2)}'\n")

    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264",       # Re-encode video
        "-c:a", "aac",           # Re-encode audio
        "-b:a", "192k",          # Bitrate audio
        "-preset", "fast",
        out_path
    ]

    subprocess.run(command)
    os.remove(list_file)
    audio.close()

def normalize_video(input_path, output_path):
    """Chuẩn hóa 1 video để tránh lỗi concat."""
    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-c:a", "aac",            # Chuyển âm thanh về codec aac
        "-b:a", "192k",           # Bitrate âm thanh
        "-ar", "44100",           # Tần số mẫu 44100Hz
        "-ac", "2", 
        "-vf", "fps=30,format=yuv420p",
        "-af", "aresample=async=1",
        "-preset", "fast",
        "-crf", "23",
        output_path
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# dùng gemini để tạo content
def generate_content(content, model='gemini-1.5-flash', api_key= gemini_keys[0]):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model)
    response = model.generate_content(content)
    return response.text


# tạo ra thumbnail
def generate_thumbnail(img_path, img_blur_path, img_person_path, draf_path, out_path, text):
    text = text.upper()
    # Mở ảnh thứ nhất (ảnh nền chính)
    background = Image.open(img_path)
    bg_w, bg_h = background.size
    percent = ((1920 - 60) / bg_w) if ((1920 - 60) / bg_w) * bg_h < 1020 else (1020 / bg_h)
    background = background.resize((int(bg_w * percent),int(bg_h * percent)))

    # Mở ảnh thứ hai (ảnh nền phụ) và thay đổi kích thước
    background_2 = Image.open(img_blur_path)
    background_2 = background_2.resize((1920, 1080))

    # Mở ảnh overlay (PNG trong suốt)
    overlay = Image.open(img_person_path)
    overlay = overlay.resize((int(1920 * 0.8), int(1080 * 0.8)))
    overlay2 = Image.open('./public/bar.png')

    # Đảm bảo ảnh overlay có kênh alpha
    if overlay.mode != 'RGBA':
        overlay = overlay.convert('RGBA')

    # Tính toán vị trí để đặt ảnh nền chính vào giữa ảnh nền phụ
    bg2_w, bg2_h = background_2.size
    x = (bg2_w - int(bg_w * percent)) // 2
    y = (bg2_h - int(bg_h * percent)) // 2

    # Dán ảnh nền chính vào giữa ảnh nền phụ
    background_2.paste(background, (x, y))

    # Dán ảnh overlay lên ảnh nền chính
    background_2.paste(overlay, (0, 250), overlay)
    background_2.paste(overlay2, (0, 0), overlay2)
    
       # Thêm văn bản vào ảnh
    draw = ImageDraw.Draw(background_2)
    font = ImageFont.truetype("./fonts/arial/arial.ttf", 55)  # Đặt font và kích thước font
    max_width = 1350
    lines = []

    # Tách văn bản thành các dòng có độ dài tối đa là 1000 pixel
    words = text.split()
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        test_width = bbox[2] - bbox[0]
        if test_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    # Tính tổng chiều cao của tất cả các dòng văn bản
    total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines) + (len(lines) - 1) * 5

    # Tính toán vị trí y ban đầu để căn giữa theo chiều dọc
    box_height = 380
    y_text_start = bg2_h - box_height + (box_height - total_text_height) // 2

    # Vẽ các dòng văn bản vào ảnh
    x_text = 480  # Khoảng cách từ trái sang
    y_text = y_text_start

    for line in lines:  # Vẽ từ trên xuống dưới
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        # Vẽ văn bản nhiều lần để làm đậm chữ
        for offset in [
    (0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1),
    (2, 0), (0, 2), (2, 2), (-2, 0), (0, -2), (-2, -2), (2, -2), (-2, 2)
]:
            draw.text((x_text + offset[0], y_text + offset[1]), line, font=font, fill="white")
        y_text += int(line_height * 1.8)

    # Lưu ảnh draf 
    background_2.save(draf_path)

    # lưu ảnh với bg 
    jpg_image = Image.open(draf_path)  
    png_image = Image.open('./public/bg/bg-1.png')
    png_image = png_image.convert("RGBA")
    jpg_image.paste(png_image, (0, 0), png_image)
    jpg_image.save(out_path)


# đẩy lên youtube
def upload_yt( user_data_dir, title, description, tags, video_path, video_thumbnail, comment = None):
    ### dùng để tạo ra 1 user
    # chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    # user_data_dir = "C:/Path/To/Chrome/news-us"
    # subprocess.Popen([chrome_path, f'--remote-debugging-port=9223', f'--user-data-dir={user_data_dir}'])
    # time.sleep(5)


    # Tạo đối tượng ChromeOptions
    chrome_options = Options()

    # Chỉ định đường dẫn đến thư mục user data
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("profile-directory=Default")  # Nếu bạn muốn sử dụng profile mặc định
    # chrome_options.add_argument("--headless")  # Chạy trong chế độ không giao diện
    # chrome_options.add_argument("--disable-gpu")  # Tắt GPU (thường dùng trong môi trường máy chủ)

    # Sử dụng Service để chỉ định ChromeDriver
    service = Service(ChromeDriverManager().install())


    # Khởi tạo WebDriver với các tùy chọn
    browser = webdriver.Chrome(service=service, options=chrome_options)

    browser.get("https://studio.youtube.com/")
    # await browser load end
    WebDriverWait(browser, 100).until(
        EC.presence_of_all_elements_located((By.ID, 'create-icon'))
    )


    browser.find_element(By.ID, 'create-icon').click()
    time.sleep(1)

    browser.find_element(By.ID, 'text-item-0').click()
    time.sleep(10)

    # upload video
    print('upload video in youtube')
    file_input = browser.find_elements(By.TAG_NAME, 'input')[1]
    file_input.send_keys(video_path)
    time.sleep(3)


    # upload thumbnail
    print('upload thumbnail in youtube')
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'file-loader'))
    )
    thumbnail_input = browser.find_element(By.ID, 'file-loader')
    thumbnail_input.send_keys(video_thumbnail)
    time.sleep(3)


    # enter title
    print('nhập title in youtube')
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'textbox'))
    )
    title_input = browser.find_element(By.ID, 'textbox')
    title_input.clear()
    time.sleep(1)
    title_input.send_keys(title)
    time.sleep(1)

    # enter description
    print('nhập description in youtube')
    des_input = browser.find_elements(By.ID, 'textbox')[1]
    des_input.clear()
    time.sleep(1)
    # Copy vào clipboard
    pyperclip.copy(description)
    des_input.click()
    time.sleep(1)
    des_input.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # enter hiển thị thêm
    # Đợi cho phần tử scrollable-content xuất hiện
    scrollable_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "scrollable-content"))
    )
    # Scroll xuống cuối cùng của phần tử scrollable-content
    browser.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_element)
    time.sleep(2)

    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'toggle-button'))
    )
    show_more_btn = browser.find_element(By.ID, 'toggle-button')
    show_more_btn.click()
    time.sleep(2)

    # enter tags
    print('nhập tags in youtube')
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'text-input'))
    )
    tags_input = browser.find_element(By.ID, 'text-input')
    tags_input.send_keys(tags)
    time.sleep(2)

    # next btn
    browser.find_element(By.ID, 'next-button').click()
    time.sleep(2)

    # # add end screens
    # WebDriverWait(browser, 10).until(
    #     EC.presence_of_all_elements_located((By.ID, 'endscreens-button'))
    # )
    # browser.find_element(By.ID, 'endscreens-button').click()
    # time.sleep(2)
    # canvas_element = WebDriverWait(browser, 10).until(
    #     EC.element_to_be_clickable((By.TAG_NAME, "canvas"))
    # )
    # browser.execute_script("arguments[0].click();", canvas_element)
    # time.sleep(2)
    # browser.find_element(By.ID, 'save-button').click()
    # time.sleep(4)

    # next
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'next-button'))
    )
    browser.find_element(By.ID, 'next-button').click()
    time.sleep(2)

    while True:
        element = browser.find_elements(By.XPATH, '//*[@check-status="UPLOAD_CHECKS_DATA_COPYRIGHT_STATUS_COMPLETED" or @check-status="UPLOAD_CHECKS_DATA_COPYRIGHT_STATUS_STARTED"]')
        
        if element:
            break  # Thoát vòng lặp nếu tìm thấy

        print("Chưa tìm thấy, tiếp tục kiểm tra...")
        time.sleep(2)  # Đợi 2 giây trước khi kiểm tra lại

    browser.find_element(By.ID, 'next-button').click()
    time.sleep(2)


    # done
    print('upload video in youtube thành công')
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'done-button'))
    )
    browser.find_element(By.ID, 'done-button').click()

    # vào youtube để nhập bình luận
    if comment is not None:
        WebDriverWait(browser, 100).until(
            EC.presence_of_all_elements_located((By.ID, 'share-url'))
        )
        link_redirect = browser.find_element(By.ID, 'share-url')
        href = link_redirect.get_attribute('href')
        browser.get(href)
        WebDriverWait(browser, 100).until(
            EC.presence_of_all_elements_located((By.ID, 'above-the-fold'))
        )
        time.sleep(5)
        is_Find_comment = False
        while  is_Find_comment is False:
            try:
                browser.execute_script("window.scrollBy(0, 50);")
                time.sleep(1)
                comment_box = browser.find_element(By.ID, 'simplebox-placeholder')
                if(comment_box):
                    is_Find_comment = True
                time.sleep(3)
            except:
                time.sleep(3)

        comment_box = browser.find_element(By.ID, 'simplebox-placeholder')
        comment_box.click()
        textarea = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#contenteditable-root[contenteditable='true']"))
        )
        pyperclip.copy(comment)
        textarea.click()
        time.sleep(1)
        textarea.send_keys(Keys.CONTROL, 'v')
        time.sleep(2)
        submit_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "submit-button"))
        )
        submit_button.click()

    time.sleep(10)
    browser.quit()

def create_shortened_link(original_url, api_key = '660f5cdd35747f5488cd1c93c0980afdf7385a71') -> str | None:
    try:
        response = requests.get(
            "https://exe.io/api",
            params={"api": api_key, "url": original_url},
            timeout=10
        )
        data = response.json()

        if data.get("status") == "success" and "shortenedUrl" in data:
            return data["shortenedUrl"]
        else:
            return None
    except Exception as e:
        return None
    
# đẩy lên youtube
def upload_rumble( user_data_dir, title, description, tags, video_path, video_thumbnail):
    ### dùng để tạo ra 1 user
    # chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    # user_data_dir = "C:/Path/To/Chrome/news-us"
    # subprocess.Popen([chrome_path, f'--remote-debugging-port=9223', f'--user-data-dir={user_data_dir}'])
    # time.sleep(5)


    # Tạo đối tượng ChromeOptions
    chrome_options = Options()

    # Chỉ định đường dẫn đến thư mục user data
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("profile-directory=Default")  # Nếu bạn muốn sử dụng profile mặc định
    # chrome_options.add_argument("--headless")  # Chạy trong chế độ không giao diện
    # chrome_options.add_argument("--disable-gpu")  # Tắt GPU (thường dùng trong môi trường máy chủ)

    # Sử dụng Service để chỉ định ChromeDriver
    service = Service(ChromeDriverManager().install())


    # Khởi tạo WebDriver với các tùy chọn
    browser = webdriver.Chrome(service=service, options=chrome_options)

    browser.get("https://rumble.com/upload.php")

    # await browser load end
    WebDriverWait(browser, 100).until(
        EC.presence_of_all_elements_located((By.ID, 'Filedata'))
    )

    # đẩy video lên
    file_input = browser.find_element(By.ID, 'Filedata')
    file_input.send_keys(video_path)
    time.sleep(3)

    WebDriverWait(browser, 100).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'num_percent'))
    )

    is_100_percent = False
    while is_100_percent is False:   
        top_percent = browser.find_element(By.CLASS_NAME, 'num_percent')
        top_percent_text = top_percent.text

        # Kiểm tra có chứa '100%' hay không
        if "100%" in top_percent_text:
            is_100_percent = True
        time.sleep(1)


    # enter title
    print('nhập title in youtube')
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'title'))
    )
    title_input = browser.find_element(By.ID, 'title')
    title_input.clear()
    time.sleep(1)
    title_input.send_keys(title)
    time.sleep(1)

    # enter description
    print('nhập description in youtube')
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'description'))
    )
    des_input = browser.find_element(By.ID, 'description')
    des_input.clear()
    time.sleep(1)
    # Copy vào clipboard
    pyperclip.copy(description)
    des_input.click()
    time.sleep(1)
    des_input.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

   
    #chọn tài khoản để đẩy video
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'channelId_0'))
    )
    account_checkbox = browser.find_element(By.ID, 'channelId_0')
    browser.execute_script("arguments[0].click();", account_checkbox)
    time.sleep(1)

    # chọn news category
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'select-search-input'))
    ) 

    input_element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "select-search-input"))
    )
    input_element.click()

    option_element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@class="select-option" and @data-label="News"]'))
    )
    option_element.click()
    time.sleep(3)

    # upload thumbnail
    print('upload thumbnail in youtube')
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'customThumb'))
    )
    thumbnail_input = browser.find_element(By.ID, 'customThumb')
    thumbnail_input.send_keys(video_thumbnail)
    time.sleep(3)
    
    # enter tags
    print('nhập tags in youtube')
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'tags'))
    )
    tags_input = browser.find_element(By.ID, 'tags')
    tags_input.send_keys(tags)
    time.sleep(2)

    # Scroll xuống cuối cùng của phần tử scrollable-content
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # nhấn nút tiếp tục
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'submitForm'))
    )
    submitForm = browser.find_element(By.ID, 'submitForm')
    submitForm.click()

    # chấp nhật các mọi quyền của rumble
    time.sleep(3)
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'crights'))
    )
    checkbox = browser.find_element(By.ID, 'crights')
    browser.execute_script("arguments[0].click();", checkbox)
    time.sleep(1)
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'cterms'))
    )
    checkbox = browser.find_element(By.ID, 'cterms')
    browser.execute_script("arguments[0].click();", checkbox)

    # Scroll xuống cuối cùng của phần tử scrollable-content
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # nhấn nút tiếp tục
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'submitForm2'))
    )
    submitForm = browser.find_element(By.ID, 'submitForm2')
    submitForm.click()
    time.sleep(3)

    WebDriverWait(browser, 100).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'upload-video-title'))
    )

    is_success = False
    while is_success is False:   
        title_success = browser.find_element(By.CLASS_NAME, 'upload-video-title')
        title_success_text = title_success.text

        # Kiểm tra có chứa 'Upload, share and license your videos' hay không
        if "Upload, share and license your videos" in title_success_text:
            is_success = True
        print('đợi')
        time.sleep(1)
    

    time.sleep(5)
    browser.quit()


def insert_short_link_affiniate(cookie_string):
    uri = "mongodb+srv://hoangdev161201:Cuem161201@cluster0.3o8ba2h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["news"]
    collection = db["link_affs"]
    
    number_page = 1
    url_index = random.randint(0, 2)
    urls = ['https://portals.aliexpress.com/material/productRecommend.do?requireCouponCode=&freeShipping=&shipTo=US&currency=USD&language=en&pageSize=11&type=1&pageNum=',
            'https://portals.aliexpress.com/material/productRecommend.do?requireCouponCode=&freeShipping=&shipTo=US&currency=USD&language=en&pageSize=11&type=2&pageNum=',
            'https://portals.aliexpress.com/material/productRecommend.do?requireCouponCode=&freeShipping=&specialOffer=all_plan&shipTo=US&currency=USD&language=en&pageSize=11&type=1&pageNum='
            ]
    url_get_link_aff = 'https://portals.aliexpress.com/promote/promoteNow.do?trackingId=default&language=en_US&shipTo=US&currency=USD&subChannel=hd&productId='

    # BƯỚC 2: Tách cookie thành dict để truyền vào requests
    cookies = {}
    for pair in cookie_string.split("; "):
        if "=" in pair:
            key, value = pair.split("=", 1)
            cookies[key] = value
    

    # Danh sách kết quả rút gọn
    simplified_items = []

    while simplified_items.__len__() < 10:
        url = f'{urls[url_index]}{number_page}'

        response = requests.get(url, cookies=cookies)

        if response.status_code == 200:
            data = response.json()
            items = data.get("data", {}).get("results", [])

            simplified_items_state = []
            for item in items:
                simplified_items_state.append({
                    "itemId": item.get("itemId"),
                    "itemOriginPriceMin": item.get("itemOriginPriceMin"),
                    "itemPriceDiscountMin": item.get("itemPriceDiscountMin"),
                    "itemTitle": item.get("itemTitle"),
                    "itemMainPic": item.get("itemMainPic"),
                    "totalTranpro3Semantic": item.get("totalTranpro3Semantic"),
                    "itemUrl": item.get("itemUrl"),
                })
            
            item_ids = [item["itemId"] for item in simplified_items_state if item.get("itemId")]
            
            # tìm ra sản phẩm đã trùng
            existing_docs = list(collection.find({"itemId": {"$in": item_ids}}))
            existing_item_ids = {doc["itemId"] for doc in existing_docs}
            simplified_items_state = [item for item in simplified_items_state if item.get("itemId") not in existing_item_ids]
            
            # lấy link affiniate
            if simplified_items_state.__len__() > 0:
                for key, item in enumerate(simplified_items_state):
                    response = requests.get(f'{url_get_link_aff}{item['itemId']}', cookies=cookies)
                    data = response.json()
                    simplified_items_state[key]['affLink'] = data['data']['creativityCopywriters'][0]['promoteUrl']
                    
                    # tạo link exe
                    short_link = create_shortened_link(simplified_items_state[key]['affLink'])
                    simplified_items_state[key]['exeLink'] = short_link
            simplified_items = simplified_items + simplified_items_state

            print(simplified_items)
            print(simplified_items.__len__())
            if(simplified_items.__len__() < 10):
                print('tiếp page tiếp theo')
                number_page += 1
        else:
            print("Lỗi gọi API:", response.status_code)
            return
    if(simplified_items.__len__() >= 10):
        collection.insert_many(simplified_items)

# tạo image để gắn affiniate --------------------------------------------------
def download_and_resize_image(url, size=(399, 399), save_path='output.jpg'):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # báo lỗi nếu không tải được
        image = Image.open(BytesIO(response.content)).convert('RGB')
        
        # Resize theo kích thước cố định (có thể méo hình nếu không đúng tỷ lệ)
        image_resized = image.resize(size)

        image_resized.save(save_path)
        print(f"✅ Saved resized image to {save_path}")
    except Exception as e:
        print(f"❌ Error processing {url}: {e}")

def add_rounded_corners(image: Image.Image, radius: int) -> Image.Image:
    # Tạo mặt nạ hình tròn
    rounded_mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(rounded_mask)
    draw.rounded_rectangle([0, 0, *image.size], radius=radius, fill=255)

    # Áp dụng mask vào ảnh
    rounded_image = image.copy()
    rounded_image.putalpha(rounded_mask)

    return rounded_image

def generate_image_and_video_aff_and_get_three_item(gif_path):
    uri = "mongodb+srv://hoangdev161201:Cuem161201@cluster0.3o8ba2h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["news"]
    collection = db["link_affs"]

    path_folder = f'./pic_affs'
    try:
        shutil.rmtree(path_folder)
    except:
        print('next')
    
    os.makedirs(path_folder)

    # Lấy ngẫu nhiên 3 item
    random_items = list(collection.aggregate([
        {"$sample": {"size": 3}}
    ]))

    # In kết quả
    for i, item in enumerate(random_items):
        download_and_resize_image(item['itemMainPic'], save_path= f'{path_folder}/pic_{i}.png')


    try:
        background = Image.open('./public/bg/aff.png').convert("RGB")
        draw = ImageDraw.Draw(background)

        
        font = ImageFont.truetype("./fonts/arial/arial.ttf", 35)
        font2 = ImageFont.truetype("./fonts/arial/arial.ttf", 29)
        font3 = ImageFont.truetype("./fonts/arial/ARIBL0.ttf", 40)
    

        for i, item in enumerate(random_items):
            foreground = Image.open(f'{path_folder}/pic_{i}.png').convert("RGBA")
            foreground = add_rounded_corners(foreground, 11)
            x = 367 + 498 * i
            y = 240
            background.paste(foreground, (x, y), foreground)
            
            title = item['itemTitle']
            if len(title) > 30:
                title = title[:20] + "..."

            
            percent = ''
            match = re.search(r'\d+(\.\d+)?', item['itemOriginPriceMin'])
            match2 = re.search(r'\d+(\.\d+)?', item['itemPriceDiscountMin'])
            if match and match2:
                number1 = float(match.group())
                number2 = float(match2.group())
                percent = f'-{round(number2 / number1 * 100, 0)}%'


            # Vẽ chữ phía dưới ảnh
            draw.text((x, y + foreground.height + 25), title, fill=(0, 0, 0), font=font)
            draw.text((x, y + foreground.height + 80), f'{item['totalTranpro3Semantic']} Sold', fill=(128, 128, 128), font=font2)
            draw.rounded_rectangle(
                [(x + 230, y), (x + 230 + 170, y + 65)],
                radius=15,  # độ cong của góc
                fill=(255, 255, 255),
                outline=(210, 210, 210)
            )
            draw.text((x + 240, y), percent, fill=(255, 0, 0), font=font3)
            # draw.text((x, y + foreground.height + 130), f'{item['itemPriceDiscountMin']}', fill=(255, 99, 71), font=font3)
            # bbox = draw.textbbox((0, 0), f"{item['itemPriceDiscountMin']}", font=font3)
            # text_width = bbox[2] - bbox[0] + 20
            # draw.text((x + text_width, y + foreground.height + 145), f'{item['itemOriginPriceMin']}', fill=(96, 96, 96), font=font2)
            # text_x = x + text_width
            # text_y = y + foreground.height + 145
            # line_y = text_y + 32 // 2
            # bbox = draw.textbbox((0, 0), f"{item['itemOriginPriceMin']}", font=font2)
            # text_width = bbox[2] - bbox[0]
            # draw.line((text_x, line_y, text_x + text_width, line_y), fill=(64, 64, 64), width=1)
        background.save(f'{path_folder}/pic_result.png')

        audio = AudioFileClip('./public/aff.aac')

        generate_video_by_image(None,
                        f'{path_folder}/pic_result.png',
                        f'{path_folder}/pic_result.png',
                        f'{path_folder}/daft.mp4',
                        audio.duration,
                        gif_path
                    )

        import_audio_to_video(f'{path_folder}/daft.mp4', f'{path_folder}/aff.mp4', audio.duration,  './public/aff.aac')
        print(audio.duration)
        
        audio.close()
        print("✅ Done")

        return random_items
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def update_des_for_aff():
    uri = "mongodb+srv://hoangdev161201:Cuem161201@cluster0.3o8ba2h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["news"]
    collection = db["link_affs"]

    # Tìm các document KHÔNG có trường 'itemDes'
    items_without_itemDes = list(collection.find({ "itemDes": { "$exists": False } }, {
        '_id': 1,
        'itemTitle': 1
    }))

    if(items_without_itemDes.__len__() == 0):
        raise Exception("Tất cả link đã thêm hết des")

    # gemini_keys[6]
    data = generate_content(f'''tôi có dữ liệu là: {items_without_itemDes}.
                                Hiện tại tôi đang có kênh tin tức chính trị, tôi muốn bạn hãy viết     
                            Tôi muốn bạn hãy viêt mô tả, tính năng hoặc ghi sao cho để thu hút các đối tượng coi tin tức chính trị trên youtube của tôi muốn nhấn vào link affiniate của tôi cho từng sản phẩn.
                            Để cho từng sản phẩm để tôi có thể gắn vào description video youtube để kêu gọi họ nhấn vào link affiniate của tôi.
                            ghi bằng tiếng anh và độ dài ký tự của mỗi mô tả sản phẩm không quá 130 ký tự.
                            trả ra theo định dạng:
                            dòng 1: id-mô tả sản phẩm 1
                            dòng 2: id-mô tả sản phẩm 2
                            dòng 3: id-mô tả sản phẩm 3
                            trả ra theo đúng định dạng, không ghi thêm hoặc giải thích gì hết.
                            ''', api_key= gemini_keys[6])
    

    # Tìm vị trí của tất cả các ID (24 ký tự hex + '-')
    id_positions = [(m.start(), m.group(0)) for m in re.finditer(r'[a-f0-9]{24}-', data)]

    items = []
    for i in range(len(id_positions)):
        start_pos, full_id = id_positions[i]
        end_pos = id_positions[i + 1][0] if i + 1 < len(id_positions) else len(data)

        _id = full_id[:-1]  # Bỏ dấu '-'
        description = data[start_pos + 25:end_pos].strip()

        items.append({ "_id": _id, "itemDes": description })

    for i in range(len(items)):
        collection.update_one(
            {"_id": ObjectId(items[i]["_id"])},
            {"$set": {"itemDes": items[i]["itemDes"]}}
        )
    
    print(f'update success {items.__len__()}')

    