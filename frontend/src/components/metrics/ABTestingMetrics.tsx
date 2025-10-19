import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { MetricsData } from "@/pages/Metrics";

interface ABTestingMetricsProps {
  metrics: MetricsData;
}

export const ABTestingMetrics = ({ metrics }: ABTestingMetricsProps) => {
  const totalAB = metrics.ab_testing.v1_count + metrics.ab_testing.v2_count;
  const v1Percentage = totalAB > 0 ? (metrics.ab_testing.v1_count / totalAB) * 100 : 50;
  const v2Percentage = totalAB > 0 ? (metrics.ab_testing.v2_count / totalAB) * 100 : 50;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card className="shadow-glass border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <span>A/B Traffic Split</span>
            <Badge variant="outline">Live</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Badge className="bg-success">V1</Badge>
                <span className="text-sm text-muted-foreground">
                  {metrics.ab_testing.v1_count.toLocaleString()} requests
                </span>
              </div>
              <span className="font-semibold">{v1Percentage.toFixed(1)}%</span>
            </div>
            <Progress value={v1Percentage} className="h-3 bg-success/20" />
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Badge className="bg-primary">V2</Badge>
                <span className="text-sm text-muted-foreground">
                  {metrics.ab_testing.v2_count.toLocaleString()} requests
                </span>
              </div>
              <span className="font-semibold">{v2Percentage.toFixed(1)}%</span>
            </div>
            <Progress value={v2Percentage} className="h-3" />
          </div>
        </CardContent>
      </Card>

      <Card className="shadow-glass border-border/50">
        <CardHeader>
          <CardTitle>A/B Split by Endpoint</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Object.entries(metrics.ab_testing.by_endpoint).map(([endpoint, counts]) => {
              const total = counts.v1 + counts.v2;
              const v1Pct = total > 0 ? (counts.v1 / total) * 100 : 50;
              
              return (
                <div key={endpoint} className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <code className="text-xs bg-muted px-2 py-1 rounded">{endpoint}</code>
                    <div className="flex gap-3 text-xs">
                      <span className="text-success">V1: {counts.v1}</span>
                      <span className="text-primary">V2: {counts.v2}</span>
                    </div>
                  </div>
                  <div className="flex gap-1 h-2 rounded-full overflow-hidden bg-muted">
                    <div 
                      className="bg-success transition-all" 
                      style={{ width: `${v1Pct}%` }}
                    />
                    <div 
                      className="bg-primary transition-all" 
                      style={{ width: `${100 - v1Pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
