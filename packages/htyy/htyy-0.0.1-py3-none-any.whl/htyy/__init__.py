"""
 htyy
~~~~~~
Version: 0.0.1
"""

from . import sendweb
from . import client
from . import reponse
from . import extensions
from . import request
from . import version
from . import message
from . import _path

__version__ = version.__version__

import miniaudio
import pyaudio
import threading
import time
import numpy as np

class Music:
    def __init__(self, file_path, play_time=-1):
        self.file_path = file_path
        self.play_time = play_time
        self._running = False
        self.audio_thread = None
        self._load_audio()  # 加载音频
        self.play()

    def _load_audio(self):
        """使用 miniaudio 加载音频"""
        try:
            # 解码音频文件（默认输出为 16 位整数）
            decoded = miniaudio.decode_file(self.file_path)
            self.sample_rate = decoded.sample_rate
            self.channels = decoded.nchannels
            # 将数据转换为 numpy 数组（int16）
            self.audio_data = np.frombuffer(decoded.samples, dtype=np.int16)
        except Exception as e:
            raise ValueError(f"加载音频失败：{e}")

    def _play_audio(self):
        """核心播放逻辑"""
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,  # 指定 16 位整数格式
            channels=self.channels,
            rate=self.sample_rate,
            output=True
        )

        self._running = True
        start_time = time.time()
        pos = 0
        chunk_size = 1024  # 每次写入的帧数

        while self._running and pos < len(self.audio_data):
            if self.play_time > 0 and (time.time() - start_time) >= self.play_time:
                break

            end_pos = pos + chunk_size * self.channels  # 注意：每个帧包含多个通道的数据
            chunk = self.audio_data[pos:end_pos]
            stream.write(chunk.tobytes())
            pos = end_pos

        stream.stop_stream()
        stream.close()
        p.terminate()

    def play(self):
        if not self._running:
            self.audio_thread = threading.Thread(target=self._play_audio)
            self.audio_thread.start()

    def stop(self):
        self._running = False
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join()

# video_conversion.py （模块主文件）
import os
import subprocess
import sys
import logging
from pathlib import Path

class VideoConversionError(Exception):
    """Custom conversion exceptions."""
    pass

class VideoConversion:
    _CODEC_MAP = {
        "wav": "pcm_s16le",
        "mp3": "libmp3lame",
        "aac": "aac",
        "flac": "flac",
        "ogg": "libvorbis"
    }

    def __init__(self, input_path: str, output_path: str):
        """
        初始化转换器
        :param input_path: 输入视频文件路径
        :param output_path: 输出音频文件路径
        """
        self.input_path = Path(input_path).resolve()
        self.output_path = Path(output_path).resolve()
        self.ffmpeg_path = self._find_ffmpeg()

        self._validate_paths()
        logging.basicConfig(level=logging.INFO)
        self.convert()

    @classmethod
    def _find_ffmpeg(cls) -> Path:
        """定位项目内的 FFmpeg 可执行文件"""
        # 获取模块所在目录的绝对路径
        module_dir = Path(__file__).parent.resolve()
        
        # 预期路径结构: 模块目录/bin/ffmpeg-版本号-essentials_build/bin/ffmpeg.exe
        ffmpeg_path = (
            module_dir / "bin" / "ffmpeg-7.0.2-essentials_build" / "bin" / "ffmpeg.exe"
        )

        if not ffmpeg_path.exists():
            raise VideoConversionError(
                f"FFmpeg 未找到于预期路径: {ffmpeg_path}\n"
                "请确认已正确放置 FFmpeg 文件结构"
            )
        return ffmpeg_path

    def _validate_paths(self):
        """路径验证"""
        if not self.input_path.exists():
            raise FileNotFoundError(f"输入文件不存在: {self.input_path}")

        output_dir = self.output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        if not os.access(str(output_dir), os.W_OK):
            raise PermissionError(f"无写入权限: {output_dir}")

    def _get_codec(self) -> str:
        """获取编解码器"""
        ext = self.output_path.suffix.lower()[1:]
        codec = self._CODEC_MAP.get(ext)
        if not codec:
            raise ValueError(f"不支持的输出格式: .{ext}")
        return codec

    def convert(self):
        """执行转换操作"""
        cmd = [
            str(self.ffmpeg_path),
            "-y",  # 覆盖输出文件
            "-i", str(self.input_path),
            "-vn",  # 忽略视频流
            "-acodec", self._get_codec(),
            "-loglevel", "error",  # 仅显示错误信息
            str(self.output_path)
        ]

        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logging.info(f"The conversion was successful: {self.output_path}")
        except subprocess.CalledProcessError as e:
            error_msg = f"FFmpeg Error: {e.stderr.strip()}"
            logging.error(error_msg)
            raise VideoConversionError(error_msg)
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise

