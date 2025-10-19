import { useState } from "react";
import { Search as SearchIcon, Sparkles } from "lucide-react";
import { SearchForm } from "@/components/search/SearchForm";
import { SearchResults } from "@/components/search/SearchResults";
import { Card, CardContent } from "@/components/ui/card";

export interface SimilarApp {
  app_id: string;
  app_name: string;
  category: string;
  similarity_score: number;
}

export interface SearchResponse {
  ab_arm: string;
  similar_apps: SimilarApp[];
  correlation_id: string;
}

const Search = () => {
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Hero Section */}
        <div className="text-center space-y-4 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-effect">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium">AI-Powered App Discovery</span>
          </div>
          
          <h1 className="text-4xl md:text-5xl font-bold gradient-text">
            Find Similar Apps with AI
          </h1>
          
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Discover mobile apps similar to yours using advanced machine learning algorithms.
            Get insights powered by A/B tested similarity models.
          </p>
        </div>

        {/* Search Form */}
        <Card className="shadow-glass border-border/50">
          <CardContent className="p-6">
            <SearchForm 
              onResults={setResults} 
              isLoading={isLoading}
              setIsLoading={setIsLoading}
            />
          </CardContent>
        </Card>

        {/* Results */}
        {results && <SearchResults results={results} />}
      </div>
    </div>
  );
};

export default Search;
