from service.ai.base_ai import BaseAIService
from models.response_model import MatchResponse
from logger import setup_logger
import asyncio

logger = setup_logger()

class ResumeMatcher:

    def __init__(self, ai_service: BaseAIService):
        self.ai_service = ai_service

    def _build_prompt(self, resume: str, jd: str) -> str:
        return f"""
            You are an AI hiring assistant.
            Analyze the resume against the job description and return ONLY valid JSON.

            Rules:
            - Score must be between 0 and 100
            - Be strict in evaluation
            - If skills are missing, reduce score accordingly
            - Keep explanation short and precise

            Output format:
            {{
                "score": number (0-100),
                "explanation": "short explanation",
                "missing_skills": ["skill1", "skill2"],
                "suggestions": ["suggestion1", "suggestion2"]
            }}

            Resume:
            {resume}

            Job Description:
            {jd}
        """

    def _validate_inputs(self, resume: str, jd: str):
        if not resume or resume.strip() == "":
            logger.error("Empty resume text provided")
            raise ValueError("Resume can't be empty")
        if not jd or jd.strip() == "":
            logger.error("Empty job description provided")
            raise ValueError("Job description can't be empty")

    def _apply_fallback_logic(self, result: MatchResponse) -> MatchResponse:
        # Ensure score is between 0-100
        if result.score < 0 or result.score > 100:
            logger.warning(f"Invalid score detected: {result.score}, clamping")
            result.score = max(0, min(result.score, 100))

        # Adjust score based on missing skills
        if result.score > 85 and len(result.missing_skills) > 3:
            logger.warning("High score with many missing skills, adjusting")
            result.score -= 10

        if result.score < 40 and len(result.missing_skills) < 2:
            logger.warning("Low score with few missing skills, adjusting")
            result.score += 10

        return result

    async def match(self, resume: str, jd: str) -> MatchResponse:
        try:
            self._validate_inputs(resume, jd)
            prompt = self._build_prompt(resume, jd)
            logger.info("Sending prompt to AI service")

            raw_response = await self.ai_service.generate_response(prompt)
            result = MatchResponse.from_json(raw_response)
            result = self._apply_fallback_logic(result)

            logger.info(f"Final score after validation: {result.score}")
            return result

        except Exception as e:
            logger.error(f"Error in resume matching: {str(e)}", exc_info=True)
            return MatchResponse(
                score=0,
                explanation="Failed to process resume",
                missing_skills=[],
                suggestions=[]
            )