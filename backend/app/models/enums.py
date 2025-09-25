import enum

class UserRole(str, enum.Enum):
    Admin = "admin"
    Moderator = "moderator"
    General = "general"

class ImageType(str, enum.Enum):
    URL = "url"
    FILE = "file"

class ApiType(str, enum.Enum):
    OPENAI = "openai"
    GROK = "grok"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"

class ProductCategory(str, enum.Enum):
    SHIRT = "shirt"
    T_SHIRT = "t-shirt"
    PANT = "pant"
    JACKET = "jacket"
    HOODIE = "hoodie"
    DRESS = "dress"

class PostType(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    STORY = "story"
    REEL = "reel"

class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    PENDING = "pending"
    SCHEDULED = "scheduled"
    FAILED = "failed"

class PostTone(str, enum.Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FRIENDLY = "friendly"
    FORMAL = "formal"
    HUMOROUS = "humorous"

class PlatformType(str, enum.Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"

class PlatformStatus(str, enum.Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    EXPIRED = "expired"

class InsightType(str, enum.Enum):
    ENGAGEMENT = "engagement"
    TIMING = "timing"
    CONTENT = "content"
    HASHTAG = "hashtag"
    AUDIENCE = "audience"
    PERFORMANCE = "performance"
