from untils import get_all_link_in_theguardian_new
from untils import get_info_new, generate_image_and_video_aff_and_get_three_item
from untils import upload_rumble, import_audio_to_video, upload_yt
from untils import get_img_gif_person, concat_content_videos
from untils import generate_image, generate_to_voice_edge
from untils import generate_video_by_image, generate_thumbnail, create_shortened_link
from untils import generate_title_description_improved, generate_content_improved
from db import check_link_exists, connect_db, insert_link, get_all_links, delete_link
from concurrent.futures import ProcessPoolExecutor, wait
import random
from slugify import slugify
import os
import time
import shutil
from moviepy import AudioFileClip
import subprocess

# print(get_all_links())
# delete_link('https://www.theguardian.com//politics/2025/jun/25/class-age-education-dividing-lines-uk-politics-electoral-reform')
# delete_link('https://www.theguardian.com//us-news/2025/jun/24/new-york-mayoral-primary-results')
# chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
# user_data_dir = r"C:/Path/To/Chrome/news-us-news"
# subprocess.Popen([chrome_path, f'--user-data-dir={user_data_dir}'])
# time.sleep(510000)

# delete_link('https://www.theguardian.com//politics/2025/jun/25/keir-starmer-dismisses-labour-welfare-cuts-rebellion-as-noises-off')
# connect_db()
# delete_link('https://www.theguardian.com//business/2025/jun/25/asda-owner-near-600m-loss-as-sales-fall')
# delete_link('https://www.theguardian.com//australia-news/2025/jun/26/nsw-coalition-proposes-cuts-to-crippling-fees-on-housing-construction-in-budget-reply')
# delete_link('https://www.theguardian.com//tv-and-radio/2025/jun/26/everyone-was-completely-caught-off-guard-fbi-radios-future-unclear-as-station-launches-emergency-fundraising-campaign')
# print(get_all_links())
# time.sleep(510000)
# # insert_link('https://www.theguardian.com/world/2025/feb/19/british-journalist-charlotte-peet-missing-in-brazil-for-more-than-10-days')


# insert_link('https://www.theguardian.com//environment/2025/jun/20/nigerian-communities-shell-high-court-oil-pollution')
# print('gg')
# is_generate_voice_success = generate_voice_google(
#     'right right right right right right right right right',
#     f"./content-voice.mp3",
#     'https://cxl-services.appspot.com/proxy?url=https://texttospeech.googleapis.com/v1beta1/text:synthesize&token=03AFcWeA5YAQQSWUWISJMznKTgL0dUS-l95FswY4AQpcbpoBQ3ki4yeBM5pX2We3xeB-e9n4g9fz51c9gZNECvOdzgSAdsHdeIj2eKLmcyarojcxRvqqH28gU-NkH76bXgmPCG4RQz-d1zxzoaXerd3YXj1Fflh6c8MsP4ccBXfD9V13UA2ZrRTvJgWBQVqVlAYYfZmZSe-EBhuZGcDzun4VzaGFgJHdONtI7gK-iPaWBFpMuudnvAet1vTIGk_1-Qm1gs7pOW853--sBF-aCj0QtBbJBXgWx1wiQPo1N2bhTlAsbjeg9Iqdz-2gjEh0cLRwCgO_tE28GOc9vr6BSanb5l-I3IEYcyo6qIXaf2Pi6iwHJsX5bT61lFhVGdHsKJGTm0Cxn9mcxqlUHLYBUlQFlpt8Wb819qnEYy-ef_ppvWRsXMFv16hAUCuWDAn9XeagL794b4j0XdSnxsHra61AF_b_mREr0yuJQAN1AGh-EDe8rEovNLwQezFq90_OLeR2978ysiV61UBm9RXl4L0TvfwlZCXO18soAFo6gGJNL05rW_UPlJ1rinkjbNZKc4AHzr4my-xGBkBCfBZ2H2SQ6mxZaxAhSqlicWjMMg2n7GfllqeC-rJoBmBBli3h9ceu78eyE22umVqEMBPbJDaycyRv2b2LuXhLuXr4huo1b7T0hPWwrmATjya9EKoRW1Cqc9WJhMUoQCbmsw2t4yQ7TtC8TEUREDMgkyecW6R-i8smhRK6EkNHsSq1zlJcGmj_GFBZZjp7Nv3hQNS8Li0KnXUc8deIjJLRg9TSi6ew1AMMP7zbKFFz670oyp8mwiaOMboCVYoCgCaMKPOTyoTEpzMYJ9Br5irPKuNJZCMTcqeOmPv41KVmFaKwoLWjibhb2XaeeA0p1N'
# )
# time.sleep(10000)


