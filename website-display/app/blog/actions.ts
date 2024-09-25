"use server";
import { supabaseBlog } from "@/lib/supabaseClient";
import { cookies } from "next/headers";

export async function getBlogPosts() {
  const supabaseBlogClient = supabaseBlog;
  const { data, error } = await supabaseBlog
    .from("blog_posts")
    .select("*")
    .order("created_at", { ascending: false });

  console.log("data", data);
  return data;
}
