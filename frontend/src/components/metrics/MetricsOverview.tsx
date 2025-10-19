import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, Clock, Server, CheckCircle } from "lucide-react";
import { MetricsData } from "@/pages/Metrics";

interface MetricsOverviewProps {
  metrics: MetricsData;
}

export const MetricsOverview = ({ metrics }: MetricsOverviewProps) => {
  const formatUptime = (seconds: number) => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const mins = Math.floor((seconds % 3600) / 60);

    if (days > 0) return `${days}d ${hours}h`;
    if (hours > 0) return `${hours}h ${mins}m`;
    return `${mins}m`;
  };

  // Calculate real success rate from status codes
  const calculateSuccessRate = () => {
    const successCount = parseInt(metrics.status_codes["200"] || "0");
    const total = metrics.total_requests;
    if (total === 0) return "0.0%";
    return `${((successCount / total) * 100).toFixed(1)}%`;
  };

  const stats = [
    {
      title: "Total Requests",
      value: metrics.total_requests.toLocaleString(),
      icon: Activity,
      color: "text-primary",
      bg: "bg-primary/10",
    },
    {
      title: "Avg Latency",
      value: `${metrics.avg_latency_ms.toFixed(1)}ms`,
      icon: Clock,
      color: "text-warning",
      bg: "bg-warning/10",
    },
    {
      title: "Uptime",
      value: formatUptime(metrics.uptime_seconds),
      icon: Server,
      color: "text-success",
      bg: "bg-success/10",
    },
    {
      title: "Success Rate",
      value: calculateSuccessRate(),
      icon: CheckCircle,
      color: "text-success",
      bg: "bg-success/10",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, index) => (
        <Card key={index} className="shadow-glass border-border/50 animate-slide-up" style={{ animationDelay: `${index * 100}ms` }}>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">{stat.title}</p>
                <p className="text-3xl font-bold mt-1">{stat.value}</p>
              </div>
              <div className={`w-12 h-12 rounded-lg ${stat.bg} flex items-center justify-center`}>
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};
