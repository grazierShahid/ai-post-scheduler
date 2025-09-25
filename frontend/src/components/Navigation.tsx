'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Calendar, BarChart3, Palette, List, Home } from 'lucide-react';

const navigation = [
  { name: 'Home', href: '/', icon: Home },
  { name: 'Schedule Post', href: '/schedule', icon: Calendar },
  { name: 'My Posts', href: '/posts', icon: List },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Product Customizer', href: '/customizer', icon: Palette },
];

export default function Navigation() {
  const pathname = usePathname();

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between">
          <div className="flex space-x-8">
            {/* Logo */}
            <div className="flex items-center py-6">
              <span className="text-xl font-bold text-blue-600">SocialScheduler</span>
            </div>

            {/* Navigation items */}
            <div className="hidden md:flex items-center space-x-1">
              {navigation.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    <item.icon className="w-4 h-4 mr-2" />
                    {item.name}
                  </Link>
                );
              })}
            </div>
          </div>

          {/* User section */}
          <div className="hidden md:flex items-center">
            <div className="px-3 py-2 text-sm text-gray-600">
              Welcome, User!
            </div>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div className="md:hidden border-t border-gray-200">
        <div className="px-2 py-3 space-y-1">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center px-3 py-2 rounded-md text-base font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                <item.icon className="w-5 h-5 mr-3" />
                {item.name}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}