import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { BarChart3, RefreshCw, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MetricsOverview } from "@/components/metrics/MetricsOverview";
import { ABTestingMetrics } from "@/components/metrics/ABTestingMetrics";
import { LatencyMetrics } from "@/components/metrics/LatencyMetrics";
import { toast } from "@/hooks/use-toast";

export interface MetricsData {
  total_requests: number;
  avg_latency_ms: number;
  requests_by_endpoint: Record<string, number>;
  status_codes: Record<string, number>;
  ab_testing: {
    v1_count: number;
    v2_count: number;
    by_endpoint: Record<string, { v1: number; v2: number }>;
  };
  latency_stats: Record<string, {
    avg: number;
    min: number;
    max: number;
    p50: number;
    p95: number;
    p99: number;
  }>;
  uptime_seconds: number;
}

const Metrics = () => {
  const [refreshInterval, setRefreshInterval] = useState<number | false>(false);

  const { data: metrics, isLoading, refetch } = useQuery<MetricsData>({
    queryKey: ["metrics"],
    queryFn: async () => {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}/metrics`);
      if (!response.ok) throw new Error("Failed to fetch metrics");
      const backendData = await response.json();

      // Transform backend metrics to UI format
      return {
        total_requests: backendData.requests.total,
        avg_latency_ms: Object.values(backendData.latencies).reduce((sum: number, stat: any) => sum + stat.avg_ms, 0) / Object.keys(backendData.latencies).length || 0,
        requests_by_endpoint: backendData.requests.by_endpoint,
        status_codes: backendData.requests.by_status,
        ab_testing: {
          v1_count: backendData.ab_tests.by_arm.v1 || 0,
          v2_count: backendData.ab_tests.by_arm.v2 || 0,
          by_endpoint: Object.fromEntries(
            Object.entries(backendData.ab_tests.by_endpoint).map(([endpoint, arms]: [string, any]) => [
              endpoint,
              { v1: arms.v1 || 0, v2: arms.v2 || 0 }
            ])
          ),
        },
        latency_stats: Object.fromEntries(
          Object.entries(backendData.latencies).map(([endpoint, stats]: [string, any]) => [
            endpoint,
            {
              avg: stats.avg_ms,
              min: stats.min_ms,
              max: stats.max_ms,
              p50: stats.p50_ms,
              p95: stats.p95_ms,
              p99: stats.p99_ms,
            }
          ])
        ),
        uptime_seconds: backendData.uptime_seconds,
      } as MetricsData;
    },
    refetchInterval: refreshInterval,
  });

  const handleExport = () => {
    if (!metrics) return;
    const dataStr = JSON.stringify(metrics, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `metrics-${new Date().toISOString()}.json`;
    link.click();
    toast({
      title: "Metrics Exported",
      description: "Metrics data has been downloaded as JSON",
    });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-effect">
              <BarChart3 className="w-4 h-4 text-success" />
              <span className="text-sm font-medium">Real-time Monitoring</span>
            </div>
            <h1 className="text-4xl font-bold gradient-text">
              Metrics Dashboard
            </h1>
          </div>

          <div className="flex items-center gap-2">
            <select
              value={refreshInterval || "manual"}
              onChange={(e) => setRefreshInterval(e.target.value === "manual" ? false : parseInt(e.target.value))}
              className="px-3 py-2 rounded-lg border border-border bg-background text-sm"
            >
              <option value="manual">Manual</option>
              <option value="5000">5s</option>
              <option value="10000">10s</option>
              <option value="30000">30s</option>
            </select>
            
            <Button onClick={() => refetch()} size="sm" variant="outline">
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </Button>

            <Button onClick={handleExport} size="sm" variant="outline">
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
          </div>
        </div>

        {/* Metrics Content */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto" />
            <p className="mt-4 text-muted-foreground">Loading metrics...</p>
          </div>
        ) : metrics ? (
          <div className="space-y-6">
            <MetricsOverview metrics={metrics} />
            <ABTestingMetrics metrics={metrics} />
            <LatencyMetrics metrics={metrics} />
          </div>
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-muted-foreground">No metrics data available</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Metrics;
