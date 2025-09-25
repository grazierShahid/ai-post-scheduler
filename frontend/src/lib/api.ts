import axios from 'axios';
import {
  PostSubmitRequest,
  PostListResponse,
  PostSummaryResponse,
  AiInsightResponse,
  ProductDesignCreateRequest,
  ProductDesignListResponse,
  AISuggestionsRequest,
  AISuggestionsResponse,
  AIBestTimeRequest,
  AIBestTimeResponse,
  PlatformType
} from '@/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  // Don't set default Content-Type - let axios set it based on request type
});

// Post endpoints
export const postApi = {
  submitPost: async (data: PostSubmitRequest, image?: File) => {
    const formData = new FormData();

    formData.append('user_id', data.user_id.toString());
    formData.append('content_text', data.content_text);

    data.platforms.forEach((platform) => {
      formData.append('platform_list', platform);
    });

    // Always send product_id (empty if not provided)
    if (data.product_id) {
      formData.append('product_id', data.product_id.toString());
    }

    // Always send schedule_time (empty if not provided)
    if (data.schedule_time) {
      formData.append('schedule_time', data.schedule_time);
    }

    // Always send hashtags
    formData.append('hashtags', data.hashtags.join(','));

    // Always send target_audience (empty if not provided)
    formData.append('target_audience', data.target_audience || '');

    // Always send call_to_action (empty if not provided)
    formData.append('call_to_action', data.call_to_action || '');

    formData.append('content_tone', data.content_tone);

    // Always send api_ids field (empty string if not provided)
    formData.append('api_ids', data.api_ids ? data.api_ids.join(',') : '');

    if (image) {
      formData.append('image', image);
    } else if (data.image_url) {
      formData.append('image_url', data.image_url);
    }

    return api.post('/submit-post', formData);
  },

  listPosts: async (limit = 20, offset = 0): Promise<PostListResponse> => {
    const response = await api.get(`/posts?limit=${limit}&offset=${offset}`);
    return response.data;
  },

  getPost: async (postId: number) => {
    const response = await api.get(`/post/${postId}`);
    return response.data;
  },

  suggestHashtags: async (data: AISuggestionsRequest): Promise<AISuggestionsResponse> => {
    const response = await api.post('/suggest-hashtag', data, {
      headers: { 'Content-Type': 'application/json' }
    });
    return response.data;
  },

  suggestBestTime: async (data: AIBestTimeRequest): Promise<AIBestTimeResponse> => {
    const response = await api.post('/suggest-best-time', data, {
      headers: { 'Content-Type': 'application/json' }
    });
    return response.data;
  },
};

// Analytics endpoints
export const analyticsApi = {
  getPostsSummary: async (
    userId?: number,
    platformType?: PlatformType,
    startDate?: string,
    endDate?: string
  ): Promise<PostSummaryResponse> => {
    const params = new URLSearchParams();
    if (userId) params.append('user_id', userId.toString());
    if (platformType) params.append('platform_type', platformType);
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);

    const response = await api.get(`/analytics/posts/summary?${params.toString()}`);
    return response.data;
  },

  getAiInsight: async (userId: number, query?: string): Promise<AiInsightResponse> => {
    const params = new URLSearchParams();
    params.append('user_id', userId.toString());
    if (query) params.append('query', query);

    const response = await api.get(`/analytics/ai-insight?${params.toString()}`);
    return response.data;
  },
};

// Product customization endpoints
export const productApi = {
  createDesign: async (data: ProductDesignCreateRequest) => {
    const response = await api.post('/product-customization/product-designs', data, {
      headers: { 'Content-Type': 'application/json' }
    });
    return response.data;
  },

  listDesigns: async (userId: number): Promise<ProductDesignListResponse> => {
    const response = await api.get(`/product-customization/product-designs?user_id=${userId}`);
    return response.data;
  },

  getDesign: async (designId: number) => {
    const response = await api.get(`/product-customization/product-designs/${designId}`);
    return response.data;
  },

  getProductImage: async (productId: number) => {
    const response = await api.get(`/product-customization/product-images/${productId}`);
    return response.data;
  },
};

export default api;