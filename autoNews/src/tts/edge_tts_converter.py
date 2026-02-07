"""
Edge TTS Converter - 使用微软Edge TTS将文本转换为语音
完全免费，无需API Key，音质优秀
"""

import asyncio
import edge_tts
from pathlib import Path
from typing import List, Optional
from src.utils.logger import get_logger

logger = get_logger()


class EdgeTTSConverter:
    """使用Edge TTS将文本转换为音频"""

    # 可用的中文语音（更多选项可通过 edge-tts --list-voices 查看）
    CHINESE_VOICES = {
        # 普通话
        'xiaoxiao': 'zh-CN-XiaoxiaoNeural',      # 女声，温柔
        'yunxi': 'zh-CN-YunxiNeural',            # 男声，沉稳
        'yunyang': 'zh-CN-YunyangNeural',        # 男声，新闻播报
        'xiaoyou': 'zh-CN-XiaoyouNeural',        # 女童，活泼
        'xiaomo': 'zh-CN-XiaomoNeural',          # 女声，甜美
        'xiaochen': 'zh-CN-XiaochenNeural',      # 女声，温和
        'yunhao': 'zh-CN-YunhaoNeural',          # 男声，阳光

        # 其他方言
        'hiugaai': 'zh-HK-HiuGaaiNeural',        # 粤语女声
        'wanlung': 'zh-HK-WanLungNeural',        # 粤语男声
        'hsiaocheng': 'zh-TW-HsiaoChenNeural',   # 台湾女声
        'yunjian': 'zh-TW-YunJianNeural',        # 台湾男声
    }

    def __init__(
        self,
        voice: str = 'xiaoxiao',
        rate: str = '+0%',      # 语速：-50%到+100%
        volume: str = '+0%',    # 音量：-50%到+100%
        pitch: str = '+0Hz'     # 音调：-50Hz到+50Hz
    ):
        """
        初始化TTS转换器

        Args:
            voice: 语音名称，可选值见CHINESE_VOICES
            rate: 语速调整，如 '+20%' 表示加快20%
            volume: 音量调整
            pitch: 音调调整
        """
        # 获取完整的语音ID
        if voice in self.CHINESE_VOICES:
            self.voice = self.CHINESE_VOICES[voice]
        else:
            logger.warning(f"Unknown voice '{voice}', using default 'xiaoxiao'")
            self.voice = self.CHINESE_VOICES['xiaoxiao']

        self.rate = rate
        self.volume = volume
        self.pitch = pitch

        logger.info(f"EdgeTTS initialized with voice: {self.voice}")

    async def convert_text_to_speech(
        self,
        text: str,
        output_file: str
    ) -> bool:
        """
        将文本转换为语音

        Args:
            text: 要转换的文本
            output_file: 输出音频文件路径（.mp3）

        Returns:
            是否成功
        """
        try:
            # 创建输出目录
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # 创建TTS通信对象
            communicate = edge_tts.Communicate(
                text,
                self.voice,
                rate=self.rate,
                volume=self.volume,
                pitch=self.pitch
            )

            # 保存音频
            await communicate.save(str(output_path))

            logger.info(f"Audio saved to: {output_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to convert text to speech: {e}")
            return False

    def convert_sync(self, text: str, output_file: str) -> bool:
        """
        同步版本的转换方法（方便调用）

        Args:
            text: 要转换的文本
            output_file: 输出音频文件路径

        Returns:
            是否成功
        """
        return asyncio.run(self.convert_text_to_speech(text, output_file))

    async def convert_multiple(
        self,
        text_list: List[tuple],
        output_dir: str
    ) -> int:
        """
        批量转换多个文本

        Args:
            text_list: [(文本, 文件名), ...] 列表
            output_dir: 输出目录

        Returns:
            成功转换的数量
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        success_count = 0

        for text, filename in text_list:
            output_file = output_path / filename
            if await self.convert_text_to_speech(text, str(output_file)):
                success_count += 1

        logger.info(f"Converted {success_count}/{len(text_list)} files")
        return success_count

    @staticmethod
    async def list_voices():
        """列出所有可用的语音"""
        voices = await edge_tts.list_voices()
        return voices

    @staticmethod
    def list_chinese_voices():
        """列出所有中文语音选项"""
        print("\n可用的中文语音:")
        print("-" * 60)
        for key, value in EdgeTTSConverter.CHINESE_VOICES.items():
            print(f"  {key:15} -> {value}")
        print("-" * 60)


# 便捷函数
def text_to_speech(
    text: str,
    output_file: str,
    voice: str = 'xiaoxiao',
    rate: str = '+0%'
) -> bool:
    """
    快速将文本转换为语音（同步）

    Args:
        text: 要转换的文本
        output_file: 输出文件路径
        voice: 语音名称
        rate: 语速

    Returns:
        是否成功

    Example:
        >>> text_to_speech("你好，这是测试", "output.mp3")
    """
    converter = EdgeTTSConverter(voice=voice, rate=rate)
    return converter.convert_sync(text, output_file)


async def text_to_speech_async(
    text: str,
    output_file: str,
    voice: str = 'xiaoxiao',
    rate: str = '+0%'
) -> bool:
    """
    快速将文本转换为语音（异步）

    Args:
        text: 要转换的文本
        output_file: 输出文件路径
        voice: 语音名称
        rate: 语速

    Returns:
        是否成功
    """
    converter = EdgeTTSConverter(voice=voice, rate=rate)
    return await converter.convert_text_to_speech(text, output_file)
