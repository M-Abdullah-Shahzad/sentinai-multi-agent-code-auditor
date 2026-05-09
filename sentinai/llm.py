import openai
import groq
from typing import Dict, List

from .config import (
    DEFAULT_MODEL,
    GROQ_API_KEY,
    OPENAI_API_KEY,
    OPENAI_DEFAULT_MODEL,
    SENTINAI_LLM_PROVIDER,
    FALLBACK_TO_OPENAI,
)


class LLMClient:
    def __init__(self):
        self.provider = SENTINAI_LLM_PROVIDER.lower()
        self.has_openai_key = bool(OPENAI_API_KEY)
        self.fallback_used = False
        self.fallback_reason = ""

        if self.provider == "groq":
            self.client = groq.Client(api_key=GROQ_API_KEY)
        else:
            openai.api_key = OPENAI_API_KEY
            self.client = openai

    def _switch_to_openai(self, reason: str = "OpenAI fallback enabled."):
        openai.api_key = OPENAI_API_KEY
        self.provider = "openai"
        self.client = openai
        self.fallback_used = True
        self.fallback_reason = reason

    def _should_fallback(self):
        return self.has_openai_key or FALLBACK_TO_OPENAI

    def validate_connection(self):
        if self.provider != "groq":
            return

        try:
            self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[{"role": "system", "content": "Health check."}],
                temperature=0,
                max_tokens=1,
            )
        except groq.AuthenticationError as exc:
            if self._should_fallback():
                self._switch_to_openai()
                return

            raise RuntimeError(
                "Groq authentication failed: invalid GROQ_API_KEY. "
                "Please verify your key in .env or your environment variables."
            ) from exc
        except groq.GroqError as exc:
            if self._should_fallback():
                self._switch_to_openai()
                return

            raise RuntimeError(
                f"Groq validation failed: {exc.__class__.__name__}: {exc}"
            ) from exc

    def chat(self, messages: List[Dict[str, str]], model: str = DEFAULT_MODEL, temperature: float = 0.2) -> str:
        if self.provider == "groq":
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                )
            except groq.AuthenticationError as exc:
                if self._should_fallback():
                    self._switch_to_openai()
                    fallback_model = OPENAI_DEFAULT_MODEL if model == DEFAULT_MODEL else model
                    return self.chat(messages, model=fallback_model, temperature=temperature)
                raise RuntimeError(
                    "Groq authentication failed: invalid GROQ_API_KEY. "
                    "Please verify your key in .env or your environment variables."
                ) from exc
            except groq.GroqError as exc:
                if self._should_fallback():
                    self._switch_to_openai()
                    fallback_model = OPENAI_DEFAULT_MODEL if model == DEFAULT_MODEL else model
                    return self.chat(messages, model=fallback_model, temperature=temperature)
                raise RuntimeError(
                    f"Groq request failed: {exc.__class__.__name__}: {exc}"
                ) from exc

            choice = response.choices[0]
            return choice.message.content or ""

        if model == DEFAULT_MODEL:
            model = OPENAI_DEFAULT_MODEL

        response = self.client.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message["content"].strip()
