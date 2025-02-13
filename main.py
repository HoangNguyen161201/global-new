from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import os
from untils import generate_content, generate_voice_kokoro, generate_image, generate_video_by_image, concact_content_videos, count_folders, generate_thumbnail, upload_yt
import concurrent.futures
from data import gif_paths, person_img_paths
from slugify import slugify
from db import connect_db, check_link_exists, insert_link,delete_link, get_all_links
from pathlib import Path
import subprocess
from datetime import datetime
import pyglet



# print(get_all_links())
# delete_link('https://www.theguardian.com/us-news/2025/feb/08/trump-and-japanese-pm-ishiba-talk-tariffs-and-vow-to-stand-against-chinese-aggression')
# # insert_link('https://www.theguardian.com/world/article/2024/may/21/gove-accuses-uk-university-protests-of-antisemitism-repurposed-for-instagram-age')
# time.sleep(60)


# chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
# user_data_dir = "C:/Path/To/Chrome/news-us"
# subprocess.Popen([chrome_path, f'--remote-debugging-port=9223', f'--user-data-dir={user_data_dir}'])
# time.sleep(100000)


# is_generate_voice_success = generate_voice_google(
#     'right right right right right right right right right',
#     f"./content-voice.mp3",
#     'https://cxl-services.appspot.com/proxy?url=https://texttospeech.googleapis.com/v1beta1/text:synthesize&token=03AFcWeA5YAQQSWUWISJMznKTgL0dUS-l95FswY4AQpcbpoBQ3ki4yeBM5pX2We3xeB-e9n4g9fz51c9gZNECvOdzgSAdsHdeIj2eKLmcyarojcxRvqqH28gU-NkH76bXgmPCG4RQz-d1zxzoaXerd3YXj1Fflh6c8MsP4ccBXfD9V13UA2ZrRTvJgWBQVqVlAYYfZmZSe-EBhuZGcDzun4VzaGFgJHdONtI7gK-iPaWBFpMuudnvAet1vTIGk_1-Qm1gs7pOW853--sBF-aCj0QtBbJBXgWx1wiQPo1N2bhTlAsbjeg9Iqdz-2gjEh0cLRwCgO_tE28GOc9vr6BSanb5l-I3IEYcyo6qIXaf2Pi6iwHJsX5bT61lFhVGdHsKJGTm0Cxn9mcxqlUHLYBUlQFlpt8Wb819qnEYy-ef_ppvWRsXMFv16hAUCuWDAn9XeagL794b4j0XdSnxsHra61AF_b_mREr0yuJQAN1AGh-EDe8rEovNLwQezFq90_OLeR2978ysiV61UBm9RXl4L0TvfwlZCXO18soAFo6gGJNL05rW_UPlJ1rinkjbNZKc4AHzr4my-xGBkBCfBZ2H2SQ6mxZaxAhSqlicWjMMg2n7GfllqeC-rJoBmBBli3h9ceu78eyE22umVqEMBPbJDaycyRv2b2LuXhLuXr4huo1b7T0hPWwrmATjya9EKoRW1Cqc9WJhMUoQCbmsw2t4yQ7TtC8TEUREDMgkyecW6R-i8smhRK6EkNHsSq1zlJcGmj_GFBZZjp7Nv3hQNS8Li0KnXUc8deIjJLRg9TSi6ew1AMMP7zbKFFz670oyp8mwiaOMboCVYoCgCaMKPOTyoTEpzMYJ9Br5irPKuNJZCMTcqeOmPv41KVmFaKwoLWjibhb2XaeeA0p1N'
# )
# time.sleep(10000)


