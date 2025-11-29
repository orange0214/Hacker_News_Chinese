import json
import asyncio
from tkinter import N
from typing import Dict, Any, Optional, List
from app.core.config import settings
from app.core.prompts import Prompts
from openai import AsyncOpenAI

class TranslateService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url
        )
        self.model = settings.deepseek_model
        self.temperature = settings.deepseek_temperature
        self.sem = asyncio.Semaphore(settings.deepseek_concurrent_limit)

    async def translate_and_summarize(self, content: str) -> str:
        if not content:
            return None
        
        truncated_content = content[:100000]

        system_prompt = Prompts.SUMMARIZE_SYSTEM_Chinese

        try:
            async with self.sem:
                response = await self.client.chat.completions.create(
                    model = self.model,
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"文章内容: \n\n{truncated_content}"},
                    ],
                    response_format={"type": "json_object"},
                    temperature=self.temperature,
                )

                result_text = response.choices[0].message.content
                if not result_text:
                    return None
                
                # returns a Python dict object.
                return json.loads(result_text)

        except json.JSONDecodeError as e:
            print(f"[TranslateAndSummarizerService] Error: LLM returned invalid JSON")
            return None
        except Exception as e:
            print(f"[TranslateAndSummarizerService] Error processing content: {e}")
            return None

    # 接口args可能需要调整
    async def translate_and_summarize_batch(self, contents: Dict[str, str]) -> Dict[str, Optional[Dict[str, Any]]]:
        # concurrently translate and summarize multiple contents
        print(f"[TranslateAndSummarizerService] Translating and summarizing batch of {len(contents)} contents...")

        # TODO: 接口args可能需要调整
        urls = list(contents.keys())

        tasks = [self.translate_and_summarize(contents[url]) for url in urls]

        results = await asyncio.gather(*tasks)

        return dict(zip(urls, results))
        

translate_service = TranslateService()