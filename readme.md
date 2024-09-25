
# Introduction
SEO is dead due to solutions like below and the way people search for information. We are still in the transition phase however where many are still searching old school and information is not quite there yet and blogs are still working slightly. It is not something anyone should sink a lot of money or time into however so I have just created a simple solution that anyone can use for their own website.

This project is a simple project that:

Phase 1: (blog-creator)
1) Takes in a company name, description, and target market
2) Generates a blog post on the company's website including identifying a unique image for the post
3) Saves the blog post to the database (here supabase is used)

Phase 2: (website-display)
A) In Supabase, we setup a trigger which will run the function on schedule (CRON)
B) The database is then automatically updated with the new blog post
C) Nextjs is used to fetch the new blog post from the database and display it on the website


## Techstack

- FastAPI
- Supabase
- OpenAI
- Anthropic
- LangFuse
- Nextjs14 (App router, Typescript) (could be anything - just write your own UI for displaying the blog posts)

(Deployment - Docker on Huggingface space is what I use but you can deploy anywhere you want)


# Setup steps:

## Basic setup

1) Fork/clone the repo
2) Copy .env.example to .env and fill in your keys (create a randomly generated secret for API_KEY= (either run openssl rand -hex 32 and use that or just hit the keyboard randomly))
(Note you can remove eg anthropic if you only want to use openai, or you can
remove langfuse if you don't want to track usage metrics - or change to other providers)
Note: Be VERY careful about the SUPABASE_SECRET_KEY - we need to bypass RLS (row level security) here as we are calling it from huggingface but be sure not to save it anywhere compromising.
3) Fill in your company information either in main.py or leave it for the scheduling job/api calls

## Set up supabase

In a new project or new schema (or old one if you want), go to the sql editor and run the code in sql_supabase.md


In the keywords table, add random terms you want for your blog posts (note you can also use chatgpt, anthropic, perplexity etc etc to generate this for you - i didn't set it up as it was easier to just ask it as opposed to getting a whole api set up for it).

4) Test the deployment by running the docker container locally:

`cd blog-creator
`docker build -t blog-generator .
`docker run -p 7860:7860 blog-generator

(Check it is working by going to localhost:7860/docs and testing the API)

## Deploying to huggingface

5) If deploying to huggingface, initialise a docker container in their *private* repo spaces and push your image to it - https://huggingface.co/spaces
(empty docker - then follow the steps there to push the repo)
(You can do public, but then change it so all api keys have to be passed to the API endpoint)

6) Add the api keys you created in the .env file to the huggingface space
Open the space settings and scroll down to 'variables and secrets' then add all the secrets from the .env file there

7) Set up your hugging face API key in the huggingface space to call the api
Click on profile -> settings -> access tokens -> create new token
(save this somewhere for now)

## Setting up the nextjs website

The code in website-display is for typescript and the nextjs14 app router. You will need to have connected up supabase to your app and have an initialised supabase client for the schema/database you created in supabase. The base page is a basic blog page which fetches the blog posts then they are displayed when you press on one of them (very stock standard for what blogs tend to look like).



# Questions?
Let me know if there are issues or questions - it is a pretty simple setup so just wanted to share as it is the full stack solution pretty much for how to generate a blog



