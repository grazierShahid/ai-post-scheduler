export enum PlatformType {
  TWITTER = "twitter",
  LINKEDIN = "linkedin",
  FACEBOOK = "facebook",
  INSTAGRAM = "instagram",
}

export enum PostStatus {
  DRAFT = "draft",
  PUBLISHED = "published",
  PENDING = "pending",
  SCHEDULED = "scheduled",
  FAILED = "failed",
}

export enum PostTone {
  PROFESSIONAL = "professional",
  CASUAL = "casual",
  FRIENDLY = "friendly",
  FORMAL = "formal",
  HUMOROUS = "humorous",
}

export enum ProductCategory {
  SHIRT = "shirt",
  T_SHIRT = "t-shirt",
  PANT = "pant",
  JACKET = "jacket",
  HOODIE = "hoodie",
  DRESS = "dress",
}

export interface ImageResponse {
  id: number;
  path: string;
}

export interface PostSubmitRequest {
  user_id: number;
  content_text: string;
  platforms: PlatformType[];
  product_id?: number;
  schedule_time?: string;
  hashtags: string[];
  target_audience?: string;
  call_to_action?: string;
  content_tone: PostTone;
  api_ids?: string[];
  image_url?: string; // Add this line
}

export interface PostListItem {
  id: number;
  content_text: string;
  image?: ImageResponse;
  platforms: PlatformType[];
  product_id?: number;
  schedule_time?: string;
  status: PostStatus;
  hashtags: string[];
  created_at: string;
}

export interface PostListResponse {
  posts: PostListItem[];
  total: number;
  limit: number;
  offset: number;
}

export interface PostSummaryResponse {
  total_posts: number;
  published_count: number;
  scheduled_count: number;
  failed_count: number;
  draft_count: number;
}

export interface AiInsightResponse {
  insight_text: string;
}

export interface ProductDesignCreateRequest {
  user_id: number;
  product_id: number;
  custom_text: string;
  text_position_x: number;
  text_position_y: number;
  text_size: number;
  text_color: string;
}

export interface ProductDesignItem {
  id: number;
  product_id: number;
  custom_text: string;
  text_position_x: number;
  text_position_y: number;
  text_size: number;
  text_color: string;
  created_at: string;
}

export interface ProductDesignListResponse {
  items: ProductDesignItem[];
  total: number;
}

export interface AISuggestionsRequest {
  user_id: number;
  content_text: string;
  product_category?: ProductCategory;
  platform_types: PlatformType[];
  target_audience?: string;
  brand_tone: PostTone;
}

export interface ContentReview {
  score: number;
  suggestions: string[];
}

export interface AISuggestionsResponse {
  hashtag_suggestions: string[];
  content_review: ContentReview;
  optimized_content: string;
}

export interface AIBestTimeRequest {
  user_id: number;
  platform_types: PlatformType[];
  target_audience?: string;
}

export interface AIBestTimeResponse {
  suggestions: string[];
}