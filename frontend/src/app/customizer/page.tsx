import ProductCustomizer from '@/components/ProductCustomizer';
import ProductDesignList from '@/components/ProductDesignList';

export default function CustomizerPage() {
  return (
    <div className="container mx-auto py-8 space-y-8">
      <ProductCustomizer />
      <ProductDesignList />
    </div>
  );
}