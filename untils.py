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
from webdriver_manager.chrome import ChromeDriverManager
import base64
import ffmpeg
import numpy as np
from datetime import datetime, timedelta
import random
import textwrap

# # nếu sử dụng https://github.com/zboyles/Kokoro-82M.git
# os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = r"C:\Program Files\eSpeak NG\libespeak-ng.dll"
# os.environ["PHONEMIZER_ESPEAK_PATH"] = r"C:\Program Files\eSpeak NG\espeak-ng.exe"
# from Kokoro.models import build_model
# import torch
# # 3️⃣ Call generate, which returns 24khz audio and the phonemes used
# from Kokoro.kokoro import generate

# # nếu tải pip install kokoro
from kokoro import KPipeline
from moviepy import AudioFileClip, concatenate_audioclips
import soundfile as sf

def generate_content(content):
    genai.configure(api_key="AIzaSyArae1nyjhAiRedUMkrUWd7p_-BJglXBNU")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(content)
    return response.text

def generate_to_voice(content, path):
    async def main() -> None:
        c = edge_tts.Communicate(content, edge_voice_data[6], rate="+5%", pitch="+20Hz")
        await c.save(path)
    asyncio.run(main())

def resize_to_cover(image, target_width, target_height):
    # Get the original dimensions
    original_height, original_width = image.shape[:2]
    
    # Calculate the aspect ratios
    target_aspect = target_width / target_height
    original_aspect = original_width / original_height
    
    # Determine the scaling factor and dimensions to cover the target area
    if original_aspect > target_aspect:
        # Image is wider than target, scale by height
        scale = target_height / original_height
    else:
        # Image is taller than target, scale by width
        scale = target_width / original_width
    
    # Resize the image
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    resized_image = cv2.resize(image, (new_width, new_height))
    
    # Calculate the cropping coordinates
    x_center = new_width // 2
    y_center = new_height // 2
    x_crop = target_width // 2
    y_crop = target_height // 2
    
    # Crop the image to the target dimensions
    cropped_image = resized_image[y_center - y_crop:y_center + y_crop, x_center - x_crop:x_center + x_crop]
    
    return cropped_image

def generate_image(link, out_path, out_blur_path, width = None, height = None):
    response = requests.get(link)
    if response.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(response.content)
    else:
        print("Yêu cầu không thành công. Mã trạng thái:", response.status_code)

    image = cv2.imread(out_path)
    image = image[150:-150, 150:-150]
    blurred_image_edit = None
    if width is not None and height is not None:
        blurred_image_edit  = resize_to_cover(image, width, height)
    else:
        image = cv2.flip(image, 1)
    border_thickness = 25
    border_color = (255, 255, 255)
    blurred_image_edit_2 = cv2.copyMakeBorder(blurred_image_edit if blurred_image_edit is not None else image, border_thickness, border_thickness, border_thickness, border_thickness, cv2.BORDER_CONSTANT, value=border_color)
    image = cv2.copyMakeBorder(image, border_thickness, border_thickness, border_thickness, border_thickness, cv2.BORDER_CONSTANT, value=border_color)

    # Làm mờ hình ảnh bằng Blur
    blurred_image = cv2.GaussianBlur(blurred_image_edit_2, (0, 0), 15)

    cv2.imwrite(out_path, image)
    cv2.imwrite(out_blur_path, blurred_image)

