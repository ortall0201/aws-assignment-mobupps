import { useQuery } from "@tanstack/react-query";
import { Activity } from "lucide-react";

export const Footer = () => {
  const { data: health } = useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}/healthz`);
      return response.json();
    },
    refetchInterval: 30000,
  });

  return (
    <footer className="border-t border-border/50 bg-card/50">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex flex-col gap-1">
            <div className="text-sm text-muted-foreground">
              © 2025 MobUpps. Powered by AI similarity search.
            </div>
            <div className="text-xs text-muted-foreground/70">
              Created by <span className="font-semibold">Ortal Lasry</span> - ML Engineer | AI team
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Activity className={`w-4 h-4 ${health?.status === "healthy" ? "text-success" : "text-warning"}`} />
            <span className="text-sm text-muted-foreground">
              API Status: <span className={health?.status === "healthy" ? "text-success" : "text-warning"}>
                {health?.status || "Unknown"}
              </span>
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
