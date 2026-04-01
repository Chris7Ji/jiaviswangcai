#!/usr/bin/env python3
import shutil
import os

src_dir = '/Users/jiyingguo/.openclaw/workspace'
dst_dir = '/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai/images/preview'

os.makedirs(dst_dir, exist_ok=True)

for i in range(1, 5):
    src = os.path.join(src_dir, f'logo_option_{i}.png')
    dst = os.path.join(dst_dir, f'logo_option_{i}.png')
    shutil.copy(src, dst)
    print(f'Copied {src} to {dst}')

print('All done!')
