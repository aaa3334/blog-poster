import Image from "next/image";
import Link from "next/link";

interface BlogPost {
  id: string;
  title: string;
  seo_description: string;
  image_url: string;
}

interface BlogPostCardProps {
  post: BlogPost;
}

export function BlogPostCard({ post }: BlogPostCardProps) {
  return (
    <Link href={`/blog/${post.id}`} className="block">
      <div className="max-w-sm rounded overflow-hidden shadow-lg">
        <div className="relative w-full h-48">
          <Image
            src={post.image_url}
            alt={post.title}
            fill
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            className="object-cover"
          />
        </div>
        <div className="px-6 py-4">
          <div className="font-bold text-xl mb-2">{post.title}</div>
          <p className="text-gray-700 text-base">{post.seo_description}</p>
        </div>
      </div>
    </Link>
  );
}
