import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { SearchResponse } from "@/pages/Search";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

interface SearchResultsProps {
  results: SearchResponse;
}

export const SearchResults = ({ results }: SearchResultsProps) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

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
        </CardContent>
      </Card>
    </div>
  );
};
