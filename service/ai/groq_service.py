import asyncio
import json
from groq import Groq
from service.ai.base_ai import BaseAIService
from config import Config
from logger import setup_logger

logger = setup_logger()

class GroqService(BaseAIService):

    def __init__(self):
        if not Config.GROQ_API_KEY:
            logger.error("GROQ_API_KEY is missing.")
            raise ValueError("GROQ_API_KEY is required")
        self.client = Groq(api_key=Config.GROQ_API_KEY)

    async def generate_response(self, prompt: str) -> str:
        self.validate_prompt(prompt)

        try:
            response = await asyncio.to_thread(
                lambda: self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a strict JSON generator. Always return valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
            )

            content = response.choices[0].message.content.strip()
            logger.info("Received response from Groq API")

            return self._parse_json(content)

        except Exception as e:
            logger.error(f"Groq AI Error: {str(e)}", exc_info=True)
            raise RuntimeError("Failed to generate AI response")

    def _parse_json(self, content: str) -> str:
        try:
            data_start = content.find("{")
            data_end = content.rfind("}") + 1
            if data_start == -1 or data_end == -1:
                raise ValueError("No JSON found in AI response")

            json_str = content[data_start:data_end]
            # valid JSON
            parsed = json.loads(json_str)
            return json.dumps(parsed)

        except Exception as e:
            logger.error(f"Error parsing AI JSON response: {str(e)}", exc_info=True)
            # fallback JSON
            return json.dumps({
                "score": 0,
                "explanation": "Failed to parse AI response",
                "missing_skills": [],
                "suggestions": []
            })