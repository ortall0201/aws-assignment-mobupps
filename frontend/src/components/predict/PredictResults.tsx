import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { PredictResponse } from "@/pages/Predict";
import { Clock, Target, Users } from "lucide-react";

interface PredictResultsProps {
  results: PredictResponse;
}

export const PredictResults = ({ results }: PredictResultsProps) => {
  const scorePercentage = (results.predicted_score / 5) * 100;
  const confidencePercentage = results.confidence * 100;

  return (
    <div className="space-y-6 animate-slide-up">
      <Card className="shadow-glass border-border/50">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Prediction Results</CardTitle>
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
        <CardContent className="space-y-6">
          {/* Predicted Score Gauge */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Target className="w-5 h-5 text-primary" />
                <span className="font-semibold">Predicted Score</span>
              </div>
              <span className="text-3xl font-bold gradient-text">
                {results.predicted_score.toFixed(2)}
              </span>
            </div>
            <Progress value={scorePercentage} className="h-4" />
            <p className="text-sm text-muted-foreground">
              Out of 5.0 maximum score
            </p>
          </div>

          {/* Confidence */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-semibold">Confidence Level</span>
              <span className="text-xl font-bold text-success">
                {confidencePercentage.toFixed(1)}%
              </span>
            </div>
            <Progress value={confidencePercentage} className="h-3 bg-success/20" />
          </div>

          {/* User Segments */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Users className="w-5 h-5 text-accent" />
              <span className="font-semibold">Target User Segments</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {results.user_segments.map((segment, index) => (
                <Badge key={index} variant="outline" className="bg-accent/10 text-accent border-accent/30">
                  {segment}
                </Badge>
              ))}
            </div>
          </div>

          {/* Latency */}
          <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">Prediction Latency</span>
            </div>
            <span className="font-mono text-sm font-semibold">{results.latency_ms}ms</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
