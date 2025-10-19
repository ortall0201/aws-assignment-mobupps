import { NavLink } from "react-router-dom";
import { Search, BarChart3, FileText, Zap, Moon, Sun } from "lucide-react";
import { Button } from "./ui/button";
import { useTheme } from "./ThemeProvider";

const navItems = [
  { to: "/", label: "Search", icon: Search },
  { to: "/predict", label: "Predict", icon: Zap },
  { to: "/metrics", label: "Metrics", icon: BarChart3 },
  { to: "/docs", label: "API Docs", icon: FileText },
];

export const Navigation = () => {
  const { theme, setTheme } = useTheme();

  return (
    <nav className="sticky top-0 z-50 glass-effect border-b border-border/50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <NavLink to="/" className="flex items-center gap-2 group">
            <div className="w-10 h-10 rounded-lg bg-gradient-primary flex items-center justify-center shadow-glow">
              <Search className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold gradient-text">MobUpps</span>
          </NavLink>

          <div className="flex items-center gap-1">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  `flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                    isActive
                      ? "bg-primary text-primary-foreground shadow-md"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted"
                  }`
                }
              >
                <item.icon className="w-4 h-4" />
                <span className="hidden md:inline">{item.label}</span>
              </NavLink>
            ))}
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="rounded-full"
          >
            {theme === "dark" ? (
              <Sun className="w-5 h-5" />
            ) : (
              <Moon className="w-5 h-5" />
            )}
          </Button>
        </div>
      </div>
    </nav>
  );
};
