from typing import Optional
from src.utils.logger import get_logger

logger = get_logger()


class Summarizer:
    """Generates article summaries using extractive summarization"""

    def __init__(self, max_length: int = 200, method: str = "extractive"):
        self.max_length = max_length
        self.method = method

    def generate_summary(self, content: str, max_length: Optional[int] = None) -> str:
        """
        Generate a summary of the article content

        Args:
            content: Full article content
            max_length: Maximum summary length (overrides default)

        Returns:
            Summary string
        """
        if not content:
            return ""

        max_len = max_length or self.max_length

        # If content is already short enough, return it
        if len(content) <= max_len:
            return content

        try:
            # Use sumy for extractive summarization
            from sumy.parsers.plaintext import PlaintextParser
            from sumy.nlp.tokenizers import Tokenizer
            from sumy.summarizers.lex_rank import LexRankSummarizer
            from sumy.nlp.stemmers import Stemmer
            from sumy.utils import get_stop_words

            # Determine number of sentences based on max_length
            # Approximate: 15 words per sentence, 6 characters per word
            num_sentences = max(1, max_len // 90)

            parser = PlaintextParser.from_string(content, Tokenizer("english"))
            stemmer = Stemmer("english")
            summarizer = LexRankSummarizer(stemmer)
            summarizer.stop_words = get_stop_words("english")

            summary_sentences = summarizer(parser.document, num_sentences)

            # Combine sentences
            summary = " ".join(str(sentence) for sentence in summary_sentences)

            # Truncate if still too long
            if len(summary) > max_len:
                summary = summary[:max_len].rsplit(' ', 1)[0] + "..."

            return summary

        except Exception as e:
            logger.warning(f"Summarization failed, using fallback: {e}")
            # Fallback: simple truncation
            return self._fallback_summary(content, max_len)

    def _fallback_summary(self, content: str, max_length: int) -> str:
        """
        Fallback summarization using simple truncation

        Args:
            content: Full content
            max_length: Maximum length

        Returns:
            Truncated content
        """
        if len(content) <= max_length:
            return content

        # Truncate at word boundary
        truncated = content[:max_length].rsplit(' ', 1)[0]
        return truncated + "..."
