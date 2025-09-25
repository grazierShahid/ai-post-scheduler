# API Documentation - Social Media AI Agent

## Overview
This API documentation covers the FastAPI backend for the AI-powered social media scheduling system with product customization and analytics features.

**Base URL**: `http://localhost:8000`

---

## User Authentication APIs

### API-1: User Signup
- **URL**: `base_url/auth/signup`
- **Method**: `POST`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Cookie**: None
- **Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "phone": "+1234567890",
    "profession": "Designer"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "message": "User created successfully"
  }
  ```

### API-2: User Signin
- **URL**: `base_url/auth/signin`
- **Method**: `POST`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Cookie**: None
- **Body**:
  ```json
  {
    "email": "john@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "profession": "Designer"
    },
    "message": "Login successful"
  }
  ```

### API-3: User Signout
- **URL**: `base_url/auth/signout`
- **Method**: `POST`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Cookie**: None
- **Body**: None
- **Response**:
  ```json
  {
    "message": "Logout successful"
  }
  ```

---

## Post APIs

### API-4: Submit Post with Text and Image
- **URL**: `base_url/posts`
- **Method**: `POST`
- **Headers**: 
  ```json
  {
    "Content-Type": "multipart/form-data"
  }
  ```
- **Cookie**: None
- **Body** (Form Data):
  ```form-data
  user_id: 1
  image: <image_file>
  content_text: "Check out our amazing new product! Perfect for summer vibes 🌞"
  platform_types: ["twitter", "instagram", "facebook"]
  product_id: 2
  schedule_time: "2025-01-20T15:30:00Z"
  content_tone: "casual"
  hashtags: ["#summer", "#fashion", "#newdrop"]
  target_audience: "young_adults"
  call_to_action: "Shop now and get 20% off!"
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "content_text": "Check out our amazing new product! Perfect for summer vibes 🌞",
    "image": {
      "id": 3,
      "path": "/uploads/posts/image_123.jpg"
    },
    "platforms": ["twitter", "instagram", "facebook"],
    "product_id": 2,
    "schedule_time": "2025-01-20T15:30:00Z",
    "status": "scheduled",
    "hashtags": ["#summer", "#fashion", "#newdrop"],
    "target_audience": "young_adults",
    "call_to_action": "Shop now and get 20% off!",
    "created_at": "2025-01-15T10:30:00Z"
  }
  ```

### API-5: Get Hashtag Suggestions and Content Review
- **URL**: `base_url/posts/ai-suggestions`
- **Method**: `POST`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Cookie**: None
- **Body**:
  ```json
  {
    "content_text": "Check out our new summer t-shirt collection",
    "product_category": "t-shirt",
    "platform_types": ["instagram", "twitter"],
    "target_audience": "young_adults",
    "brand_tone": "casual"
  }
  ```
- **Response**:
  ```json
  {
    "hashtag_suggestions": [
      "#summercollection",
      "#tshirt",
      "#fashion",
      "#casualwear",
      "#trendy",
      "#ootd",
      "#stylish",
      "#comfortable",
      "#newdrop",
      "#summerstyle"
    ],
    "content_review": {
      "score": 85,
      "suggestions": [
        "Consider adding an emoji to make the post more engaging",
        "The tone matches your target audience perfectly",
        "Add a call-to-action to drive more conversions",
        "Perfect length for Instagram and Twitter"
      ]
    },
    "optimized_content": "Check out our fresh summer t-shirt collection! ☀️ Perfect for those sunny days ahead. #summercollection #fashion"
  }
  ```

### API-6: Get Posts List
- **URL**: `base_url/posts`
- **Method**: `GET`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Cookie**: None
- **Body**: None
- **Query Parameters**:
  ```
  ?user_id=1&status=scheduled&platform_type=instagram&limit=10&offset=0
  ```
- **Response**:
  ```json
  {
    "posts": [
      {
        "id": 1,
        "content_text": "Check out our amazing new product!",
        "image": {
          "id": 3,
          "path": "/uploads/posts/image_123.jpg"
        },
        "platforms": ["twitter", "instagram"],
        "product_id": 2,
        "schedule_time": "2025-01-20T15:30:00Z",
        "status": "scheduled",
        "hashtags": ["#summer", "#fashion"],
        "created_at": "2025-01-15T10:30:00Z"
      }
    ],
    "total": 1,
    "limit": 10,
    "offset": 0
  }
  ```

### API-7: Get Post by ID
- **URL**: `base_url/posts/{post_id}`
- **Method**: `GET`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Cookie**: None
- **Body**: None
- **Response**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "content_text": "Check out our amazing new product! Perfect for summer vibes 🌞",
    "image": {
      "id": 3,
      "path": "/uploads/posts/image_123.jpg"
    },
    "platforms": ["twitter", "instagram", "facebook"],
    "product": {
      "id": 2,
      "name": "Summer T-Shirt",
      "category": "t-shirt",
      "price": 25.99
    },
    "schedule_time": "2025-01-20T15:30:00Z",
    "published_at": null,
    "status": "scheduled",
    "hashtags": ["#summer", "#fashion", "#newdrop"],
    "target_audience": "young_adults",
    "call_to_action": "Shop now and get 20% off!",
    "content_tone": "casual",
    "created_at": "2025-01-15T10:30:00Z",
    "modified_at": "2025-01-15T10:30:00Z"
  }
  ```