class MusicConversionError(Exception):
    """自定义音频转换异常"""
    pass

class MusicConversion:
    _CODEC_MAP = {
        "wav": "pcm_s16le",
        "mp3": "libmp3lame",
        "aac": "aac",
        "flac": "flac",
        "ogg": "libvorbis",
        "m4a": "aac"
    }

    def __init__(self, input_path: str, output_path: str, progress_callback=None):
        """
        初始化音频转换器
        :param input_path: 输入音频文件路径（如 "D:/input.mp3"）
        :param output_path: 输出音频文件路径（如 "D:/output.wav"）
        :param progress_callback: 可选进度回调函数（示例：lambda pct: print(f"进度: {pct}%")）
        """
        self.input_path = Path(input_path).resolve()
        self.output_path = Path(output_path).resolve()
        self.ffmpeg_path = self._find_ffmpeg()
        self._validate_paths()
        logging.basicConfig(level=logging.INFO)
        self.convert(progress_callback)

    @classmethod
    def _find_ffmpeg(cls) -> Path:
        """定位项目内的 FFmpeg 可执行文件"""
        # 模块目录 -> bin/ffmpeg-版本号-essentials_build/bin/ffmpeg.exe
        module_dir = Path(__file__).parent.resolve()
        ffmpeg_path = (
            module_dir / "bin" / "ffmpeg-7.0.2-essentials_build" / "bin" / "ffmpeg.exe"
        )
        if not ffmpeg_path.exists():
            raise MusicConversionError(f"FFmpeg 未找到于: {ffmpeg_path}")
        return ffmpeg_path

    def _validate_paths(self):
        """路径验证"""
        if not self.input_path.exists():
            raise FileNotFoundError(f"输入文件不存在: {self.input_path}")
        if not self.input_path.suffix.lower()[1:] in self._CODEC_MAP:
            raise ValueError(f"不支持的输入格式: {self.input_path.suffix}")
        output_dir = self.output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        if not os.access(str(output_dir), os.W_OK):
            raise PermissionError(f"无写入权限: {output_dir}")

    def _get_codec_params(self) -> list:
        """获取编解码参数"""
        out_ext = self.output_path.suffix.lower()[1:]
        codec = self._CODEC_MAP.get(out_ext)
        if not codec:
            raise ValueError(f"不支持的输出格式: .{out_ext}")

        params = ["-acodec", codec]
        
        # 格式特定参数（示例：MP3 的比特率设置）
        if out_ext == "mp3":
            params += ["-b:a", "320k"]  # 默认 320kbps 高音质
        elif out_ext == "wav":
            params += ["-ar", "44100"]  # 默认 44.1kHz 采样率
        
        return params

    def convert(self, progress_callback=None):
        """
        执行音频格式转换
        :param progress_callback: 可选进度回调函数（示例：lambda pct: print(f"进度: {pct}%")）
        """
        cmd = [
            str(self.ffmpeg_path),
            "-y",  # 覆盖输出文件
            "-i", str(self.input_path),
            "-hide_banner",  # 隐藏冗余信息
            "-loglevel", "error",
            *self._get_codec_params(),
            str(self.output_path)
        ]

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding="utf-8",
                errors="replace"
            )

            # 实时进度处理（简化示例）
            duration = None
            for line in process.stdout:
                if "Duration" in line:
                    # 提取总时长（示例：Duration: 00:03:25.04）
                    time_str = line.split("Duration: ")[1].split(",")[0].strip()
                    h, m, s = time_str.split(":")
                    duration = int(h)*3600 + int(m)*60 + float(s)
                elif "time=" in line and duration:
                    # 提取当前时间（示例：time=00:01:23.45）
                    time_str = line.split("time=")[1].split(" ")[0].strip()
                    h, m, s = time_str.split(":")
                    current = int(h)*3600 + int(m)*60 + float(s)
                    if progress_callback and duration > 0:
                        progress_callback(round(current / duration * 100, 1))

            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd)
            
            logging.info(f"The conversion was successful: {self.output_path}")

        except subprocess.CalledProcessError as e:
            raise MusicConversionError(f"FFmpeg Error: {str(e)}")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise

