import { useState } from "react";
import { useForm } from "react-hook-form";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { toast } from "@/hooks/use-toast";
import { SearchResponse } from "@/pages/Search";
import { findSimilarApps } from "@/lib/api";

interface SearchFormProps {
  onResults: (results: SearchResponse) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

const categories = [
  "Games",
  "Health & Fitness",
  "Social",
  "Productivity",
  "Finance",
  "Education",
  "Entertainment",
];

const regions = ["US", "UK", "EU", "APAC", "Global"];
const pricingModels = ["free", "freemium", "paid", "subscription"];
const availableFeatures = ["sharing", "tracking", "notifications", "offline", "social", "analytics"];

export const SearchForm = ({ onResults, isLoading, setIsLoading }: SearchFormProps) => {
  const [topK, setTopK] = useState(20);
  const [selectedFeatures, setSelectedFeatures] = useState<string[]>([]);
  const { register, handleSubmit, setValue, watch } = useForm();

  const onSubmit = async (data: any) => {
    setIsLoading(true);

    // Build payload in backend-expected format
    const payload = {
      app: {
        name: data.appName,
        category: data.category,
        region: data.region,
        pricing: data.pricingModel,
        features: selectedFeatures.length > 0 ? selectedFeatures : undefined,
      },
      filters: data.category || data.region ? {
        ...(data.category ? { category: [data.category] } : {}),
        ...(data.region ? { region: [data.region] } : {}),
      } : undefined,
      top_k: topK,
      partner_id: data.partnerId || undefined,
      app_id: data.appId || undefined,
    };

    try {
      const { data: result, correlationId } = await findSimilarApps(payload);

      // Transform backend response to UI format
      const similarApps = result.neighbors.map(neighbor => ({
        app_id: neighbor.app_id,
        app_name: neighbor.app_name || neighbor.app_id, // Use real app name from backend
        category: neighbor.category || "Unknown", // Use real category from backend
        similarity_score: neighbor.similarity,
      }));

      onResults({
        ab_arm: result.ab_arm,
        similar_apps: similarApps,
        correlation_id: correlationId,
      }, payload.app);

      // Save to history
      const history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
      history.unshift({ ...payload.app, timestamp: new Date().toISOString() });
      localStorage.setItem("searchHistory", JSON.stringify(history.slice(0, 10)));

      toast({
        title: "Search Complete",
        description: `Found ${similarApps.length} similar apps using ${result.ab_arm}`,
      });
    } catch (error) {
      toast({
        title: "Search Failed",
        description: error instanceof Error ? error.message : "Unable to complete search. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const toggleFeature = (feature: string) => {
    setSelectedFeatures(prev =>
      prev.includes(feature) ? prev.filter(f => f !== feature) : [...prev, feature]
    );
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="appName">App Name</Label>
          <Input
            id="appName"
            {...register("appName", { required: true })}
            placeholder="e.g., Fitness Tracker Pro"
            className="bg-background"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="category">Category</Label>
          <Select onValueChange={(value) => setValue("category", value)}>
            <SelectTrigger className="bg-background">
              <SelectValue placeholder="Select category" />
            </SelectTrigger>
            <SelectContent>
              {categories.map((cat) => (
                <SelectItem key={cat} value={cat}>
                  {cat}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="region">Region</Label>
          <Select onValueChange={(value) => setValue("region", value)}>
            <SelectTrigger className="bg-background">
              <SelectValue placeholder="Select region" />
            </SelectTrigger>
            <SelectContent>
              {regions.map((region) => (
                <SelectItem key={region} value={region}>
                  {region}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="pricingModel">Pricing Model</Label>
          <Select onValueChange={(value) => setValue("pricingModel", value)}>
            <SelectTrigger className="bg-background">
              <SelectValue placeholder="Select pricing" />
            </SelectTrigger>
            <SelectContent>
              {pricingModels.map((model) => (
                <SelectItem key={model} value={model}>
                  {model}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="partnerId">Partner ID (Optional)</Label>
          <Input
            id="partnerId"
            {...register("partnerId")}
            placeholder="partner_123"
            className="bg-background"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="appId">App ID (Optional)</Label>
          <Input
            id="appId"
            {...register("appId")}
            placeholder="app_456"
            className="bg-background"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label>Features (Optional)</Label>
        <div className="flex flex-wrap gap-2">
          {availableFeatures.map((feature) => (
            <button
              key={feature}
              type="button"
              onClick={() => toggleFeature(feature)}
              className={`px-3 py-1 rounded-full text-sm transition-all ${
                selectedFeatures.includes(feature)
                  ? "bg-primary text-primary-foreground shadow-md"
                  : "bg-muted text-muted-foreground hover:bg-muted/80"
              }`}
            >
              {feature}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-2">
        <Label>Top K Results: {topK}</Label>
        <Slider
          value={[topK]}
          onValueChange={([value]) => setTopK(value)}
          min={5}
          max={50}
          step={5}
          className="w-full"
        />
      </div>

      <Button type="submit" disabled={isLoading} className="w-full bg-gradient-primary hover:opacity-90">
        {isLoading ? (
          <>
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
            Searching...
          </>
        ) : (
          <>
            <Search className="w-4 h-4 mr-2" />
            Find Similar Apps
          </>
        )}
      </Button>
    </form>
  );
};
