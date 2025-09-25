# Backend API Endpoints Analysis

## 1. POST /api/v1/submit-post
**Type**: multipart/form-data
**Required Fields**:
- user_id (integer)
- content_text (string)
- platform_list (array of strings)

**Optional Fields**:
- image (binary)
- product_id (integer, nullable)
- schedule_time (string, nullable)
- hashtags (string, default: "")
- target_audience (string, nullable)
- call_to_action (string, nullable)
- content_tone (string, default: "casual")
- api_ids (string, default: "")

## 2. POST /api/v1/suggest-hashtag
**Type**: application/json
**Required Fields**:
- user_id (integer)
- content_text (string)
- platform_types (array of PlatformType)

**Optional Fields**:
- product_category (ProductCategory, nullable)
- target_audience (string, nullable)
- brand_tone (PostTone, default: "casual")

## 3. POST /api/v1/suggest-best-time
**Type**: application/json
**Required Fields**:
- user_id (integer)
- platform_types (array of PlatformType)

**Optional Fields**:
- target_audience (string, nullable)

## 4. GET /api/v1/posts
**Query Parameters**:
- limit (integer, default: 20)
- offset (integer, default: 0)

## 5. GET /api/v1/post/{post_id}
**Path Parameters**:
- post_id (integer, required)

## 6. POST /api/v1/product-designs
**Type**: application/json
**Required Fields**:
- user_id (integer)
- product_id (integer)
- custom_text (string)

**Optional Fields**:
- font_style (string, default: "Arial")
- text_color (string, default: "#000000")
- text_position_x (integer, default: 0)
- text_position_y (integer, default: 0)

## 7. GET /api/v1/product-designs
**Query Parameters**:
- user_id (integer, required)

## 8. GET /api/v1/product-designs/{design_id}
**Path Parameters**:
- design_id (integer, required)

## 9. GET /api/v1/product-images/{product_id}
**Path Parameters**:
- product_id (integer, required)

## 10. GET /api/v1/analytics/posts/summary
**Query Parameters** (all optional):
- user_id (integer, nullable)
- platform_type (PlatformType, nullable)
- start_date (string datetime, nullable)
- end_date (string datetime, nullable)

## 11. GET /api/v1/analytics/ai-insight
**Query Parameters**:
- user_id (integer, required)
- query (string, optional)

## Enums:
- PlatformType: ["twitter", "linkedin", "facebook", "instagram"]
- PostTone: ["professional", "casual", "friendly", "formal", "humorous"]
- PostStatus: ["draft", "published", "pending", "scheduled", "failed"]
- ProductCategory: ["shirt", "t-shirt", "pant", "jacket", "hoodie", "dress"]