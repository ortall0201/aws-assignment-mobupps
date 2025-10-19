import { useForm } from "react-hook-form";
import { Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "@/hooks/use-toast";
import { PredictResponse } from "@/pages/Predict";
import { useState } from "react";
import { predictPerformance } from "@/lib/api";

interface PredictFormProps {
  onResults: (results: PredictResponse) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const PredictForm = ({ onResults, isLoading, setIsLoading }: PredictFormProps) => {
  const { register, handleSubmit, setValue } = useForm();
  const [abArm, setAbArm] = useState("v1");

  const onSubmit = async (data: any) => {
    setIsLoading(true);

    let neighbors = [];
    try {
      neighbors = JSON.parse(data.neighborResults || "[]");
      // Transform to backend format if needed
      neighbors = neighbors.map((n: any) => ({
        app_id: n.app_id,
        similarity: n.similarity_score || n.similarity || 0,
      }));
    } catch (e) {
      toast({
        title: "Invalid JSON",
        description: "Neighbor results must be valid JSON format: [{ \"app_id\": \"app_123\", \"similarity_score\": 0.95 }]",
        variant: "destructive",
      });
      setIsLoading(false);
      return;
    }

    const payload = {
      app: {
        name: data.appName || data.appId,
        category: data.category,
        region: data.region,
        pricing: data.pricingModel,
        features: data.features ? data.features.split(",").map((f: string) => f.trim()) : undefined,
      },
      neighbors,
      ab_arm: abArm,
    };

    try {
      const { data: result, correlationId } = await predictPerformance(payload);

      onResults({
        predicted_score: result.prediction.score,
        user_segments: result.prediction.segments,
        confidence: result.prediction.score, // Use score as confidence for now
        latency_ms: result.latency_ms,
        ab_arm: result.ab_arm,
        correlation_id: correlationId,
      });

      toast({
        title: "Prediction Complete",
        description: `Score: ${result.prediction.score.toFixed(2)} | Latency: ${result.latency_ms}ms`,
      });
    } catch (error) {
      toast({
        title: "Prediction Failed",
        description: error instanceof Error ? error.message : "Unable to complete prediction. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const exampleNeighbors = `[
  { "app_id": "app_123", "similarity_score": 0.95 },
  { "app_id": "app_456", "similarity_score": 0.87 }
]`;

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="appId">App ID</Label>
          <Input
            id="appId"
            {...register("appId", { required: true })}
            placeholder="app_456"
            className="bg-background"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="partnerId">Partner ID</Label>
          <Input
            id="partnerId"
            {...register("partnerId", { required: true })}
            placeholder="partner_789"
            className="bg-background"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="abArm">A/B Testing Arm</Label>
        <Select value={abArm} onValueChange={setAbArm}>
          <SelectTrigger className="bg-background">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="v1">Version 1 (v1)</SelectItem>
            <SelectItem value="v2">Version 2 (v2)</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="neighborResults">
          Neighbor Results (JSON)
          <span className="text-xs text-muted-foreground ml-2">
            Paste results from similarity search or manual input
          </span>
        </Label>
        <Textarea
          id="neighborResults"
          {...register("neighborResults", { required: true })}
          placeholder={exampleNeighbors}
          className="bg-background font-mono text-sm h-32"
        />
      </div>

      <Button type="submit" disabled={isLoading} className="w-full bg-gradient-primary hover:opacity-90">
        {isLoading ? (
          <>
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
            Predicting...
          </>
        ) : (
          <>
            <Zap className="w-4 h-4 mr-2" />
            Predict Performance
          </>
        )}
      </Button>
    </form>
  );
};
