from llm_obfuscator.tokenizer.huggingface_tokenizer import HuggingFaceTokenizer
from llm_obfuscator.tokenizer.openai_tokenizer import OpenAITokenizer
import tiktoken
import logging

logger = logging.getLogger(__name__)

DEFAULT_TOKENIZER = 'o200k_base'


class TokenizerRegistry:
    def __init__(self, preload_tokenizers=None):
        self.tokenizers = {}
        self._tokenizer_type_cache = {}
        if preload_tokenizers:
            self._preload_tokenizers(preload_tokenizers)

    def _preload_tokenizers(self, preload_tokenizers):
        for model_name in preload_tokenizers:
            self.register_tokenizer(model_name)

    def get_tokenizer_type(self, model_name: str):
        if model_name in self._tokenizer_type_cache:
            return self._tokenizer_type_cache[model_name]

        try:
            # Try OpenAI tokenizer first
            tiktoken.encoding_for_model(model_name) or tiktoken.get_encoding(model_name)
            tokenizer_type = "openai"
        except (KeyError, ValueError):
            try:
                # Try HuggingFace tokenizer as fallback
                HuggingFaceTokenizer(model_name)
                tokenizer_type = "huggingface"
            except OSError:
                # Default to OpenAI if both fail
                tokenizer_type = "openai"

        self._tokenizer_type_cache[model_name] = tokenizer_type
        return tokenizer_type

    def register_tokenizer(self, model_name: str):
        tokenizer_type = self.get_tokenizer_type(model_name)
        if tokenizer_type == "huggingface":
            self.tokenizers[model_name] = HuggingFaceTokenizer(model_name)
        elif tokenizer_type == "openai":
            self.tokenizers[model_name] = OpenAITokenizer(model_name)
        else:
            self.tokenizers[model_name] = OpenAITokenizer(DEFAULT_TOKENIZER)

        logger.info(f"Tokenizer registered: {model_name}")

    def get_tokenizer(self, model_name: str):
        if model_name not in self.tokenizers:
            try:
                self.register_tokenizer(model_name)
            except (KeyError, ValueError, OSError) as e:
                if DEFAULT_TOKENIZER not in self.tokenizers:
                    self.register_tokenizer(DEFAULT_TOKENIZER)
                return self.tokenizers[DEFAULT_TOKENIZER]
        return self.tokenizers[model_name]

    def list_active_tokenizers(self):
        return list(self.tokenizers.keys())