---

## Product Customization APIs

### API-8: Add Text Customization to Product
- **URL**: `base_url/products/customizations`
- **Method**: `POST`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Cookie**: None
- **Body**:
  ```json
  {
    "user_id": 1,
    "product_id": 2,
    "custom_text": "MY AWESOME DESIGN",
    "font_family": "Arial",
    "font_size": 24,
    "text_color": "#FFFFFF",
    "text_position": {
      "x": 150,
      "y": 200
    },
    "text_rotation": 0,
    "text_opacity": 1.0,
    "design_name": "Summer Vibes Tee",
    "background_color": "#000000",
    "text_style": "bold"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "product": {
      "id": 2,
      "name": "Classic White T-Shirt",
      "category": "t-shirt",
      "image_path": "/images/products/tshirt_white.jpg"
    },
    "customization": {
      "custom_text": "MY AWESOME DESIGN",
      "font_family": "Arial",
      "font_size": 24,
      "text_color": "#FFFFFF",
      "text_position": {
        "x": 150,
        "y": 200
      },
      "text_rotation": 0,
      "text_opacity": 1.0,
      "background_color": "#000000",
      "text_style": "bold"
    },
    "design_name": "Summer Vibes Tee",
    "preview_url": "/customizations/1/preview",
    "created_at": "2025-01-15T11:00:00Z"
  }
  ```

### API-9: List View Customizations
- **URL**: `base_url/products/customizations`
- **Method**: `GET`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Cookie**: None
- **Body**: None
- **Query Parameters**:
  ```
  ?user_id=1&product_category=t-shirt&limit=10&offset=0
  ```
- **Response**:
  ```json
  {
    "customizations": [
      {
        "id": 1,
        "design_name": "Summer Vibes Tee",
        "product": {
          "id": 2,
          "name": "Classic White T-Shirt",
          "category": "t-shirt"
        },
        "custom_text": "MY AWESOME DESIGN",
        "preview_url": "/customizations/1/preview",
        "created_at": "2025-01-15T11:00:00Z"
      },
      {
        "id": 2,
        "design_name": "Cool Graphic",
        "product": {
          "id": 3,
          "name": "Black Hoodie",
          "category": "hoodie"
        },
        "custom_text": "STAY COOL",
        "preview_url": "/customizations/2/preview",
        "created_at": "2025-01-14T09:30:00Z"
      }
    ],
    "total": 2,
    "limit": 10,
    "offset": 0
  }
  ```

