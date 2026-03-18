from fastapi import APIRouter, UploadFile, File, Form
from service.parser.pdf_parser import PDFParser
from service.match.resume_matcher import ResumeMatcher
from service.ai.groq_service import GroqService
from logger import setup_logger

router = APIRouter()
logger = setup_logger()

ai_service = GroqService()
matcher = ResumeMatcher(ai_service)
parser = PDFParser()

@router.post("/match")
async def match_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        logger.info("Received resume matching request")

        if not job_description.strip():
            return {"success": False, "error": "Job description cannot be empty"}

        if len(job_description) > 5000:
            return {"success": False, "error": "Job description too long"}

        if resume.content_type != "application/pdf":
            return {"success": False, "error": "Only PDF files are supported"}

        resume_text = parser.parse(resume.file)
        if not resume_text.strip():
            return {"success": False, "error": "Unable to extract text from resume"}

        result = await matcher.match(resume_text, job_description)
        return {"success": True, "data": result.to_dict()}

    except Exception as e:
        logger.error(f"Error in match endpoint: {str(e)}", exc_info=True)
        return {"success": False, "error": "Internal server error", "details": str(e)}