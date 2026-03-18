from PyPDF2 import PdfReader
from logger import setup_logger
from PIL import Image
import pytesseract

logger = setup_logger()

class PDFParser:

    def parse(self, file) -> str:
        try:
            if file is None:
                logger.error("No file provided")
                raise ValueError("File cannot be None")

            reader = PdfReader(file)

            text = ""
            for i, page in enumerate(reader.pages):
                try:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                    else:
                        logger.warning(f"No text found on page {i}")
                except Exception as page_error:
                    logger.warning(f"Error reading page {i}: {str(page_error)}")

            final_text = text.strip()

            # Fallback OCR
            if not final_text:
                logger.info("Attempting OCR fallback for scanned PDF")
                try:
                    # Convert pages to images using temporary files
                    images = [page.to_image() for page in reader.pages]
                    ocr_text = ""
                    for i, img in enumerate(images):
                        ocr_text += pytesseract.image_to_string(img) + "\n"
                    final_text = ocr_text.strip()
                except Exception as e:
                    logger.error(f"OCR fallback failed: {str(e)}", exc_info=True)

            if not final_text:
                logger.warning("Failed to extract any text from PDF")

            logger.info("PDF parsing completed")
            return final_text

        except Exception as e:
            logger.error(f"PDF Parsing Error: {str(e)}", exc_info=True)
            raise RuntimeError("Failed to parse PDF")