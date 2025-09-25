'use client';

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Calendar, Clock, Hash, Target, Megaphone, Upload, Wand2, Link } from 'lucide-react';
import { postApi } from '@/lib/api';
import { PlatformType, PostTone, AISuggestionsRequest } from '@/types/api';

const postSchema = z.object({
  user_id: z.number().min(1),
  content_text: z.string().min(1, 'Content text is required'),
  platforms: z.array(z.nativeEnum(PlatformType)).min(1, 'Select at least one platform'),
  product_id: z.number().optional(),
  schedule_time: z.string().optional(),
  hashtags: z.string(),
  target_audience: z.string().optional(),
  call_to_action: z.string().optional(),
  content_tone: z.nativeEnum(PostTone),
  image_url: z.string().url({ message: "Please enter a valid URL" }).optional().or(z.literal('')),
});

type PostFormData = z.infer<typeof postSchema>;

export default function PostScheduler() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isGeneratingHashtags, setIsGeneratingHashtags] = useState(false);
  const [isGeneratingTime, setIsGeneratingTime] = useState(false);
  const [imageSource, setImageSource] = useState<'upload' | 'url'>('upload');

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<PostFormData>({
    resolver: zodResolver(postSchema),
    defaultValues: {
      user_id: 1,
      content_tone: PostTone.CASUAL,
      platforms: [],
      hashtags: '',
      image_url: '',
    },
  });

  const watchedPlatforms = watch('platforms');
  const watchedContentText = watch('content_text');
  const watchedImageUrl = watch('image_url');

  useEffect(() => {
    if (imageSource === 'url' && watchedImageUrl) {
      setImagePreview(watchedImageUrl);
    }
  }, [watchedImageUrl, imageSource]);

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = () => setImagePreview(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const togglePlatform = (platform: PlatformType) => {
    const currentPlatforms = watchedPlatforms || [];
    const updatedPlatforms = currentPlatforms.includes(platform)
      ? currentPlatforms.filter((p) => p !== platform)
      : [...currentPlatforms, platform];
    setValue('platforms', updatedPlatforms);
  };

  const generateHashtags = async () => {
    if (!watchedContentText?.trim()) {
      alert('Please enter some content text first');
      return;
    }

    setIsGeneratingHashtags(true);
    try {
      const request: AISuggestionsRequest = {
        user_id: 1,
        content_text: watchedContentText,
        platform_types: watchedPlatforms || [PlatformType.TWITTER],
        brand_tone: watch('content_tone'),
        target_audience: watch('target_audience'),
      };

      const response = await postApi.suggestHashtags(request);
      const hashtags = response.hashtag_suggestions.join(', ');
      setValue('hashtags', hashtags);
    } catch (error) {
      console.error('Error generating hashtags:', error);
      alert('Failed to generate hashtags. Please try again.');
    } finally {
      setIsGeneratingHashtags(false);
    }
  };

  const generateBestTime = async () => {
    if (watchedPlatforms.length === 0) {
      alert('Please select at least one platform first');
      return;
    }

    setIsGeneratingTime(true);
    try {
      const request: AIBestTimeRequest = {
        user_id: 1,
        platform_types: watchedPlatforms,
        target_audience: watch('target_audience'),
      };

      const response = await postApi.suggestBestTime(request);
      const suggestions = response.suggestions.join('\n- ');
      alert(`AI-Suggested Best Times to Post:\n- ${suggestions}`);
    } catch (error) {
      console.error('Error generating best time:', error);
      alert('Failed to generate best time suggestions. Please try again.');
    } finally {
      setIsGeneratingTime(false);
    }
  };

  const onSubmit = async (data: PostFormData) => {
    setIsSubmitting(true);
    try {
      // Create a submission-specific data object to avoid mutating the form state
      const submissionData = {
        ...data,
        hashtags: data.hashtags.split(',').map((h) => h.trim()).filter(Boolean),
        // Convert schedule_time to UTC ISO string for the submission only
        schedule_time: data.schedule_time ? new Date(data.schedule_time).toISOString() : undefined,
      };

      const imageFile = imageSource === 'upload' ? selectedImage || undefined : undefined;
      
      if (imageSource === 'url') {
        submissionData.image_url = watchedImageUrl;
      } else {
        submissionData.image_url = '';
      }

      const response = await postApi.submitPost(submissionData, imageFile);
      console.log('Post submission response:', response.data);
      alert('Post scheduled successfully!');

      // Reset form
      setSelectedImage(null);
      setImagePreview(null);
      setValue('image_url', '');
    } catch (error: any) {
      console.error('Error submitting post:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      alert('Failed to schedule post. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Schedule Social Media Post</h2>
        <p className="text-gray-600 mt-1">Create and schedule your post across multiple platforms</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Content Text */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Megaphone className="inline w-4 h-4 mr-1" />
            Post Content
          </label>
          <textarea
            {...register('content_text')}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900"
            placeholder="What would you like to share?"
          />
          {errors.content_text && (
            <p className="text-red-500 text-sm mt-1">{errors.content_text.message}</p>
          )}
        </div>

        {/* Image Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Image (Optional)
          </label>
          <div className="flex border border-gray-300 rounded-md mb-2">
            <button
              type="button"
              onClick={() => setImageSource('upload')}
              className={`flex-1 p-2 text-sm rounded-l-md flex items-center justify-center gap-2 ${
                imageSource === 'upload' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Upload className="w-4 h-4" />
              Upload File
            </button>
            <button
              type="button"
              onClick={() => setImageSource('url')}
              className={`flex-1 p-2 text-sm rounded-r-md flex items-center justify-center gap-2 ${
                imageSource === 'url' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Link className="w-4 h-4" />
              From URL
            </button>
          </div>

          {imageSource === 'upload' ? (
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900"
            />
          ) : (
            <input
              type="text"
              {...register('image_url')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900"
              placeholder="https://example.com/image.jpg"
            />
          )}
          {errors.image_url && (
            <p className="text-red-500 text-sm mt-1">{errors.image_url.message}</p>
          )}

          {imagePreview && (
            <div className="mt-2">
              <img
                src={imagePreview}
                alt="Preview"
                className="w-32 h-32 object-cover rounded-md"
              />
            </div>
          )}
        </div>

        {/* Platforms */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Platforms
          </label>
          <div className="flex flex-wrap gap-2">
            {Object.values(PlatformType).map((platform) => (
              <button
                key={platform}
                type="button"
                onClick={() => togglePlatform(platform)}
                className={`px-4 py-2 rounded-md text-sm font-medium capitalize transition-colors ${
                  watchedPlatforms?.includes(platform)
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {platform}
              </button>
            ))}
          </div>
          {errors.platforms && (
            <p className="text-red-500 text-sm mt-1">{errors.platforms.message}</p>
          )}
        </div>

        {/* Schedule Time */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Clock className="inline w-4 h-4 mr-1" />
            Schedule Time (Optional)
          </label>
          <div className="flex gap-2">
            <input
              type="datetime-local"
              {...register('schedule_time')}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900"
            />
            <button
              type="button"
              onClick={generateBestTime}
              disabled={isGeneratingTime}
              className="px-4 py-2 bg-teal-500 text-white rounded-md hover:bg-teal-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-1"
            >
              <Wand2 className="w-4 h-4" />
              {isGeneratingTime ? 'Suggesting...' : 'Suggest Time'}
            </button>
          </div>
        </div>

        {/* Hashtags */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Hash className="inline w-4 h-4 mr-1" />
            Hashtags
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              {...register('hashtags')}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900"
              placeholder="Enter hashtags separated by commas"
            />
            <button
              type="button"
              onClick={generateHashtags}
              disabled={isGeneratingHashtags}
              className="px-4 py-2 bg-purple-500 text-white rounded-md hover:bg-purple-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-1"
            >
              <Wand2 className="w-4 h-4" />
              {isGeneratingHashtags ? 'Generating...' : 'AI Generate'}
            </button>
          </div>
        </div>

        {/* Target Audience */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Target className="inline w-4 h-4 mr-1" />
            Target Audience (Optional)
          </label>
          <input
            type="text"
            {...register('target_audience')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900"
            placeholder="e.g., Tech enthusiasts, Marketing professionals"
          />
        </div>

        {/* Call to Action */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Call to Action (Optional)
          </label>
          <input
            type="text"
            {...register('call_to_action')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900"
            placeholder="e.g., Visit our website, Sign up now"
          />
        </div>

        {/* Content Tone */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Content Tone
          </label>
          <select
            {...register('content_tone')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900"
          >
            {Object.values(PostTone).map((tone) => (
              <option key={tone} value={tone} className="capitalize">
                {tone}
              </option>
            ))}
          </select>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-blue-500 text-white py-3 px-4 rounded-md font-medium hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <Calendar className="w-4 h-4" />
          {isSubmitting ? 'Scheduling...' : 'Schedule Post'}
        </button>
      </form>
    </div>
  );
}