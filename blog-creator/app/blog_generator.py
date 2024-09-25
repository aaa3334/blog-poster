import os
import random
import requests
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import List, Dict
import openai
import anthropic
from langfuse import Langfuse
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SECRET_KEY"))

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Anthropic client
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Initialize Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

# AI model selection
AI_MODELS = ["gpt-4o", "claude-3-5-sonnet-20240620"]
AI_MODELS = ['claude-3-5-sonnet-20240620']

def get_random_keywords(num_keywords: int = 3) -> List[str]:
    try:
        response = supabase.table("keywords").select("keyword").execute()
        all_keywords = [item['keyword'] for item in response.data]
        
        if len(all_keywords) < num_keywords:
            logger.warning(f"Not enough keywords in the database. Using all {len(all_keywords)} available keywords.")
            return all_keywords
        # print("All keywords are: ", all_keywords)
        return random.sample(all_keywords, num_keywords)
    except Exception as e:
        logger.error(f"Error fetching keywords from Supabase: {str(e)}")
        return []

def openai_completion(**kwargs):
    trace = langfuse.trace(name="openai_completion")
    generation = trace.generation(name="openai_generation", model=kwargs['model'])
    
    response = openai_client.chat.completions.create(**kwargs)
    
    generation.update(
        output=response.choices[0].message.content,
        prompt_tokens=response.usage.prompt_tokens,
        completion_tokens=response.usage.completion_tokens
    )
    
    return response.choices[0].message.function_call.arguments if response.choices[0].message.function_call else response.choices[0].message.content

def anthropic_completion(**kwargs):
    trace = langfuse.trace(name="anthropic_completion")
    generation = trace.generation(name="anthropic_generation", model=kwargs['model'])
    
    response = anthropic_client.messages.create(**kwargs)
    
    generation.update(
        output=response.content[0].text,
        prompt_tokens=response.usage.input_tokens,
        completion_tokens=response.usage.output_tokens
    )
    
    return response.content[0].text


def generate_blog_post(keywords: List[str], ai_model: str, company_name:str, company_description:str, target_market:str) -> Dict:
    prompt = f"""As an expert SEO writer and marketer, create a comprehensive blog post about {', '.join(keywords)}. 
    This post is for {company_name}, a real company {company_description}
      
    
    Follow these guidelines:
    1. Think through this content from an SEO perspective. Use the keywords naturally throughout the post.
    2. Provide general advice that would be valuable to {target_market}.
    3. Do not make up or mention any companies or competitors which do not exist. - Do not mention any other companies besides {company_name}.
    4. Focus on practical tips and industry trends related to the company.
    5. Include relevant statistics or data points if applicable, but only use factual information.
    6. Consider the user intent behind these keywords and address potential questions readers might have.

    Structure the blog post as a JSON object with the following fields:
    - title: An SEO-optimized, engaging title using the main keyword(s)
    - seo_description: A compelling meta description that includes the main keyword(s) and encourages clicks
    - intro_paragraph: An attention-grabbing introduction that outlines the post's content
    - paragraph_1: The first main point or section of your content
    - paragraph_2: The second main point or section of your content
    - paragraph_3: The third main point or section of your content
    - conclusion: A summary of key points and a call-to-action
    - image_keywords: A list of 3-5 keywords that best represent the visual aspects of the blog post content

    Use British english spelling and grammar and never use american spelling.
    Ensure each section is informative, engaging, and optimised for both readers and search engines.
    """

    try:
        if ai_model == "gpt-4o":
            function_def = {
                "name": "create_blog_post",
                "description": "Create a structured blog post",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "seo_description": {"type": "string"},
                        "intro_paragraph": {"type": "string"},
                        "paragraph_1": {"type": "string"},
                        "paragraph_2": {"type": "string"},
                        "paragraph_3": {"type": "string"},
                        "conclusion": {"type": "string"},
                        "image_keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 3,
                            "maxItems": 5
                        }
                    },
                    "required": ["title", "seo_description", "intro_paragraph", "paragraph_1", "paragraph_2", "paragraph_3", "conclusion", "image_keywords"]
                }
            }

            raw_content = openai_completion(
                model=ai_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes structured blog posts."},
                    {"role": "user", "content": prompt}
                ],
                functions=[function_def],
                function_call={"name": "create_blog_post"}
            )
            content = json.loads(raw_content)
        elif ai_model == "claude-3-5-sonnet-20240620":
            raw_content = anthropic_completion(
                model=ai_model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt + " Ensure the output is valid JSON."}
                ]
            )
            content = json.loads(raw_content)
        else:
            raise ValueError(f"Unsupported AI model: {ai_model}")

        return content
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        logger.error(f"Raw content that caused the error: {raw_content}")
        raise
    except Exception as e:
        logger.error(f"Error in generate_blog_post: {str(e)}")
        raise

def get_pexels_image(keywords: List[str], page_size: int = 10, max_retries: int = 3) -> str:
    api_key = os.getenv("PEXELS_API_KEY")
    base_url = "https://api.pexels.com/v1/search"
    
    for attempt in range(max_retries):
        try:
            # Randomize the page number to get different results each time
            page = random.randint(1, 5)
            
            url = f"{base_url}?query={'+'.join(keywords)}&per_page={page_size}&page={page}"
            headers = {"Authorization": api_key}
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if 'photos' in data and len(data['photos']) > 0:
                # Randomly select a photo from the results
                photo = random.choice(data['photos'])
                
                # Check if this image has been used before
                image_url = photo['src']['large']
                if not image_url_exists_in_database(image_url):
                    return image_url
            else:
                logger.warning(f"No images found from Pexels API for keywords: {keywords} on attempt {attempt + 1}")
        except Exception as e:
            logger.error(f"Error fetching image from Pexels API: {str(e)} on attempt {attempt + 1}")
    
    logger.error(f"Failed to find a unique image after {max_retries} attempts")
    return ""

def image_url_exists_in_database(image_url: str) -> bool:
    try:
        response = supabase.table("blog_posts").select("id").eq("image_url", image_url).execute()
        return len(response.data) > 0
    except Exception as e:
        logger.error(f"Error checking image URL in database: {str(e)}")
        return False

def create_blog_post(company_name:str, company_description:str, target_market:str):
    trace = langfuse.trace(name="create_blog_post")
    try:
        keywords = get_random_keywords()
        if not keywords:
            logger.error("No keywords available. Cannot generate blog post.")
            raise ValueError("No keywords available for blog post generation.")
        
        ai_model = random.choice(AI_MODELS)

        blog_content = generate_blog_post(keywords, ai_model, company_name, company_description, target_market)

        trace.generation(
            name="blog_post",
            metadata={"title": blog_content.get("title"), "keywords": keywords, "ai_model": ai_model}
        )

        image_keywords = blog_content.pop('image_keywords', [])
        image_url = get_pexels_image(image_keywords)

        blog_post = {
            **blog_content,
            "image_url": image_url,
            "ai_model": ai_model,
            "keywords": keywords,
            "image_keywords": image_keywords
        }

        response = supabase.table("blog_posts").insert(blog_post).execute()
        logger.info(f"Blog post created: {response.data}")

        trace.score(
            name="blog_post_created",
            value=1,
            comment="Successfully created and saved a blog post"
        )

        return blog_post

    except Exception as e:
        logger.error(f"Error in create_blog_post: {str(e)}")
        trace.event(
            name="error",
            payload={"message": str(e)}
        )
        raise