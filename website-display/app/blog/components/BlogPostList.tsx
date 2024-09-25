import { BlogPostCard } from "./BlogPostCard";

interface BlogPost {
  id: string;
  title: string;
  seo_description: string;
  image_url: string;
}

interface BlogPostListProps {
  posts: BlogPost[];
}

export function BlogPostList({ posts }: BlogPostListProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {posts.map((post) => (
        <BlogPostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
