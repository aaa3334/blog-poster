
-- Create the keywords table
CREATE TABLE public.keywords (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    keyword TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create the blog_posts table
CREATE TABLE public.blog_posts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title TEXT NOT NULL,
    seo_description TEXT NOT NULL,
    intro_paragraph TEXT NOT NULL,
    paragraph_1 TEXT NOT NULL,
    paragraph_2 TEXT NOT NULL,
    paragraph_3 TEXT NOT NULL,
    conclusion TEXT NOT NULL,
    image_url TEXT NOT NULL,
    ai_model TEXT NOT NULL,
    keywords TEXT[] NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable Row Level Security for both tables
ALTER TABLE public.keywords ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.blog_posts ENABLE ROW LEVEL SECURITY;

-- Create policies for the keywords table
CREATE POLICY "Allow authenticated select on keywords" 
    ON public.keywords FOR SELECT 
    USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated insert on keywords" 
    ON public.keywords FOR INSERT 
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated update on keywords" 
    ON public.keywords FOR UPDATE 
    USING (auth.role() = 'authenticated');

-- Create policies for the blog_posts table
CREATE POLICY "Allow authenticated select on blog_posts" 
    ON public.blog_posts FOR SELECT 
    USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated insert on blog_posts" 
    ON public.blog_posts FOR INSERT 
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated update on blog_posts" 
    ON public.blog_posts FOR UPDATE 
    USING (auth.role() = 'authenticated');
