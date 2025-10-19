import { FileText, ExternalLink, Copy } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "@/hooks/use-toast";

const endpoints = [
  {
    method: "GET",
    path: "/healthz",
    description: "Health check endpoint",
    request: null,
    response: {
      status: "healthy",
      uptime_seconds: 3600,
    },
  },
  {
    method: "GET",
    path: "/metrics",
    description: "Get operational metrics and A/B testing stats",
    request: null,
    response: {
      total_requests: 1234,
      avg_latency_ms: 45.2,
      ab_testing: { v1_count: 617, v2_count: 617 },
    },
  },
  {
    method: "POST",
    path: "/api/v1/find-similar",
    description: "Find similar apps based on input criteria",
    request: {
      app_name: "Fitness Tracker Pro",
      category: "Health & Fitness",
      region: "US",
      pricing_model: "freemium",
      features: ["tracking", "notifications"],
      top_k: 20,
    },
    response: {
      ab_arm: "v1",
      similar_apps: [
        {
          app_id: "app_123",
          app_name: "Health Monitor",
          category: "Health & Fitness",
          similarity_score: 0.95,
        },
      ],
    },
  },
  {
    method: "POST",
    path: "/api/v1/predict",
    description: "Predict app performance based on similar apps",
    request: {
      app_id: "app_456",
      partner_id: "partner_789",
      neighbor_results: [
        { app_id: "app_123", similarity_score: 0.95 },
      ],
      ab_arm: "v1",
    },
    response: {
      predicted_score: 4.2,
      user_segments: ["fitness_enthusiasts", "health_conscious"],
      confidence: 0.87,
      latency_ms: 23,
    },
  },
];

const ApiDocs = () => {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied!",
      description: "Code copied to clipboard",
    });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-4 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-effect">
            <FileText className="w-4 h-4 text-accent" />
            <span className="text-sm font-medium">API Documentation</span>
          </div>
          
          <h1 className="text-4xl md:text-5xl font-bold gradient-text">
            API Reference
          </h1>
          
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Complete API documentation for the MobUpps similarity search and prediction service
          </p>

          <div className="flex justify-center gap-4">
            <Button variant="outline" asChild>
              <a href={`${apiBaseUrl}/docs`} target="_blank" rel="noopener noreferrer">
                <ExternalLink className="w-4 h-4 mr-2" />
                Swagger Docs
              </a>
            </Button>
            <Button variant="outline" asChild>
              <a href={`${apiBaseUrl}/redoc`} target="_blank" rel="noopener noreferrer">
                <ExternalLink className="w-4 h-4 mr-2" />
                ReDoc
              </a>
            </Button>
          </div>
        </div>

        {/* Endpoints */}
        <div className="space-y-6">
          {endpoints.map((endpoint, index) => (
            <Card key={index} className="shadow-glass border-border/50 animate-slide-up" style={{ animationDelay: `${index * 100}ms` }}>
              <CardHeader>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <Badge variant={endpoint.method === "GET" ? "secondary" : "default"}>
                        {endpoint.method}
                      </Badge>
                      <code className="text-sm font-mono text-primary">{endpoint.path}</code>
                    </div>
                    <CardTitle className="text-lg">{endpoint.description}</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {endpoint.request && (
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold text-sm">Request Body</h4>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => copyToClipboard(JSON.stringify(endpoint.request, null, 2))}
                      >
                        <Copy className="w-4 h-4" />
                      </Button>
                    </div>
                    <pre className="bg-muted p-4 rounded-lg overflow-x-auto text-sm">
                      <code>{JSON.stringify(endpoint.request, null, 2)}</code>
                    </pre>
                  </div>
                )}

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-sm">Response</h4>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => copyToClipboard(JSON.stringify(endpoint.response, null, 2))}
                    >
                      <Copy className="w-4 h-4" />
                    </Button>
                  </div>
                  <pre className="bg-muted p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{JSON.stringify(endpoint.response, null, 2)}</code>
                  </pre>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ApiDocs;
