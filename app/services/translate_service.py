import json
import asyncio
from typing import Dict, Any, Optional, List
from pydantic import ValidationError
from app.core.config import settings
from app.core.prompts import Prompts
from app.models.article import AITranslatedResult
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

    async def translate_and_summarize(
        self, 
        title: str, 
        hn_text: Optional[str]=None, 
        scraped_content: Optional[str]=None
        ) -> Optional[AITranslatedResult]:

        if not title and not hn_text and not scraped_content:
            return None
        
        safe_title = title or "N/A"
        safe_hn_text = hn_text or "N/A"
        safe_scraped_content = scraped_content[:100000] if scraped_content else "N/A"

        combined_input = f"""
        Title: {safe_title}
        Original Post Description: 
        {safe_hn_text}
        ---
        Scraped Article Content:
        {safe_scraped_content}
        """

        system_prompt = Prompts.SUMMARIZE_SYSTEM_Chinese

        try:
            async with self.sem:
                response = await self.client.chat.completions.create(
                    model = self.model,
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": combined_input},
                    ],
                    response_format={"type": "json_object"},
                    temperature=self.temperature,
                )

                result_text = response.choices[0].message.content

                if not result_text:
                    print(f"[TranslateAndSummarizerService] Error: LLM returned empty result")
                    return None
                
                return AITranslatedResult.model_validate_json(result_text)

        except json.JSONDecodeError:
            print(f"[TranslateAndSummarizerService] Error: LLM returned invalid JSON")
            return None
        except ValidationError as e:
            print(f"[TranslateAndSummarizerService] Validation Error: {e}")
            # TODO: Log the raw result_text here for debugging
            return None
        except Exception as e:
            print(f"[TranslateAndSummarizerService] Error processing content: {e}")
            return None

    async def translate_and_summarize_batch(
        self, 
        inputs: Dict[int, Dict[str, Any]]
        ) -> Dict[int, Optional[AITranslatedResult]]:
        # concurrently translate and summarize multiple inputs
        print(f"[TranslateAndSummarizerService] Translating and summarizing batch of {len(inputs)} inputs...")

        ids = list(inputs.keys())

        tasks = [
            self.translate_and_summarize(
                title = input[i].get("title", ""),
                hn_text = input[i].get("hn_text"),
                scraped_content = input[i].get("scraped_content"),
                ) for i in ids
            ]

        results = await asyncio.gather(*tasks)

        return dict(zip(ids, results))
        

translate_service = TranslateService()