def generate_video_by_image(zoom_in, in_path, blur_in_path, out_path, second, gif_path, is_short = False):
    clip_image = ImageClip(in_path).with_duration(second)
    clip_blurred_image = ImageClip(blur_in_path, duration= second).resized((1080, 1920) if is_short else (1920, 1080))
    clip_blurred_image = clip_blurred_image.resized(lambda t: 1 + 0.3 * t/second)

    if not zoom_in:
        w_clip_image, h_clip_image = clip_image.size
        percent = (960 / w_clip_image) if (960 / w_clip_image) * h_clip_image < 720 else (720 / h_clip_image)
        if is_short:
            percent = (720 / w_clip_image) if (720 / w_clip_image) * h_clip_image < 960 else (960 / h_clip_image)
        clip_image = clip_image.resized((percent * w_clip_image, percent * h_clip_image))
        clip_image = clip_image.resized(lambda t: 1 + 0.4 * t/second)
    else:
        w_clip_image, h_clip_image = clip_image.size
        percent = ((1920 - 60) / w_clip_image) if ((1920 - 60) / w_clip_image) * h_clip_image < 1020 else (1020 / h_clip_image)
        if is_short:
            percent = (1020 / w_clip_image) if (1020 / w_clip_image) * h_clip_image < (1920 - 60) else ((1920 - 60) / h_clip_image)
        clip_image = clip_image.resized((percent * w_clip_image, percent * h_clip_image))
        clip_image = clip_image.resized(lambda t: 1 - 0.3 * t/second)
    
    # add gif
    gif = VideoFileClip(gif_path, has_mask= True)
    percent_gif = 0.8 
    gif = gif.resized((int(1920 * percent_gif), int(1080 * percent_gif)))
    while gif.duration < second:
        gif = concatenate_videoclips([gif, gif])
    gif = gif.subclipped(0, second)

    
    # Tạo avatar clip
    avatar_clip = ImageClip('./public/avatar.png').resized((200, 200))
    avatar_clip = avatar_clip.with_opacity(0.7)
    avatar_clip = avatar_clip.with_position((830 if is_short else 1650,  50))

    final_clip = CompositeVideoClip([
        clip_blurred_image.with_position('center'),
        clip_image.with_position('center'),
        gif.with_position((0, 1080 if is_short else 250)),
        avatar_clip.with_duration(second)
        ])

    final_clip.write_videofile(out_path, fps=24)

def wrap_text(text, width=50):
    return "\n".join(textwrap.wrap(text, width=width))
def concact_content_videos(audio_path, video_path_list, out_path, is_short = False, title_mobile_options = None):
    # Load âm thanh
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration

    # intro video
    intro = VideoFileClip('./public/intro.mp4')
    intro_audio = AudioFileClip(title_mobile_options['title_audio'] if is_short else './public/intro.mp4')
    intro = intro.resized((1080, 1920) if is_short else (1920, 1080))
    intro_duration =  intro.duration
    final_duration = audio_duration + intro_duration

    duration_video = 0
    index = 0
    videos = [] if is_short else [intro]

    bg_mobile_img = Image.open('./public/bg/bg-mobile-1.png').convert("RGBA")
    bg_mobile_array = np.array(bg_mobile_img)
    bg_mobile = ImageClip(bg_mobile_array, duration= 5, is_mask = False, transparent = True)  # Không cố định thời gian ở đây
    bg_mobile = bg_mobile.with_position((0, -700))
 
    bg_mobile = bg_mobile.with_duration(intro.duration)

    while duration_video < final_duration:
        video = VideoFileClip(video_path_list[index])
        if(duration_video + video.duration > final_duration):
            duration_end_video =  duration_video + video.duration - final_duration
            video = video.subclipped(0, duration_end_video)
            duration_video += duration_end_video
        else:
            duration_video += video.duration
        videos.append(video)
        if(index + 1 == video_path_list.__len__()):
            index = 0
        else:
            index += 1

    # Nối video lại với nhau
    final_video = concatenate_videoclips(videos).subclipped(0, final_duration)
    # Ghép video và âm thanh lại với nhau
    final_video = final_video.with_audio(concatenate_audioclips([intro_audio, audio]))
    final_video.write_videofile('./mobile.mp4' if is_short else out_path)
    final_video.close()

    if(is_short):
        name_clip = TextClip(text = wrap_text(title_mobile_options['title'], 20), interline = 10, font_size=70, font="./fonts/arial/arial.ttf",  size=(2000, None), text_align="center").with_position(("center", 330)).with_duration(intro_duration).with_start(0)
        # pronunciation_clip = TextClip(text = wrap_text(animal_options['pronunciation'].upper(), 100), interline = 10, font_size=50, font="C:/Windows/Fonts/Arial.ttf", color='white',  size=(2000, None), text_align="center", stroke_color="black", stroke_width=3).with_position(("center", 730)).with_duration(duration).with_start(0)

        video = VideoFileClip('./mobile.mp4')
        final_video = CompositeVideoClip([video, bg_mobile, name_clip])
        final_video.write_videofile(out_path)
        final_video.close()


def count_folders(path):
    # Kiểm tra xem đường dẫn tồn tại không
    if not os.path.exists(path):
        print(fr"Đường dẫn không tồn tại {path}")
        return
    
    # Đếm số lượng thư mục
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return len(folders)

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

