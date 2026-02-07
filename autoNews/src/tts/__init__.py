"""
TTS (Text-to-Speech) Module
"""

from src.tts.edge_tts_converter import (
    EdgeTTSConverter,
    text_to_speech,
    text_to_speech_async
)

__all__ = [
    'EdgeTTSConverter',
    'text_to_speech',
    'text_to_speech_async'
]
