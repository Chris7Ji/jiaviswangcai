#!/bin/bash
# 旺财Jarvis LOGO 生成脚本
# 用法: bash gen_logo.sh

SCRIPT_DIR="/Users/jiyingguo/.openclaw/workspace/skills/nano-banana-pro/scripts"
OUTPUT_DIR="/Users/jiyingguo/.openclaw/workspace"

cd "$OUTPUT_DIR" || exit 1

uv run "$SCRIPT_DIR/generate_image.py" \
    --prompt "A cute cartoon mascot logo for 旺财Jarvis - an AI assistant combining a lucky golden dog with a sophisticated robot AI butler. Design: fluffy golden fur with cute pointed ears, bright glowing cyan/blue LED eyes (like Jarvis from Iron Man), wears elegant black bow tie with gold pattern, has circuit board texture on body, golden coin pendant necklace, holographic AR glasses, holds golden staff/scepter with gem on top. Color palette: rich gold (#FFD700) and orange (#FF8C00) mixed with deep blue (#1E90FF) and cyan. Pixar-Disney style, adorable yet sophisticated, clean vector logo aesthetic, square composition, centered." \
    --filename "wangcai_jarvis_logo.png" \
    --resolution 2K \
    --api-key "AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s"
