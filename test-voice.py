from untils import create_video_support
import random
from data import data_support
import os

support_randoom = random.sample(data_support, 3)
link_support_images = [item['link_img'] for item in support_randoom]
list_discount = [item['discount'] for item in support_randoom]
content_supports = "\n".join([item['content'] for item in support_randoom])

# tạo video kêu gọi kiếm tiền
create_video_support(
    './public/support.mp3',
    './public/bg/support.png',
    './public/gifs/gif_1.gif',
    './public/support.mp4',
    link_support_images,
    ['./public/support_1.png', './public/support_2.png', './public/support_3.png'],
    list_discount
)