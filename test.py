from untils import create_video_support, process_image_support
import random
from data import data_support


support_randoom = random.sample(data_support, 3)
link_support_images = [item['link_img'] for item in support_randoom]
content_supports = "\n".join([item['content'] for item in support_randoom])

for index, item in enumerate(link_support_images):
    print(item)
    process_image_support(item, f'./t{index}.png')


# create_video_support(
#     './public/support.mp3',
#     './public/bg/support.png',
#     './public/gifs/gif_1.gif',
#     './public/support.mp4',
#     link_support_images,
#     ['./public/support_1.png', './public/support_2.png', './public/support_3.png']
# )

# print(content_supports)