### API-10: Get Customization by ID
- **URL**: `base_url/products/customizations/{customization_id}`
- **Method**: `GET`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Cookie**: None
- **Body**: None
- **Response**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "product": {
      "id": 2,
      "name": "Classic White T-Shirt",
      "category": "t-shirt",
      "price": 19.99,
      "image_path": "/images/products/tshirt_white.jpg"
    },
    "customization": {
      "custom_text": "MY AWESOME DESIGN",
      "font_family": "Arial",
      "font_size": 24,
      "text_color": "#FFFFFF",
      "text_position": {
        "x": 150,
        "y": 200
      },
      "text_rotation": 0,
      "text_opacity": 1.0,
      "background_color": "#000000",
      "text_style": "bold"
    },
    "design_name": "Summer Vibes Tee",
    "preview_url": "/customizations/1/preview",
    "created_at": "2025-01-15T11:00:00Z",
    "modified_at": "2025-01-15T11:00:00Z"
  }
  ```

---

## Analytics Dashboard APIs

### API-11: Get Scheduled Post Stats and AI Insights with Filters
- **URL**: `base_url/analytics/dashboard`
- **Method**: `GET`
- **Headers**: 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Cookie**: None
- **Body**: None
- **Query Parameters**:
  ```
  ?user_id=1&platform_type=instagram&date_from=2025-01-01&date_to=2025-01-31&product_category=t-shirt
  ```
- **Response**:
  ```json
  {
    "stats": {
      "total_posts": 25,
      "scheduled_posts": 8,
      "published_posts": 15,
      "failed_posts": 2,
      "draft_posts": 0
    },
    "platform_breakdown": [
      {
        "platform": "instagram",
        "scheduled": 4,
        "published": 8,
        "failed": 1
      },
      {
        "platform": "twitter",
        "scheduled": 3,
        "published": 5,
        "failed": 1
      },
      {
        "platform": "facebook",
        "scheduled": 1,
        "published": 2,
        "failed": 0
      }
    ],
    "chart_data": [
      {
        "date": "2025-01-10",
        "scheduled": 2,
        "published": 1,
        "failed": 0
      },
      {
        "date": "2025-01-11",
        "scheduled": 1,
        "published": 3,
        "failed": 1
      },
      {
        "date": "2025-01-12",
        "scheduled": 3,
        "published": 2,
        "failed": 0
      }
    ],
    "ai_insights": [
      {
        "id": 1,
        "type": "performance",
        "title": "Best Posting Times",
        "insight": "Your Instagram posts perform 45% better when published between 2-4 PM on weekdays. Consider scheduling more content during this peak engagement window.",
        "confidence_score": 0.89,
        "generated_at": "2025-01-15T12:00:00Z"
      },
      {
        "id": 2,
        "type": "content",
        "title": "Content Strategy",
        "insight": "Posts featuring t-shirt products get 60% more engagement than other categories. Your audience shows strong preference for casual wear content.",
        "confidence_score": 0.92,
        "generated_at": "2025-01-15T12:00:00Z"
      },
      {
        "id": 3,
        "type": "hashtag",
        "title": "Hashtag Performance",
        "insight": "Using 5-7 hashtags generates optimal reach. Posts with #fashion and #style combination show 35% higher engagement rates.",
        "confidence_score": 0.76,
        "generated_at": "2025-01-15T12:00:00Z"
      }
    ],
    "period": {
      "from": "2025-01-01",
      "to": "2025-01-31"
    },
    "filters_applied": {
      "platform_type": "instagram",
      "product_category": "t-shirt"
    }
  }
  ```

---

## Common Data Models

### User Schema
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "profession": "Designer"
}
```

### Product Schema
```json
{
  "id": 2,
  "name": "Classic White T-Shirt",
  "category": "t-shirt",
  "price": 19.99,
  "image_path": "/images/products/tshirt_white.jpg"
}
```

### Error Response Schema
```json
{
  "error": {
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Email already exists"
      }
    ]
  }
}
```

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error