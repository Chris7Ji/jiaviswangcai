#!/usr/bin/env python3
import shutil
import os

src_dir = '/Users/jiyingguo/.openclaw/media/tool-image-generation'
dst_dir = '/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai/images/preview'

os.makedirs(dst_dir, exist_ok=True)

files = [
    'wangcai_jarvis_hd_v4---640612d8-46b8-4ea0-903a-973fa5432017.png',
    'wangcai_jarvis_hd_v4---748acdcf-9523-448a-8895-668d4c4ca27c.png',
    'wangcai_jarvis_hd_v4---fbaeb085-0db8-48c9-84c5-2250a4ac855e.png',
    'wangcai_jarvis_hd_v4---cba05629-3c2c-4b37-bae0-1e69cef3e553.png'
]

for i, f in enumerate(files, 1):
    src = os.path.join(src_dir, f)
    dst = os.path.join(dst_dir, f'logo_hd_option_{i}.png')
    shutil.copy(src, dst)
    print(f'Copied option {i}')

print('All done!')
