from abc import ABC, abstractmethod
from logger import setup_logger

logger = setup_logger()

class BaseAIService(ABC):

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        # return response from AI model based on given prompt.
        pass

    def validate_prompt(self, prompt: str):
        if not prompt or not prompt.strip():
            logger.error("Empty prompt")
            raise ValueError("Prompt cannot be empty")

        if len(prompt) > 15000:
            logger.warning("Prompt size too large")