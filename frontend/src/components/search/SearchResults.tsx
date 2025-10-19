import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { SearchResponse } from "@/pages/Search";
import { ChevronDown, ChevronUp, Zap } from "lucide-react";
import { useState } from "react";
import { predictPerformance } from "@/lib/api";
import { toast } from "@/hooks/use-toast";

interface SearchResultsProps {
  results: SearchResponse;
  appData?: any; // Original app search data
}

export const SearchResults = ({ results, appData }: SearchResultsProps) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
  const [isPredicting, setIsPredicting] = useState(false);
  const [prediction, setPrediction] = useState<any>(null);

  const handlePredict = async () => {
    setIsPredicting(true);
    try {
      const neighbors = results.similar_apps.map(app => ({
        app_id: app.app_id,
        similarity: app.similarity_score,
      }));

      const { data: result } = await predictPerformance({
        app: appData || { name: "Search App" },
        neighbors,
        ab_arm: results.ab_arm,
      });

      setPrediction(result);
      toast({
        title: "Prediction Complete",
        description: `Score: ${result.prediction.score.toFixed(2)} | Latency: ${result.latency_ms}ms`,
      });
    } catch (error) {
      toast({
        title: "Prediction Failed",
        description: error instanceof Error ? error.message : "Unable to predict",
        variant: "destructive",
      });
    } finally {
      setIsPredicting(false);
    }
  };

  return (
    <div className="space-y-4 animate-slide-up">
      <Card className="shadow-glass border-border/50">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Search Results</CardTitle>
            <div className="flex items-center gap-2">
              <Badge variant={results.ab_arm === "v1" ? "default" : "secondary"}>
                A/B Arm: {results.ab_arm}
              </Badge>
              <span className="text-sm text-muted-foreground">
                ID: {results.correlation_id}
              </span>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground mb-4">
            Found {results.similar_apps?.length || 0} similar apps
          </p>

          <div className="space-y-3">
            {results.similar_apps?.map((app, index) => (
              <Card
                key={index}
                className="cursor-pointer hover:shadow-md transition-all"
                onClick={() => setExpandedIndex(expandedIndex === index ? null : index)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 space-y-2">
                      <div className="flex items-center gap-2">
                        <h3 className="font-semibold">{app.app_name}</h3>
                        <Badge variant="outline" className="text-xs">
                          {app.category}
                        </Badge>
                      </div>
                      
                      <div className="space-y-1">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-muted-foreground">Similarity</span>
                          <span className="font-medium text-primary">
                            {(app.similarity_score * 100).toFixed(1)}%
                          </span>
                        </div>
                        <Progress value={app.similarity_score * 100} className="h-2" />
                      </div>

                      {expandedIndex === index && (
                        <div className="pt-2 border-t border-border/50 space-y-1 text-sm">
                          <div className="flex justify-between">
                            <span className="text-muted-foreground">App ID:</span>
                            <span className="font-mono">{app.app_id}</span>
                          </div>
                        </div>
                      )}
                    </div>

                    <button type="button" className="text-muted-foreground hover:text-foreground">
                      {expandedIndex === index ? (
                        <ChevronUp className="w-5 h-5" />
                      ) : (
                        <ChevronDown className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Predict Performance Button */}
          <div className="mt-6 pt-6 border-t border-border/50">
            <Button
              onClick={handlePredict}
              disabled={isPredicting}
              className="w-full bg-gradient-primary hover:opacity-90"
            >
              {isPredicting ? (
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
          </div>
        </CardContent>
      </Card>

      {/* Prediction Results */}
      {prediction && (
        <Card className="shadow-glass border-border/50 animate-slide-up">
          <CardHeader>
            <CardTitle>Performance Prediction</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground">Predicted Score</p>
                <p className="text-3xl font-bold gradient-text">{prediction.prediction.score.toFixed(2)}</p>
              </div>
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground">Latency</p>
                <p className="text-xl font-semibold">{prediction.latency_ms}ms</p>
              </div>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Target Segments</p>
              <div className="flex flex-wrap gap-2">
                {prediction.prediction.segments.map((segment: string, idx: number) => (
                  <Badge key={idx} variant="outline">{segment}</Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