def main():
    while True:
        current_link = None
        try:
            # tạo folder để chứa video
            path_folder = f'./videos'
            try:
                shutil.rmtree(path_folder)
            except:
                print('next')
            
            os.makedirs(path_folder)

            # lấy tất cả link tin tức
            link_news = get_all_link_in_theguardian_new()

            # kết nối db và kiểm tra có link tồn tại chưa, chưa thì lấy và làm video
            connect_db()
            for link in link_news:
                if not check_link_exists(f'https://www.theguardian.com/{link}'):
                    current_link = link
                    break
                
            # nếu không có link thì bắn lỗi
            if (current_link is None):
                raise Exception("Lỗi xảy ra, không tồn tại link hoặc đã hết tin tức")

            current_link = f'https://www.theguardian.com/{current_link}'

            # lấy thông tin của video
            new_info = get_info_new(current_link)

            # nếu không có thông tin tin tức thì bắn lỗi
            if (current_link is None):
                raise Exception("Lỗi xảy ra, không có link")

            # lấy ngẫu nhiên đường dẫn hình ảnh và hình động người thuyết trình
            person_info = get_img_gif_person()

            # tạo ra image gốc và image mờ, sau đó tạo ra video từng phần
            path_videos = []
            print(current_link)
            if(new_info is None):
                raise Exception("Lỗi xảy ra, không có thông tin của content")
            for key, item in enumerate(new_info['picture_links']):
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
                    person_info['person_gif_path']
                )
                path_videos.append(f"{path_folder}/video-{key}.mp4")

            # # tạo video kêu gọi người dùng nhấn vào link short kiếm tiền
            # generate_video_by_image(None,
            #                         './public/bg/short-link.png',
            #                         './public/bg/short-link.png',
            #                         f'{path_folder}/short-link.mp4',
            #                         AudioFileClip('./public/short-link.aac').duration + 1,
            #                         person_info['person_gif_path']
            #                     )
            # import_audio_to_video(f'{path_folder}/short-link.mp4',
            #                     f'{path_folder}/short-link-2.mp4',
            #                     AudioFileClip('./public/short-link.aac').duration + 1,
            #                     './public/short-link.aac'
            #                     )

            # products = generate_image_and_video_aff_and_get_three_item(person_info['person_gif_path'])
            # if(products is None):
            #     raise Exception("Lỗi xảy ra, không thể tạo và lấy ra 3 product ngẫu nhiên")
            # nswf
            import_audio_to_video(f'./public/nsfw/nsfw.mp4',
                f'{path_folder}/nsfw.mp4',
                AudioFileClip('./public/nsfw/nsfw.aac').duration + 1,
                './public/nsfw/nsfw.aac'
            )

            # chuyển đổi title và description lại, tạo mới lại content
            with ProcessPoolExecutor() as executor:
                future1 = executor.submit(generate_title_description_improved, new_info['title'], new_info['description'])
                future2 = executor.submit(generate_content_improved, new_info['content'], new_info['title'])

                wait([future1, future2])

                result1 = future1.result()
                result2 = future2.result()

                # Gán lại kết quả vào new_info
                new_info['title'] = result1['title']
                new_info['description'] = result1['description']
                new_info['content'] = result2
                new_info['title_slug'] = slugify(new_info['title'])

            print(new_info)
            # tạo thumbnail video
            generate_thumbnail(
                f"{path_folder}/image-0.jpg",
                f"{path_folder}/image-blur-0.jpg",
                person_info['person_img_path'],
                f"{path_folder}/draf-thumbnail.jpg",
                f"{path_folder}/thumbnail.jpg",
                new_info['title'].replace('*', '')
            )

            # # save content to file txt
            # with open(f"{path_folder}/result.txt", "w",  encoding="utf-8") as file:
            #     # Viết vào file
            #     file.write(f"link: {current_link}.\n")
            #     file.write(f"title: {new_info['title']}\n")
            #     file.write(f"title slug: {new_info['title_slug']}\n")
            #     file.write(f"content: {new_info['content']}\n")
            #     file.write(f"tags: {new_info['tags']}\n")

            # tạo âm thanh video
            print('generate voice-----------------')
            generate_to_voice_edge(new_info['content'], f"{path_folder}/content-voice.mp3")

            # concact content video ---------------------------------------
            # concat_content_videos(
            #     './public/intro_ffmpeg.mp4',
            #     f'./pic_affs/aff.mp4',
            #     f"{path_folder}/content-voice.mp3",
            #     f"{path_folder}/content-voice.aac",
            #     path_videos,
            #     f'{path_folder}/{new_info['title_slug']}.mp4',
            #     f'{path_folder}/draf.mp4',
            #     f'{path_folder}/draf2.mp4',
            # )
            concat_content_videos(
                './public/intro_ffmpeg.mp4',
                f'{path_folder}/nsfw.mp4',
                f"{path_folder}/content-voice.mp3",
                f"{path_folder}/content-voice.aac",
                path_videos,
                f'{path_folder}/{new_info['title_slug']}.mp4',
                f'{path_folder}/draf.mp4',
                f'{path_folder}/draf2.mp4',
            )


            # tạo link rút gọn
            # short_link = create_shortened_link(current_link)
            # if short_link is None:
            #     raise Exception("Lỗi xảy ra, không thể tạo link rút gọn")
         
            # aff_text = ''
            # for item in products:
            #     aff_text += f'{item['itemDes']}: {item['exeLink']}\n'

            # des_youtube = f"{new_info['description']}\n\n💡 Support us by using the short links below — just a few seconds of ads before the awesome deals!:\n{aff_text}\n\n(tags):\n{', '.join(new_info['tags'].split(','))}"
            des_youtube = f"{new_info['description']}\n\nJoin my Patreon to discover unique artworks that I don't share publicly. For just $1, you'll get access to exclusive sketches and special pieces!\n👉 https://www.patreon.com/LenaStudio\n\n(tags):\n{', '.join(new_info['tags'].split(','))}"
            
            upload_yt(
                "C:/Path/To/Chrome/news-us-news",
                new_info['title'],
                des_youtube,
                f'news,{new_info['tags']},breaking news,current events,',
                os.path.abspath(f'{path_folder}/{new_info['title_slug']}.mp4'),
                os.path.abspath(f"{path_folder}/thumbnail.jpg"),
            )
            # upload_rumble(
            #     "C:/Path/To/Chrome/news-us-news",
            #     new_info['title'],
            #     des_youtube,
            #     f'news, {', '.join(new_info['tags'].split(','))}, breaking news, current events',
            #     os.path.abspath(f'{path_folder}/{new_info['title_slug']}.mp4'),
            #     os.path.abspath(f"{path_folder}/thumbnail.jpg"),
            # )

            
            print('upload video to youtube successfully')
            insert_link(current_link)
            print(new_info)
            time.sleep(60 * 20)     
        except Exception as e:
            print(current_link)
            print(f'loi xay ra: {e}')
            if current_link is not None:
                insert_link(current_link)
            else:
                time.sleep(60 * 20)


if __name__ == "__main__":
    main()
