from untils import generate_to_voice_edge, normalize_audio, import_audio_to_video, normalize_video
from moviepy import AudioFileClip
print('hhhh')
# generate_to_voice_edge("If you're a fan of bold and expressive art, come check out my Patreon! For just $1, you’ll get exclusive access to artwork that I don’t share anywhere else, Click the link in the video description to dive into my daring creations and unique artistic style!", './public/nsfw.mp3', rate='+15%')
# normalize_audio('./public/nsfw/nsfw.mp3', './public/nsfw/nsfw.aac')
import_audio_to_video(f'./public/nsfw/nsfw.mp4',
        f'./nsfw.mp4',
        AudioFileClip('./public/nsfw/nsfw.aac').duration + 1,
        './public/nsfw/nsfw.aac'
        )