from datetime import datetime, timedelta

class TimeManager:
    current_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=20)

    @staticmethod
    def reset_to_current_time():
        TimeManager.current_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=16)
        print(f"Thời gian đã được reset: {TimeManager.current_time.strftime('%Y-%m-%d %H:%M:%S')}")

    @staticmethod
    def add_30_minutes():
        new_time = TimeManager.current_time + timedelta(minutes=30)
        TimeManager.current_time = new_time
        print(f"Thời gian sau khi cộng 30 phút: {TimeManager.current_time.strftime('%Y-%m-%d %H:%M:%S')}")



def upload_yt( user_data_dir, title, description, tags, video_path, video_thumbnail, is_short = False):
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
    time.sleep(3)

    # upload video
    print('upload video in youtube')
    file_input = browser.find_elements(By.TAG_NAME, 'input')[1]
    file_input.send_keys(video_path)
    time.sleep(3)

    if is_short is False:
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
    title_input.send_keys(title)
    time.sleep(1)

    # enter description
    print('nhập description in youtube')
    des_input = browser.find_elements(By.ID, 'textbox')[1]
    des_input.clear()
    des_input.send_keys(description)
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

    # chọn upload trực tiếp hay lên lịch
    current_time = datetime.now()
    current_hour = current_time.hour

    # # Đặt khoảng thời gian từ 17:00 đến 08:00
    # if (current_hour >= 16 or current_hour < 6) or is_short:
    #     if is_short is False:
    #         TimeManager.reset_to_current_time()
    #     print('Upload trực tiếp')
    # else:
    #     print('lên lịch upload')
    #     schedule_datetime = TimeManager.current_time
    #     formatted_date = schedule_datetime.strftime("%b %d, %Y")  # Thí dụ: "Feb 23, 2025"
    #     formatted_time = schedule_datetime.strftime("%I:%M %p")   # Thí dụ: "01:00 AM"
    #     print(f'lên lịch upload {formatted_date} {formatted_time}')
    #     WebDriverWait(browser, 10).until(
    #         EC.presence_of_all_elements_located((By.ID, 'second-container-expand-button'))
    #     )
    #     browser.find_element(By.ID, 'second-container-expand-button').click()
    #     time.sleep(2)
    #     WebDriverWait(browser, 10).until(
    #         EC.presence_of_all_elements_located((By.XPATH, "//tp-yt-paper-input[@id='textbox']//input[@class='style-scope tp-yt-paper-input']"))
    #     )
    #     time_input = browser.find_element(By.XPATH, "//tp-yt-paper-input[@id='textbox']//input[@class='style-scope tp-yt-paper-input']")
    #     time_input.clear()
    #     time_input.send_keys(formatted_time)
    #     time.sleep(2)
    #     WebDriverWait(browser, 10).until(
    #         EC.presence_of_all_elements_located((By.ID, 'right-icon'))
    #     )
    #     browser.find_element(By.ID, 'right-icon').click()
    #     time.sleep(1)
    #     WebDriverWait(browser, 10).until(
    #         EC.presence_of_all_elements_located((By.XPATH, "//tp-yt-paper-input[@aria-label='Enter date']//input[@class='style-scope tp-yt-paper-input']"))
    #     )
    #     date_input = browser.find_element(By.XPATH, "//tp-yt-paper-input[@aria-label='Enter date']//input[@class='style-scope tp-yt-paper-input']")
    #     date_input.clear()
    #     date_input.send_keys(formatted_date)
    #     time.sleep(1)
    #     date_input.send_keys(Keys.RETURN)
    #     time.sleep(2)
    #     TimeManager.add_30_minutes()
        
        

    # done
    print('upload video in youtube thành công')
    WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'done-button'))
    )
    browser.find_element(By.ID, 'done-button').click()

    time.sleep(10)
    browser.quit()


def split_text(text, max_length=500):
    sentences = text.split('.')
    segments = []
    current_segment = ''
    
    for sentence in sentences:
        # Thêm dấu chấm bị loại bỏ trong quá trình split
        sentence = sentence.strip() + '.'
        
        # Kiểm tra nếu thêm câu hiện tại vào sẽ vượt quá giới hạn
        if len(current_segment) + len(sentence) > max_length:
            segments.append(current_segment.strip())
            current_segment = sentence
        else:
            current_segment += ' ' + sentence
    
    # Thêm đoạn cuối cùng vào danh sách
    if current_segment:
        segments.append(current_segment.strip())
    
    return segments



