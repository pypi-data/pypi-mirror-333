# dh_tool/llm_tool/llm/gemini.py
from typing import Any

import google.generativeai as genai
from google.generativeai import GenerationConfig
from google.generativeai.types.generation_types import AsyncGenerateContentResponse

from .base import BaseLLM
from ..utils.response_parser import parse_gemini_response
from ..utils.stream_processor import GeminiStreamProcessor


class GeminiModel(BaseLLM):

    def _get_allowed_params(self):
        self._allowed_generation_params = {
            attr for attr in dir(GenerationConfig) if not attr.startswith("_")
        }

    def _setup_client(self):
        genai.configure(api_key=self.config.api_key)
        if self.system_instruction:
            self._client = genai.GenerativeModel(
                model_name=self.model,
                system_instruction=self.system_instruction,
                # generation_config=self.generation_params,
            )
        else:
            self._client = genai.GenerativeModel(
                model_name=self.model,
                # generation_config=self.generation_params,
            )

    async def generate(self, message: str, parsed=True, **kwargs: Any):
        generation_params = self.generation_params
        if kwargs:
            for k, v in kwargs.items():
                if k not in self._allowed_generation_params:
                    raise ValueError(f"Parameter '{k}' is not allowed.")
            generation_params.update(**kwargs)

        response = await self._client.generate_content_async(
            contents=message, generation_config=generation_params
        )
        if parsed:
            return self.parse_response(response)
        return response

    async def generate_stream(
        self, message: str, vebose=True, parsed=True, **kwargs: Any
    ):
        generation_params = self.generation_params
        if kwargs:
            for k, v in kwargs.items():
                if k not in self._allowed_generation_params:
                    raise ValueError(f"Parameter '{k}' is not allowed.")
            generation_params.update(**kwargs)

        stream = await self._client.generate_content_async(
            contents=message, generation_config=generation_params, stream=True
        )
        response = await GeminiStreamProcessor.process_stream(stream, verbose=vebose)
        if parsed:
            return self.parse_response(response)
        return response

    @staticmethod
    def parse_response(response: AsyncGenerateContentResponse):
        return parse_gemini_response(response)
