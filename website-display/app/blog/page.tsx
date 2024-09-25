import React from "react";
import { getBlogPosts } from "./actions";
import { BlogPostList } from "./components/BlogPostList";

export default async function BlogPage() {
  const posts = await getBlogPosts();

  if (!posts) {
    return <div>Error loading blog posts</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Blog Posts</h1>
      <BlogPostList posts={posts} />
    </div>
  );
}