is_generate_voice_error = False 
connect_db()
while not is_generate_voice_error:
    count_folder = count_folders('./videos')
    path_folder = f'./videos/video-{count_folder}'
    current_link = None

    try:
        while not is_generate_voice_error:
            browser = webdriver.Chrome()
            browser.get('https://www.theguardian.com/world')

            # await browser load end dcr-ezvrjj
            WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'dcr-2yd10d'))
            )

            # get link to redirect to new
            links_elements = browser.find_elements(By.CLASS_NAME, 'dcr-2yd10d')
            links = []
            for element in links_elements:
                if element.get_attribute('data-link-name') == 'news | group-0 | card-@1':
                    links.append(element.get_attribute('href'))
            links.reverse()

            print(links)
            print(links.__len__())


            current_link = None
            for element in links:
                if not check_link_exists(element):
                    current_link = element
                    break

            # khi có curent link -----------------------------------
            if(current_link):
                browser.get(current_link)
                
                # await browser load end
                WebDriverWait(browser, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'h1'))
                )


                try:
                    time.sleep(5)
                    browser.execute_script("arguments[0].remove()", browser.find_element(By.CLASS_NAME, 'dcr-pvn4wq'))
                except:
                    print('khong the xoa dang nhap hoac khong co')
                is_video = False
                try:
                    video_play =  browser.find_element(By.CLASS_NAME, 'play-icon')
                    if(video_play):
                        is_video = True
                except:
                    print('khong co video')

                if not is_video:
                    # title
                    title = browser.find_element(By.TAG_NAME, 'h1').text
                    print(title)

                    # remove ---
                    browser.execute_script("""
                        var elements = document.querySelectorAll('p.dcr-1xjndtj');
                        for (var i = 0; i < elements.length; i++) {
                            elements[i].parentNode.removeChild(elements[i]);
                        }
                    """)
                    browser.execute_script("""
                        var elements = document.querySelectorAll('div.dcr-cn68uf');
                        for (var i = 0; i < elements.length; i++) {
                            elements[i].parentNode.removeChild(elements[i]);
                        }
                    """)
                     

                    # contents
                    main_body = browser.find_element(By.TAG_NAME, 'main')
                    article = main_body.find_element(By.TAG_NAME, 'article')
                    contents =  [element.text for element in article.find_elements(By.TAG_NAME, 'p')]
                    content = " ".join(contents)
                    print(content)

                    # images
                    images = [element.get_attribute('src') for element in article.find_elements(By.CLASS_NAME, 'dcr-evn1e9')]
                    images = [f"{src.split('?')[0]}?width=1920&dpr=1&s=none" for src in images if src is not None]
                    if images.__len__() == 1:
                        images.append(images[0])
                    print(images)

                    # create folder to save files to edit video
                    count_folder = count_folders('./videos')
                    path_folder = f'./videos/video-{count_folder}'
                    try:
                        os.makedirs(path_folder)
                    except:
                        print('folder existed')
                    


                    # random number to get image and gif
                    index_path = random.randint(0, 3)
                    gif_path = gif_paths[index_path]
                    person_img_path = person_img_paths[index_path]

                    #import images
                    path_videos = []
                    def process_image_and_video(item, key, path_folder):
                        img_path = f"{path_folder}/image-{key}.jpg"
                        img_blur_path = f"{path_folder}/image-blur-{key}.jpg"
                        generate_image(item, img_path, img_blur_path)
                        random_number = random.randint(5, 10)
                        generate_video_by_image(
                            1 if key % 2 == 0 else None,
                            img_path,
                            img_blur_path,
                            f'{path_folder}/video-{key}.mp4',
                            random_number,
                            gif_path
                        )
                        return f"{path_folder}/video-{key}.mp4"
                    
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        futures = []
                        for key, item in enumerate(images):
                            futures.append(
                                executor.submit(process_image_and_video, item, key, path_folder)
                            )
                        
                        path_videos = [future.result() for future in concurrent.futures.as_completed(futures)]

                    # generate title by ai
                    print('generate title')
                    title = generate_content(f'hãy đặt lại title youtube cho tôi bằng tiếng anh không quá 100 ký tự: {title}, trả ra title cho tôi luôn, không cần phải ghi thêm gì hết.')
                    if len(title) > 100:
                        title = title[:100]
                    print('nguyen quang hpang')
                    print(title)
                    title_slug = slugify(str(title))
                    title_youtube = f'{title}'
                    print('huy')
                    # generate content by ai
                    print(f'generate content {content.__len__()}')

                    content = generate_content(f'hãy viết lại đoạn văn sau bằng tiếng anh và có độ dài ký tự là {content.__len__()}: {content}')
                    print(content)
                
                    # generate tags
                    print(f'generate tags')
                    tags = generate_content(f'hãy gợi ý 15 tags (không phải hastag nha, không ghi dính liền với nhau, không cần sắp xếp theo số thứ tự, không có dấu #, tổng các tags không quá 290 ký tự, đồng thời các tag ngăn cách nhau bởi dấu phẩy như vầy tag1, tag2, tag3, ....) quan trọng để tui gắn vào video dài trên youtube để có nhiều người search. title của video là {title}, content là {content}')
                    description = generate_content(f'hãy tóm tắt lại đoạn văn sau bao gồm các ý quan trọng bằng tiếng anh để gắn vào phần mô tả youtube để seo, và có độ dài không quá 600 ký tự: {content}')
                    # Chuyển chuỗi thành list các tag
                    tag_list = tags.split(', ')
                    result = ""
                    length = 0

                    for tag in tag_list:
                        if length + len(tag) + 2 <= 300:  
                            result += tag + ", "
                            length += len(tag) + 2
                        else:
                            break

                    if result.endswith(", "):
                        result = result[:-2]

                    # generate thumbnail by ai
                    print('generate thumbnail')
                    generate_thumbnail(
                        f"{path_folder}/image-0.jpg",
                        f"{path_folder}/image-blur-0.jpg",
                        person_img_path,
                        f"{path_folder}/thumbnail.jpg",
                        title.replace('*', '')
                    )

                    # save content to file txt
                    print('write result txt')
                    with open(f"{path_folder}/result.txt", "w",  encoding="utf-8") as file:
                        # Viết vào file
                        file.write(f"link: {current_link}.\n")
                        file.write(f"title: {title}\n")
                        file.write(f"title slug: {title_slug}\n")
                        file.write(f"content: {content}\n")
                        file.write(f"tags: {result}\n")

                    # generate voice ---------------------------------------
                    print('generate voice-----------------')
                    is_generate_voice_success = generate_voice_kokoro(content, f"{path_folder}/content-voice.mp3")

                    if not is_generate_voice_success:
                        print('generate voice error ....')
                        music = pyglet.resource.media('public/reng.weba', streaming=False)
                        player = pyglet.media.Player()
                        player.queue(music)
                        player.loop = True
                        player.play()
                        pyglet.app.run()


                        is_generate_voice_error = True
                        browser.quit()
                        subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], check=True)
                        print('time hien tai')
                        print(datetime.now())
                        break
                        
                
                    # concact content video ---------------------------------------
                    concact_content_videos(f"{path_folder}/content-voice.mp3",path_videos, f'{path_folder}/{title_slug}.mp4' )

                    insert_link(current_link)
                    browser.quit()
                    
                    print('upload video to youtube')
                    des_youtube = f"{title}\n{description}\n\n(tags):\n{result}"
                    upload_yt(
                        "C:/Program Files/Google/Chrome/Application/chrome.exe",
                        "C:/Path/To/Chrome/news-us",
                        title_youtube,
                        des_youtube,
                        f'{result},',
                        os.path.abspath(f'{path_folder}/{title_slug}.mp4'),
                        os.path.abspath(f"{path_folder}/thumbnail.jpg"),
                    )
                    print('upload video to youtube successfully')
                    
                    time.sleep(60)
                else:
                    insert_link(current_link)
                    browser.quit()
                    time.sleep(10)
            # không có current link ----------------------------------------------
            else:
                print('không có tin tức mời, chờ 5 phút')
                browser.quit()
                time.sleep(60)
        
    except Exception as e:
        print('Error')
        print(e)
        print(NameError)
        dir_path = Path(f'{path_folder}/result.txt')
        if not dir_path.is_file() and not is_generate_voice_error:
            insert_link(current_link)
        subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], check=True)