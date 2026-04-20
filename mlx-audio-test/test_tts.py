from mlx_audio.tts.utils import load_model
import numpy as np
import wave
import struct

print("正在加载 Kokoro 模型...")
model = load_model("mlx-community/Kokoro-82M-bf16")

print("正在生成语音...")
# 遍历生成器直到获取音频数组
audio_array = None
for result in model.generate(
    text="你好，老板。我是旺财Jarvis，现在正在尝试本地化的MLX音频模型。",
    voice="zf_xiaobei",
    speed=1.0,
    lang_code="z"
):
    audio_array = result.audio
    print(f"语音生成完毕，数组形状: {audio_array.shape}")

if audio_array is not None:
    # 将 mlx.core.array 转换为 numpy 数组
    import mlx.core as mx
    audio_np = np.array(audio_array).astype(np.float32)
    
    # 归一化并转换为 16-bit PCM
    audio_int16 = (audio_np * 32767).astype(np.int16)
    
    # 保存为 WAV 文件
    with wave.open("test_output.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000) # Kokoro 通常是 24kHz
        wf.writeframes(audio_int16.tobytes())
    print("已保存到 test_output.wav")
else:
    print("未能生成音频")
