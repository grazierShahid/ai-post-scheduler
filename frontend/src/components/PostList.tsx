'use client';

import { useState, useEffect } from 'react';
import { Calendar, Clock, Hash, Image as ImageIcon } from 'lucide-react';
import { postApi } from '@/lib/api';
import { PostListItem, PostStatus, PlatformType } from '@/types/api';
import { format } from 'date-fns';

export default function PostList() {
  const [posts, setPosts] = useState<PostListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await postApi.listPosts(20, 0);
      setPosts(response.posts);
      setError(null);
    } catch (err) {
      setError('Failed to fetch posts');
      console.error('Error fetching posts:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: PostStatus) => {
    const statusClasses = {
      [PostStatus.DRAFT]: 'bg-gray-100 text-gray-800',
      [PostStatus.SCHEDULED]: 'bg-blue-100 text-blue-800',
      [PostStatus.PUBLISHED]: 'bg-green-100 text-green-800',
      [PostStatus.FAILED]: 'bg-red-100 text-red-800',
      [PostStatus.PENDING]: 'bg-yellow-100 text-yellow-800',
    };

    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full capitalize ${statusClasses[status]}`}>
        {status}
      </span>
    );
  };

  const getPlatformBadges = (platforms: PlatformType[]) => {
    const platformColors = {
      [PlatformType.TWITTER]: 'bg-blue-500',
      [PlatformType.LINKEDIN]: 'bg-blue-700',
      [PlatformType.FACEBOOK]: 'bg-blue-600',
      [PlatformType.INSTAGRAM]: 'bg-pink-500',
    };

    return platforms.map((platform) => (
      <span
        key={platform}
        className={`px-2 py-1 text-xs font-medium text-white rounded capitalize ${platformColors[platform]}`}
      >
        {platform}
      </span>
    ));
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="animate-pulse space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="bg-gray-200 h-32 rounded-lg"></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
          <button
            onClick={fetchPosts}
            className="mt-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Scheduled Posts</h2>
        <p className="text-gray-600 mt-1">Manage your upcoming and published posts</p>
      </div>

      {posts.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No posts scheduled</h3>
          <p className="text-gray-600">Create your first post to get started!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {posts.map((post) => (
            <div key={post.id} className="bg-white rounded-lg shadow hover:shadow-md transition-shadow p-6">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="flex gap-2">
                    {getPlatformBadges(post.platforms)}
                  </div>
                  {getStatusBadge(post.status)}
                </div>
                <div className="flex items-center text-sm text-gray-500 gap-4">
                  {post.schedule_time && (
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {format(new Date(post.schedule_time), 'MMM dd, yyyy HH:mm')}
                    </div>
                  )}
                  <div className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    {format(new Date(post.created_at), 'MMM dd, yyyy')}
                  </div>
                </div>
              </div>

              <div className="flex gap-4">
                {post.image && (
                  <div className="flex-shrink-0">
                    <div className="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center">
                      <ImageIcon className="w-8 h-8 text-gray-400" />
                    </div>
                  </div>
                )}

                <div className="flex-1 min-w-0">
                  <p className="text-gray-900 mb-2 line-clamp-2">{post.content_text}</p>

                  {post.hashtags.length > 0 && (
                    <div className="flex items-center gap-1 text-sm text-blue-600">
                      <Hash className="w-3 h-3" />
                      <span className="truncate">
                        {post.hashtags.join(' ')}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}