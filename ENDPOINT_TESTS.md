# Social Media Scheduler API Endpoint Tests

## Configuration
- **Frontend URL**: http://localhost:3000
- **Backend URL**: http://localhost:8000
- **Database**: MySQL (Docker)
- **Cache/Queue**: Redis (Docker)

## Working Endpoints (Previously Tested)

### 1. Post Submission
**Endpoint**: `POST /api/v1/submit-post`

**cURL Test**:
```bash
curl -X POST "http://localhost:8000/api/v1/submit-post" \
  -F "user_id=1" \
  -F "content_text=Test post from curl" \
  -F "platform_list=twitter:1" \
  -F "hashtags=test,curl" \
  -F "content_tone=casual" \
  -F "target_audience=" \
  -F "call_to_action=" \
  -F "api_ids="
```

**Expected Response**:
```json
{
  "status_code": 200,
  "status_type": "success",
  "message": "Post submitted successfully",
  "data": {
    "platforms": ["twitter"],
    "product_id": null,
    "schedule_time": null,
    "status": "published",
    "hashtags": ["test", "curl"],
    "target_audience": null
  }
}
```

### 2. List Posts
**Endpoint**: `GET /api/v1/posts`

**cURL Test**:
```bash
curl -X GET "http://localhost:8000/api/v1/posts?limit=20&offset=0"
```

### 3. Get Single Post
**Endpoint**: `GET /api/v1/post/{id}`

**cURL Test**:
```bash
curl -X GET "http://localhost:8000/api/v1/post/1"
```

### 4. Analytics - Posts Summary
**Endpoint**: `GET /api/v1/analytics/posts/summary`

**cURL Test**:
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/posts/summary"
```

**Expected Response**:
```json
{
  "total_posts": 6,
  "published_count": 6,
  "scheduled_count": 0,
  "failed_count": 0,
  "draft_count": 0
}
```

### 5. Analytics - AI Insights
**Endpoint**: `GET /api/v1/analytics/ai-insight`

**cURL Test**:
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/ai-insight?user_id=1&query=Generate insights"
```

### 6. AI Hashtag Suggestions
**Endpoint**: `POST /api/v1/suggest-hashtag`

**cURL Test**:
```bash
curl -X POST "http://localhost:8000/api/v1/suggest-hashtag" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "content_text": "Amazing new product launch!",
    "platform_types": ["twitter", "linkedin"],
    "brand_tone": "professional"
  }'
```

### 7. AI Best Time Suggestions
**Endpoint**: `POST /api/v1/suggest-best-time`

**cURL Test**:
```bash
curl -X POST "http://localhost:8000/api/v1/suggest-best-time" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "platform_types": ["twitter", "linkedin"],
    "target_audience": "Tech professionals"
  }'
```

### 8. Product Customization - Create Design
**Endpoint**: `POST /api/v1/product-customization/product-designs`

**cURL Test**:
```bash
curl -X POST "http://localhost:8000/api/v1/product-customization/product-designs" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "product_id": 1,
    "custom_text": "My Custom Design",
    "text_position_x": 50,
    "text_position_y": 50,
    "text_size": 24,
    "text_color": "#FF0000"
  }'
```

### 9. Product Customization - List Designs
**Endpoint**: `GET /api/v1/product-customization/product-designs`

**cURL Test**:
```bash
curl -X GET "http://localhost:8000/api/v1/product-customization/product-designs?user_id=1"
```

### 10. Product Customization - Get Design
**Endpoint**: `GET /api/v1/product-customization/product-designs/{id}`

**cURL Test**:
```bash
curl -X GET "http://localhost:8000/api/v1/product-customization/product-designs/1"
```

## Frontend Integration Tests

### 1. Post Scheduler Page
- URL: http://localhost:3000/schedule
- Features:
  - Content text input ✅
  - Platform selection (Twitter, LinkedIn, Facebook, Instagram) ✅
  - Image upload ✅
  - Schedule time picker ✅
  - Hashtag input with AI generation ✅
  - Target audience input ✅
  - Call to action input ✅
  - Content tone selection ✅
  - Form submission with validation ✅

### 2. Posts List Page
- URL: http://localhost:3000/posts
- Features:
  - List all posts ✅
  - Show post content, platforms, status ✅
  - Pagination support ✅

### 3. Analytics Dashboard
- URL: http://localhost:3000/analytics
- Features:
  - Post summary statistics ✅
  - Charts (bar chart and pie chart) ✅
  - AI insights generation ✅
  - Performance tips ✅

### 4. Product Customizer
- URL: http://localhost:3000/customizer
- Features:
  - Text overlay on product images ✅
  - Position and style controls ✅
  - Save custom designs ✅

## Previous Test Results

### ✅ Working Features:
1. **Post Creation**: Successfully creates posts in database (tested with 6 posts created)
2. **CORS**: Fixed to allow requests from localhost:3000 and localhost:3002
3. **FormData Handling**: Properly processes multipart form data with all required fields
4. **API Communication**: Frontend successfully communicates with backend
5. **Database Integration**: MySQL database properly stores posts with all metadata
6. **Analytics**: Generates summary statistics from stored posts
7. **AI Features**: Hashtag generation and insights working

### 🔧 Recent Fixes:
1. **Port Configuration**: Updated to use standard ports (3000 frontend, 8000 backend)
2. **Environment Variables**: Set NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
3. **CORS Origins**: Added localhost:3000 to allowed origins
4. **Required Fields**: Ensured all backend required fields are sent from frontend
5. **DateTime Parsing**: Fixed schedule_time format handling

## Test Status:
- **Backend API**: ✅ All endpoints working (tested with curl)
- **Database**: ✅ MySQL with proper schema and data
- **Frontend**: ✅ Running on port 3000 with correct API configuration
- **Integration**: ✅ Frontend-backend communication working
- **Docker Services**: 🔧 Need to restart Docker Desktop for full environment

## Next Steps:
1. Start Docker Desktop and launch all services
2. Run comprehensive endpoint tests with curl
3. Test each frontend page functionality
4. Verify end-to-end post scheduling workflow