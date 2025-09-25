-- MySQL Insert Script for All Tables
-- Note: Assuming user_id values 1-5 exist in a users table

-- Insert sample data into images table
INSERT INTO images (type, path, created_at, modified_at) VALUES
('url', 'https://example.com/images/product1.jpg', NOW(), NOW()),
('file', '/uploads/images/product2.png', NOW(), NOW()),
('url', 'https://example.com/images/social1.jpg', NOW(), NOW()),
('file', '/uploads/images/social2.png', NOW(), NOW()),
('url', 'https://example.com/images/product5.jpg', NOW(), NOW());

INSERT INTO products (name, description, custom_text, customize_count, last_customized_at, image_id, category, price, user_id, sell_count, available, ongoing_order, comment_id, click, created_at, modified_at) VALUES
('Premium Cotton T-Shirt', 'High-quality 100% cotton t-shirt with comfortable fit', 'Best seller!', 15, '2024-09-20 10:30:00', 1, 'T_SHIRT', 29.99, 1, 45, TRUE, 5, NULL, 120, NOW(), NOW()),
('Classic Blue Jeans', 'Durable denim jeans with modern cut', 'Trending now', 8, '2024-09-22 14:15:00', 2, 'PANT', 79.99, 2, 23, TRUE, 2, NULL, 85, NOW(), NOW()),
('Winter Hoodie', 'Warm and cozy hoodie perfect for cold weather', 'Limited edition', 12, '2024-09-21 16:45:00', 5, 'HOODIE', 49.99, 1, 31, TRUE, 3, NULL, 95, NOW(), NOW()),
('Summer Dress', 'Light and breezy dress for summer occasions', 'New arrival', 6, '2024-09-23 11:20:00', NULL, 'DRESS', 59.99, 3, 18, TRUE, 1, NULL, 67, NOW(), NOW()),
('Leather Jacket', 'Genuine leather jacket with vintage style', 'Premium quality', 22, '2024-09-19 09:10:00', NULL, 'JACKET', 199.99, 4, 12, FALSE, 0, NULL, 201, NOW(), NOW());

-- Insert sample data into apis table
INSERT INTO apis (user_id, type, endpoint, access_key, secret_key, `load`, extra, created_at, modified_at) VALUES
(1, 'openai', 'https://api.openai.com/v1', 'sk-test123456789', 'secret123', 25, '{"model": "gpt-4", "max_tokens": 1000}', NOW(), NOW()),
(2, 'twitter', 'https://api.twitter.com/2', 'twitter_key_456', 'twitter_secret_789', 15, '{"version": "2.0", "rate_limit": 300}', NOW(), NOW()),
(1, 'linkedin', 'https://api.linkedin.com/v2', 'linkedin_key_123', 'linkedin_secret_456', 10, '{"scope": "w_member_social", "version": "v2"}', NOW(), NOW()),
(3, 'gemini', 'https://generativelanguage.googleapis.com/v1', 'gemini_key_789', NULL, 30, '{"model": "gemini-pro", "safety_settings": "high"}', NOW(), NOW()),
(4, 'facebook', 'https://graph.facebook.com/v18.0', 'facebook_key_012', 'facebook_secret_345', 20, '{"permissions": ["pages_manage_posts", "pages_read_engagement"]}', NOW(), NOW());

-- Insert sample data into social_platforms table
INSERT INTO social_platforms (name, type, status, api_id, isVerified, isActive, user_id, created_at, modified_at) VALUES
('My Twitter Account', 'twitter', 'connected', 'twitter_123', TRUE, TRUE, 1, NOW(), NOW()),
('Business LinkedIn', 'linkedin', 'connected', 'linkedin_456', TRUE, TRUE, 2, NOW(), NOW()),
('Brand Facebook Page', 'facebook', 'connected', 'facebook_789', FALSE, TRUE, 1, NOW(), NOW()),
('Instagram Business', 'instagram', 'expired', 'instagram_012', TRUE, FALSE, 3, NOW(), NOW()),
('Personal Twitter', 'twitter', 'disconnected', NULL, FALSE, TRUE, 4, NOW(), NOW());

