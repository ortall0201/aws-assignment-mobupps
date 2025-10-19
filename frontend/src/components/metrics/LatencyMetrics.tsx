import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MetricsData } from "@/pages/Metrics";

interface LatencyMetricsProps {
  metrics: MetricsData;
}

export const LatencyMetrics = ({ metrics }: LatencyMetricsProps) => {
  return (
    <Card className="shadow-glass border-border/50">
      <CardHeader>
        <CardTitle>Latency Statistics</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 font-semibold">Endpoint</th>
                <th className="text-right py-3 px-4 font-semibold">Avg</th>
                <th className="text-right py-3 px-4 font-semibold">Min</th>
                <th className="text-right py-3 px-4 font-semibold">Max</th>
                <th className="text-right py-3 px-4 font-semibold">P50</th>
                <th className="text-right py-3 px-4 font-semibold">P95</th>
                <th className="text-right py-3 px-4 font-semibold">P99</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(metrics.latency_stats).map(([endpoint, stats]) => (
                <tr key={endpoint} className="border-b border-border/50 hover:bg-muted/50 transition-colors">
                  <td className="py-3 px-4">
                    <code className="text-xs bg-muted px-2 py-1 rounded">{endpoint}</code>
                  </td>
                  <td className="text-right py-3 px-4 font-medium">{stats.avg.toFixed(1)}ms</td>
                  <td className="text-right py-3 px-4 text-success">{stats.min.toFixed(1)}ms</td>
                  <td className="text-right py-3 px-4 text-destructive">{stats.max.toFixed(1)}ms</td>
                  <td className="text-right py-3 px-4">{stats.p50.toFixed(1)}ms</td>
                  <td className="text-right py-3 px-4">{stats.p95.toFixed(1)}ms</td>
                  <td className="text-right py-3 px-4">{stats.p99.toFixed(1)}ms</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
};