from PIL import Image

class ImageConversionError(Exception):
    """自定义图像转换异常"""
    pass

class ImageConversion:
    SUPPORTED_FORMATS = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "bmp": "BMP",
        "webp": "WEBP",
        "gif": "GIF",
        "tiff": "TIFF"
    }

    def __init__(self, input_path: str, output_path: str, **kwargs):
        """
        初始化图像转换器
        :param input_path:  输入图像路径（如 "D:/input.jpg"）
        :param output_path: 输出图像路径（如 "D:/output.png"）
        :param kwargs:      可选参数（如 quality=85, optimize=True）
        """
        self.input_path = Path(input_path).resolve()
        self.output_path = Path(output_path).resolve()
        self.convert_params = kwargs  # 转换参数（如质量、优化选项）
        self._validate_paths()
        logging.basicConfig(level=logging.INFO)

    def _validate_paths(self):
        """验证输入输出路径合法性"""
        # 输入文件检查
        if not self.input_path.exists():
            raise FileNotFoundError(f"输入文件不存在: {self.input_path}")
        
        # 输入格式支持性检查
        input_ext = self.input_path.suffix.lower()[1:]
        if input_ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"不支持的输入格式: .{input_ext}")

        # 输出目录写入权限检查
        output_dir = self.output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        if not os.access(str(output_dir), os.W_OK):
            raise PermissionError(f"无写入权限: {output_dir}")

        # 输出格式支持性检查
        output_ext = self.output_path.suffix.lower()[1:]
        if output_ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"不支持的输出格式: .{output_ext}")

    def _get_save_params(self) -> dict:
        """根据输出格式生成保存参数"""
        output_ext = self.output_path.suffix.lower()[1:]
        params = self.convert_params.copy()

        # 格式特定参数（示例：JPEG 质量、PNG 压缩）
        if output_ext in ["jpg", "jpeg"]:
            params.setdefault("quality", 90)  # 默认 JPEG 质量 90%
        elif output_ext == "webp":
            params.setdefault("quality", 80)  # 默认 WEBP 质量 80%
        elif output_ext == "png":
            params.setdefault("compress_level", 6)  # PNG 压缩级别

        return params

    def convert(self):
        """执行图像格式转换"""
        try:
            # 打开输入图像
            with Image.open(self.input_path) as img:
                # 转换 RGBA 格式处理（如 PNG 转 JPEG 需移除透明度）
                if img.mode in ("RGBA", "LA") and self.output_path.suffix.lower() in [".jpg", ".jpeg"]:
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])  # 移除透明度
                    img = background

                # 保存为输出格式
                img.save(
                    self.output_path,
                    format=self.SUPPORTED_FORMATS[self.output_path.suffix.lower()[1:]],
                    **self._get_save_params()
                )
            
            logging.info(f"The conversion was successful: {self.output_path}")

        except IOError as e:
            error_msg = f"Image processing failed: {str(e)}"
            logging.error(error_msg)
            raise ImageConversionError(error_msg)
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise

"""
if __name__ == "__main__":
    try:
        converter = VideoConversion(
            input_path="D:/test_video.mp4",
            output_path="D:/output/test_audio.wav"
        )
        converter.convert()
    except Exception as e:
        print(f"转换失败: {str(e)}")
        sys.exit(1)
"""

path = _path
htyy = __file__

if __name__ == "__main__":
    message.showinfo("Title","Message\nmsg")
    response = request.get('https://codinghou.cn', timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text[:200]}...")
    if not path.exists("PATH"):
        pass

    else:
        print(htyy)

    if path.name.startswith("win32"):
        pass

    else:
        print(htyy)