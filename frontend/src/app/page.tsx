import Link from 'next/link';
import { Calendar, BarChart3, Palette, ArrowRight, Sparkles, Shield, Zap } from 'lucide-react';

export default function HomePage() {
  const features = [
    {
      icon: Calendar,
      title: 'Smart Scheduling',
      description: 'Schedule posts across multiple social platforms with AI-suggested optimal timing',
      href: '/schedule',
      color: 'bg-blue-500',
    },
    {
      icon: BarChart3,
      title: 'Analytics Dashboard',
      description: 'Track your posting performance with detailed analytics and AI insights',
      href: '/analytics',
      color: 'bg-green-500',
    },
    {
      icon: Palette,
      title: 'Product Customizer',
      description: 'Design custom products with text overlays and preview them instantly',
      href: '/customizer',
      color: 'bg-purple-500',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <div className="mb-6">
          <span className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium mb-4">
            <Sparkles className="w-4 h-4 mr-2" />
            AI-Powered Social Media Management
          </span>
        </div>

        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Schedule, Analyze, and
          <span className="text-blue-600"> Optimize</span>
        </h1>

        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Streamline your social media workflow with our intelligent posting scheduler,
          comprehensive analytics, and custom product designer - all powered by AI.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/schedule"
            className="bg-blue-600 text-white px-8 py-4 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
          >
            Get Started
            <ArrowRight className="w-4 h-4" />
          </Link>

          <Link
            href="/analytics"
            className="border border-gray-300 text-gray-700 px-8 py-4 rounded-lg font-medium hover:bg-gray-50 transition-colors"
          >
            View Analytics
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-8 mb-16">
        {features.map((feature, index) => (
          <Link
            key={index}
            href={feature.href}
            className="group bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 p-8 border border-gray-200"
          >
            <div className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
              <feature.icon className="w-6 h-6 text-white" />
            </div>

            <h3 className="text-xl font-semibold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">
              {feature.title}
            </h3>

            <p className="text-gray-600 mb-4">
              {feature.description}
            </p>

            <div className="flex items-center text-blue-600 font-medium group-hover:gap-2 transition-all">
              Learn more
              <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>
        ))}
      </div>

      {/* Stats Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white mb-16">
        <div className="grid md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-3xl font-bold mb-2">99%</div>
            <div className="text-blue-100">Scheduling Accuracy</div>
          </div>
          <div>
            <div className="text-3xl font-bold mb-2">4+</div>
            <div className="text-blue-100">Social Platforms</div>
          </div>
          <div>
            <div className="text-3xl font-bold mb-2">AI</div>
            <div className="text-blue-100">Powered Insights</div>
          </div>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Why Choose SocialScheduler?
        </h2>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Zap className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Lightning Fast</h3>
            <p className="text-gray-600">Schedule posts across all platforms in seconds with our streamlined interface</p>
          </div>

          <div className="text-center">
            <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">AI-Powered</h3>
            <p className="text-gray-600">Get intelligent suggestions for hashtags, posting times, and content optimization</p>
          </div>

          <div className="text-center">
            <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Reliable</h3>
            <p className="text-gray-600">Never miss a scheduled post with our robust infrastructure and monitoring</p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-50 rounded-2xl p-8 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Ready to Transform Your Social Media Strategy?
        </h2>
        <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
          Join thousands of content creators and businesses who trust SocialScheduler
          to manage their social media presence effectively.
        </p>
        <Link
          href="/schedule"
          className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors inline-flex items-center gap-2"
        >
          Start Scheduling Now
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}
