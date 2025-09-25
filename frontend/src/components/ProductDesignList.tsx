'use client';

import { useState, useEffect } from 'react';
import { Palette, Calendar, Eye } from 'lucide-react';
import { productApi } from '@/lib/api';
import { ProductDesignItem } from '@/types/api';
import { format } from 'date-fns';

export default function ProductDesignList() {
  const [designs, setDesigns] = useState<ProductDesignItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDesigns();
  }, []);

  const fetchDesigns = async () => {
    try {
      setLoading(true);
      const response = await productApi.listDesigns(1); // Using user_id = 1 for demo
      setDesigns(response.items);
      setError(null);
    } catch (err) {
      setError('Failed to fetch designs');
      console.error('Error fetching designs:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="animate-pulse space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="bg-gray-200 h-24 rounded-lg"></div>
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
            onClick={fetchDesigns}
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
        <h2 className="text-2xl font-bold text-gray-900">My Designs</h2>
        <p className="text-gray-600 mt-1">View and manage your product customizations</p>
      </div>

      {designs.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <Palette className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No designs created</h3>
          <p className="text-gray-600">Start customizing products to see your designs here!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {designs.map((design) => (
            <div key={design.id} className="bg-white rounded-lg shadow hover:shadow-md transition-shadow">
              {/* Preview Area */}
              <div className="p-6 bg-gray-50 rounded-t-lg">
                <div className="w-full h-40 bg-white rounded border-2 border-dashed border-gray-200 flex items-center justify-center relative">
                  {/* Mock t-shirt background */}
                  <div className="w-32 h-32 bg-gray-100 rounded border border-gray-300 flex items-center justify-center relative">
                    <span
                      style={{
                        fontSize: `${Math.max(design.text_size / 3, 8)}px`,
                        color: design.text_color,
                        position: 'absolute',
                        left: `${(design.text_position_x / 400) * 100}%`,
                        top: `${(design.text_position_y / 500) * 100}%`,
                        transform: 'translate(-50%, -50%)',
                        maxWidth: '120px',
                        textAlign: 'center',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap'
                      }}
                    >
                      {design.custom_text}
                    </span>
                  </div>
                </div>
              </div>

              {/* Design Info */}
              <div className="p-4">
                <h3 className="font-semibold text-gray-900 mb-2 truncate">
                  "{design.custom_text}"
                </h3>

                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center gap-2">
                    <Palette className="w-4 h-4" />
                    <span>Color: {design.text_color}</span>
                    <div
                      className="w-4 h-4 rounded border border-gray-300"
                      style={{ backgroundColor: design.text_color }}
                    ></div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Eye className="w-4 h-4" />
                    <span>Size: {design.text_size}px</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <Calendar className="w-4 h-4" />
                    <span>{format(new Date(design.created_at), 'MMM dd, yyyy')}</span>
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-gray-100">
                  <button
                    onClick={() => {
                      // You could implement a detailed view or edit functionality here
                      alert(`Design ID: ${design.id}\nPosition: (${design.text_position_x}, ${design.text_position_y})`);
                    }}
                    className="w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors text-sm"
                  >
                    View Details
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}