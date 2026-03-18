import json
from logger import setup_logger

logger = setup_logger()

class MatchResponse:

    def __init__(self, score: int, explanation: str, missing_skills: list, suggestions: list):
        self.score = score
        self.explanation = explanation
        self.missing_skills = missing_skills
        self.suggestions = suggestions

    @classmethod
    def from_json(cls, json_str: str):
        try:
            logger.info("Parsing AI response JSON")

            data = json.loads(json_str)

            # Validates
            score = data.get("score", 0)
            explanation = data.get("explanation", "")
            missing_skills = data.get("missing_skills", [])
            suggestions = data.get("suggestions", [])

            if not isinstance(score, int):
                logger.warning(f"Invalid score type: {type(score)}, defaulting to 0")
                score = 0

            if not isinstance(explanation, str):
                logger.warning("Invalid explanation type, defaulting to empty string")
                explanation = ""

            if not isinstance(missing_skills, list):
                logger.warning("Invalid missing_skills type, defaulting to empty list")
                missing_skills = []
            else:
                missing_skills = [str(skill) for skill in missing_skills]

            if not isinstance(suggestions, list):
                logger.warning("Invalid suggestions type, defaulting to empty list")
                suggestions = []
            else:
                suggestions = [str(s) for s in suggestions]

            return cls(
                score=score,
                explanation=explanation,
                missing_skills=missing_skills,
                suggestions=suggestions
            )

        except json.JSONDecodeError:
            logger.error("Failed to decode AI response as JSON")

        except Exception as e:
            logger.error(f"Unexpected error while parsing response: {str(e)}", exc_info=True)

        # Fallback 
        return cls(
            score=0,
            explanation="Failed to parse AI response",
            missing_skills=[],
            suggestions=[]
        )

    def to_dict(self):
        return {
            "score": self.score,
            "explanation": self.explanation,
            "missing_skills": self.missing_skills,
            "suggestions": self.suggestions
        }