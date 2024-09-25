import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from app.blog_generator import create_blog_post
import logging
from fastapi import FastAPI, HTTPException, Depends, Header


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
security = HTTPBearer()

API_KEY = os.getenv("API_KEY")

def verify_api_key(authorisation_mine: str = Header(...)):
    if authorisation_mine != f"Bearer {API_KEY}":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return True

@app.post("/generate-blog-post")
async def generate_blog_post( company_name: str, company_description: str, target_market: str, authorized: bool = Depends(verify_api_key)):
    
    # Note you can either enter the company_name etc. through the api call itself, or you can
    # just hardcode it here
    
    print("Received request to generate blog post")
    logger.info("Received request to generate blog post")
    try:
        blog_post = create_blog_post(company_name, company_description, target_market)
        logger.info("Blog post generated successfully")
        return {"message": "Blog post generated and saved successfully", "blog_post": blog_post}
    except Exception as e:
        error_message = f"Error generating blog post: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@app.get("/")
async def root():
    return {"message": "Blog Generation API is running"}