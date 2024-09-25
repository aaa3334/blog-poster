import React from "react";
import { getBlogPosts } from "../actions";
import Image from "next/image";

function formatContent(content: string) {
  // Split the content by double asterisks
  const parts = content.split(/\*\*(.*?)\*\*/);
  return parts.map((part, index) => {
    if (index % 2 === 1) {
      // Odd indexes are the subheadings
      // Remove the colon if it exists at the end of the subheading
      const cleanedPart = part.endsWith(":") ? part.slice(0, -1) : part;
      return (
        <h3 key={index} className="text-2xl font-bold mt-6 mb-4">
          {cleanedPart}
        </h3>
      );
    } else {
      // Even indexes are regular paragraphs
      return (
        <p key={index} className="mb-4">
          {part}
        </p>
      );
    }
  });
}

export default async function BlogPostPage({
  params,
}: {
  params: { slug: string };
}) {
  const posts = await getBlogPosts();
  const post = posts?.find((p) => p.id === params.slug);

  if (!post) {
    return <div>Blog post not found</div>;
  }

  return (
    <article className="max-w-3xl mx-auto px-4 py-8">
      <div className="relative w-full h-24 mb-8">
        <Image
          src={post.image_url}
          alt={post.title}
          fill
          sizes="100vw"
          className="object-cover"
          priority
        />
      </div>

      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
        <p className="text-xl text-gray-600 italic">{post.seo_description}</p>
      </header>

      <div className="prose prose-lg max-w-none">
        <div className="mb-6">{formatContent(post.intro_paragraph)}</div>
        <div className="mb-6">{formatContent(post.paragraph_1)}</div>
        <div className="mb-6">{formatContent(post.paragraph_2)}</div>
        <div className="mb-6">{formatContent(post.paragraph_3)}</div>
        <div className="mb-6">{formatContent(post.conclusion)}</div>
      </div>
    </article>
  );
}
