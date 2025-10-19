import { useState } from "react";
import { Zap, TrendingUp } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { PredictForm } from "@/components/predict/PredictForm";
import { PredictResults } from "@/components/predict/PredictResults";

export interface PredictResponse {
  predicted_score: number;
  user_segments: string[];
  confidence: number;
  latency_ms: number;
  ab_arm: string;
  correlation_id: string;
}

const Predict = () => {
  const [results, setResults] = useState<PredictResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-4 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-effect">
            <Zap className="w-4 h-4 text-warning" />
            <span className="text-sm font-medium">Performance Prediction</span>
          </div>
          
          <h1 className="text-4xl md:text-5xl font-bold gradient-text">
            Predict App Performance
          </h1>
          
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Use machine learning to predict how your app will perform based on similar apps
            and user segments. Powered by A/B tested prediction models.
          </p>
        </div>

        {/* Prediction Form */}
        <Card className="shadow-glass border-border/50">
          <CardContent className="p-6">
            <PredictForm 
              onResults={setResults}
              isLoading={isLoading}
              setIsLoading={setIsLoading}
            />
          </CardContent>
        </Card>

        {/* Results */}
        {results && <PredictResults results={results} />}
      </div>
    </div>
  );
};

export default Predict;