def generate_voice_google(text, out_path, url):
    is_success = True
    try:
        split_texts = split_text(text, 500)
        audio_paths = []

        for key, item in enumerate(split_texts):
            try_generate = 0
            while try_generate < 3:
                print(try_generate)
                # Dữ liệu JSON cần gửi
                payload = {
                    "input": {
                        "text": item
                    },
                    "voice": {
                        "languageCode": "en-US",
                        "name": "en-US-Journey-F"
                    },
                    "audioConfig": {
                        "audioEncoding": "LINEAR16",
                        "pitch": 0,
                        "speakingRate": 1,
                        "effectsProfileId": ["small-bluetooth-speaker-class-device"]
                    }
                }


                headers = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
                    'content-type': 'text/plain;charset=UTF-8'
                }

                # Gửi yêu cầu POST
                response = requests.post(url, headers=headers, json=payload )

                # Kiểm tra mã trạng thái và in ra phản hồi
                if response.status_code == 200:
                    print(f'generate voice {key} success')
                    audio_data = base64.b64decode(response.json()['audioContent'])
                    with open(f'./audio-{key}.mp3', 'wb') as file:
                        file.write(audio_data)
                    audio_paths.append(f'./audio-{key}.mp3')
                    break
                else:
                    print(response)
                    print('generate voice error')
                    if(try_generate + 1 == 3):
                        is_success = False
                    try_generate += 1
                        

        clips = [AudioFileClip(audio) for audio in audio_paths]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(out_path)
        return is_success
    except:
        return False

# def generate_voice_kokoro(text, out_path):
#     try:
#         text_arr = split_text(text, 500)
#         audio_paths = []
#         for key, item in enumerate(text_arr):
#             audio_path = f'./audio-{key}.mp3'
#             audio_paths.append(audio_path)

#             device = 'cuda' if torch.cuda.is_available() else 'cpu'
#             MODEL = build_model('./Kokoro/kokoro-v0_19.pth', device)
#             VOICE_NAME = [
#                 'af', # Default voice is a 50-50 mix of Bella & Sarah
#                 'af_bella', 'af_sarah', 'am_adam', 'am_michael',
#                 'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis',
#                 'af_nicole', 'af_sky',
#             ][0]
#             VOICEPACK = torch.load(f'./Kokoro/voices/{VOICE_NAME}.pt', weights_only=True).to(device)
#             print(f'Loaded voice: {VOICE_NAME}')

#             audio, out_ps = generate(MODEL, item, VOICEPACK, lang=VOICE_NAME[0])

#             process = (
#                             ffmpeg
#                             .input('pipe:0', format='f32le', ac=1, ar='24000')  # Định dạng đầu vào
#                             .output(audio_path, acodec='libmp3lame', audio_bitrate='192k')
#                             .overwrite_output()
#                             .run_async(pipe_stdin=True)
#                         )

#             # Gửi dữ liệu âm thanh vào ffmpeg
#             process.stdin.write(audio.astype(np.float32).tobytes())
#             process.stdin.close()
#             process.wait()

#         clips = [AudioFileClip(audio) for audio in audio_paths]
#         final_clip = concatenate_audioclips(clips)
#         final_clip.write_audiofile(out_path)
#         return True
            
#     except NameError:
        
#       print('An exception occurred')
#       print(NameError)
#       return False
    
def generate_voice_kokoro_pip(text, out_path):
    try:
        print('generate voice')
        pipeline = KPipeline(lang_code='a') # <= make sure lang_code matches voice

        generator = pipeline(
            text, voice='af_heart', # <= change voice here
            speed=1, split_pattern=r'\n+'
        )

        audio_paths = []
        for i, (gs, ps, audio) in enumerate(generator):
            audio_path = f"./audio_{i}.wav"
            audio_paths.append(audio_path)
            
            sf.write(audio_path, audio, 24000)

        clips = [AudioFileClip(audio) for audio in audio_paths]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(out_path)
        return True
    except:
      print('generate voice error')
      return False 

