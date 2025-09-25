'use client';

import { useState, useRef, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Palette, Type, Move, Save } from 'lucide-react';
import { productApi } from '@/lib/api';
import { ProductDesignCreateRequest } from '@/types/api';

interface CustomizerFormData {
  user_id: number;
  product_id: number;
  custom_text: string;
  text_size: number;
  text_color: string;
}

export default function ProductCustomizer() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [textPosition, setTextPosition] = useState({ x: 100, y: 100 });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<CustomizerFormData>({
    defaultValues: {
      user_id: 1,
      product_id: 1,
      custom_text: 'Your Text Here',
      text_size: 24,
      text_color: '#000000',
    },
  });

  const watchedText = watch('custom_text');
  const watchedSize = watch('text_size');
  const watchedColor = watch('text_color');

  const drawCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw mock t-shirt background
    ctx.fillStyle = '#f3f4f6';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw t-shirt shape (simple rectangle for demo)
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(50, 50, canvas.width - 100, canvas.height - 100);
    ctx.strokeStyle = '#d1d5db';
    ctx.strokeRect(50, 50, canvas.width - 100, canvas.height - 100);

    // Draw custom text
    ctx.font = `${watchedSize}px Arial`;
    ctx.fillStyle = watchedColor;
    ctx.textAlign = 'center';
    ctx.fillText(watchedText || 'Your Text Here', textPosition.x, textPosition.y);

    // Draw drag handle
    ctx.strokeStyle = '#3b82f6';
    ctx.setLineDash([5, 5]);
    const textMetrics = ctx.measureText(watchedText || 'Your Text Here');
    const textWidth = textMetrics.width;
    ctx.strokeRect(
      textPosition.x - textWidth / 2 - 5,
      textPosition.y - watchedSize - 5,
      textWidth + 10,
      watchedSize + 10
    );
    ctx.setLineDash([]);
  };

  useEffect(() => {
    drawCanvas();
  }, [watchedText, watchedSize, watchedColor, textPosition]);

  const handleMouseDown = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Check if click is near text
    const textMetrics = canvas.getContext('2d')?.measureText(watchedText || 'Your Text Here');
    if (!textMetrics) return;

    const textWidth = textMetrics.width;
    if (
      x >= textPosition.x - textWidth / 2 - 5 &&
      x <= textPosition.x + textWidth / 2 + 5 &&
      y >= textPosition.y - watchedSize - 5 &&
      y <= textPosition.y + 5
    ) {
      setIsDragging(true);
    }
  };

  const handleMouseMove = (event: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDragging) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    setTextPosition({ x, y });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const onSubmit = async (data: CustomizerFormData) => {
    setIsSubmitting(true);
    try {
      const designData: ProductDesignCreateRequest = {
        user_id: data.user_id,
        product_id: data.product_id,
        custom_text: data.custom_text,
        text_position_x: textPosition.x,
        text_position_y: textPosition.y,
        text_size: data.text_size,
        text_color: data.text_color,
      };

      await productApi.createDesign(designData);
      alert('Design saved successfully!');
    } catch (error) {
      console.error('Error saving design:', error);
      alert('Failed to save design. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Product Customizer</h2>
        <p className="text-gray-600 mt-1">Design your custom t-shirt with text overlay</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Canvas Area */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Product Preview</h3>
          <div className="border border-gray-200 rounded-lg p-4">
            <canvas
              ref={canvasRef}
              width={400}
              height={500}
              className="w-full max-w-md mx-auto cursor-move"
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onMouseLeave={handleMouseUp}
            />
          </div>
          <p className="text-sm text-gray-500 mt-2 text-center">
            <Move className="inline w-4 h-4 mr-1" />
            Click and drag the text to reposition it
          </p>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Customization Options</h3>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Text Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Type className="inline w-4 h-4 mr-1" />
                Custom Text
              </label>
              <input
                type="text"
                {...register('custom_text', { required: 'Text is required' })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                placeholder="Enter your custom text"
              />
              {errors.custom_text && (
                <p className="text-red-500 text-sm mt-1">{errors.custom_text.message}</p>
              )}
            </div>

            {/* Text Size */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Text Size: {watchedSize}px
              </label>
              <input
                type="range"
                min="12"
                max="48"
                {...register('text_size')}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>

            {/* Text Color */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Palette className="inline w-4 h-4 mr-1" />
                Text Color
              </label>
              <div className="flex items-center gap-3">
                <input
                  type="color"
                  {...register('text_color')}
                  className="w-12 h-10 border border-gray-300 rounded cursor-pointer"
                />
                <span className="text-sm text-gray-600">{watchedColor}</span>
              </div>
            </div>

            {/* Position Info */}
            <div className="bg-gray-50 p-4 rounded-md">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Text Position</h4>
              <p className="text-sm text-gray-600">
                X: {Math.round(textPosition.x)}, Y: {Math.round(textPosition.y)}
              </p>
            </div>

            {/* Save Button */}
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-blue-500 text-white py-3 px-4 rounded-md font-medium hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <Save className="w-4 h-4" />
              {isSubmitting ? 'Saving...' : 'Save Design'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}