-- Insert sample data into posts table
INSERT INTO posts (type, content_text, content_tone, platform_id, product_id, image_id, user_id, schedule_time, status, published_at, remarks, api_ids, created_at, modified_at) VALUES
('text', '{"text": "Check out our amazing new cotton t-shirt! Perfect for any occasion. #fashion #style"}', 'casual', 1, 1, 3, 1, '2024-09-25 10:00:00', 'scheduled', NULL, 'First product launch post', '[1, 2]', NOW(), NOW()),
('image', '{"text": "New arrival alert! 🔥 These jeans are flying off the shelves!", "hashtags": ["#denim", "#fashion", "#newproduct"]}', 'friendly', 2, 2, 4, 2, '2024-09-24 14:30:00', 'published', '2024-09-24 14:30:15', 'Great engagement expected', '[3]', NOW(), NOW()),
('carousel', '{"text": "Winter collection is here! Stay warm and stylish.", "slides": ["hoodie1.jpg", "hoodie2.jpg"]}', 'professional', 3, 3, NULL, 1, '2024-09-26 09:00:00', 'draft', NULL, 'Need to finalize carousel images', '[1, 5]', NOW(), NOW()),
('story', '{"text": "Behind the scenes of our summer dress photoshoot ☀️", "duration": 24}', 'humorous', 4, 4, NULL, 3, '2024-09-24 12:00:00', 'failed', NULL, 'Platform connection issue', '[4]', NOW(), NOW()),
('reel', '{"text": "Leather jacket styling tips for autumn 🍂", "music": "trending_song_1"}', 'formal', 1, 5, NULL, 4, NULL, 'pending', NULL, 'Waiting for approval', '[1, 2]', NOW(), NOW());

-- Insert sample data into ai_insights table
INSERT INTO ai_insights (post_id, insight_type, insight_text, metadata, created_at, modified_at) VALUES
(1, 'engagement', 'This post is likely to receive high engagement due to the casual tone and relevant hashtags. Expected reach: 2000-3000 users.', '{"confidence": 0.85, "factors": ["hashtags", "tone", "timing"]}', NOW(), NOW()),
(2, 'timing', 'Posted at optimal time for LinkedIn audience. Business hours posts typically perform 40% better on this platform.', '{"optimal_time": "14:30", "timezone": "UTC", "expected_improvement": 0.4}', NOW(), NOW()),
(3, 'content', 'Carousel format is excellent for showcasing product variants. Consider adding more visual elements and customer testimonials.', '{"format_score": 9, "suggestions": ["testimonials", "product_variants"]}', NOW(), NOW()),
(4, 'audience', 'Summer dress content resonates well with 25-35 age demographic. This represents 60% of your follower base.', '{"target_age": "25-35", "audience_match": 0.6, "gender_split": {"female": 0.75, "male": 0.25}}', NOW(), NOW()),
(5, 'performance', 'Leather jacket posts historically perform well in autumn. Similar posts averaged 150 likes and 25 shares.', '{"historical_avg": {"likes": 150, "shares": 25}, "seasonal_boost": 1.2}', NOW(), NOW());

-- Insert sample data into post_analyses table
INSERT INTO post_analyses (post_id, analysis, ai_insight_id, created_at, modified_at) VALUES
(1, '{"sentiment": "positive", "readability": 8.5, "seo_score": 7.2, "keywords": ["cotton", "t-shirt", "fashion"], "engagement_prediction": 85}', 1, NOW(), NOW()),
(2, '{"sentiment": "excited", "readability": 9.1, "seo_score": 8.0, "keywords": ["jeans", "denim", "new"], "engagement_prediction": 92, "emoji_count": 1}', 2, NOW(), NOW()),
(3, '{"sentiment": "professional", "readability": 8.8, "seo_score": 7.8, "keywords": ["winter", "hoodie", "style"], "engagement_prediction": 78}', 3, NOW(), NOW()),
(4, '{"sentiment": "playful", "readability": 9.3, "seo_score": 6.9, "keywords": ["summer", "dress", "photoshoot"], "engagement_prediction": 88, "emoji_count": 1}', 4, NOW(), NOW()),
(5, '{"sentiment": "informative", "readability": 8.7, "seo_score": 8.5, "keywords": ["leather", "jacket", "autumn"], "engagement_prediction": 81, "emoji_count": 1}', 5, NOW(), NOW());

-- Verify the inserts with count queries
SELECT 'images' as table_name, COUNT(*) as record_count FROM images
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'apis', COUNT(*) FROM apis
UNION ALL
SELECT 'social_platforms', COUNT(*) FROM social_platforms
UNION ALL
SELECT 'posts', COUNT(*) FROM posts
UNION ALL
SELECT 'ai_insights', COUNT(*) FROM ai_insights
UNION ALL
SELECT 'post_analyses', COUNT(*) FROM post_analyses;