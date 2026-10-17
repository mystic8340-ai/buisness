
import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import "./App.css";

const API = "http://127.0.0.1:8000";

const COLORS = [
  "#4f46e5",
  "#0d9488",
  "#f59e0b",
  "#e11d48",
  "#7c3aed",
  "#0284c7",
  "#65a30d",
  "#db2777",
];

function App() {
  const [summary, setSummary] = useState(null);
  const [cities, setCities] = useState([]);
  const [categories, setCategories] = useState([]);
  const [sources, setSources] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const endpoints = [
          "/api/dashboard/summary",
          "/api/dashboard/cities",
          "/api/dashboard/categories",
          "/api/dashboard/sources",
        ];

        const responses = await Promise.all(
          endpoints.map((endpoint) =>
            fetch(`${API}${endpoint}`)
          )
        );

        for (const response of responses) {
          if (!response.ok) {
            throw new Error(
              `API request failed: ${response.status}`
            );
          }
        }

        const [
          summaryData,
          cityData,
          categoryData,
          sourceData,
        ] = await Promise.all(
          responses.map((response) => response.json())
        );

        setSummary(summaryData);
        setCities(cityData);
        setCategories(categoryData);
        setSources(sourceData);
      } catch (err) {
        setError(
          "Could not load dashboard data. Check that FastAPI " +
          "and MySQL are running."
        );
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  const categoryChart = categories.map((item) => ({
    name: item.category,
    value: item.count,
  }));

  const sourceChart = sources.map((item) => ({
    name: item.source,
    value: item.count,
  }));

  if (loading) {
    return <main className="page"><p>Loading dashboard...</p></main>;
  }

  if (error) {
    return (
      <main className="page">
        <h1>Business Listings Dashboard</h1>
        <p className="error">{error}</p>
        <p>
          Check the backend at http://127.0.0.1:8000/api/health
        </p>
      </main>
    );
  }

  const cards = [
    {
      label: "Total Businesses",
      value: summary?.total_businesses ?? 0,
    },
    {
      label: "Cities",
      value: summary?.total_cities ?? 0,
    },
    {
      label: "Categories",
      value: summary?.total_categories ?? 0,
    },
    {
      label: "Data Sources",
      value: summary?.total_sources ?? 0,
    },
  ];

  return (
    <main className="page">
      <header className="header">
        <div>
          <p className="eyebrow">DATA ANALYTICS</p>
          <h1>Business Listings Dashboard</h1>
          <p className="subtitle">
            Explore businesses by location, category, and source.
          </p>
        </div>
        <span className="live-status">● API Dashboard</span>
      </header>

      <section className="summary-grid">
        {cards.map((card) => (
          <article className="summary-card" key={card.label}>
            <p>{card.label}</p>
            <h2>{Number(card.value).toLocaleString()}</h2>
          </article>
        ))}
      </section>

      <section className="chart-grid">
        <article className="chart-card city-card">
          <h2>City-wise Business Count</h2>
          <p className="chart-subtitle">
            Number of listings in each city
          </p>

          {cities.length === 0 ? (
            <p>No city data available.</p>
          ) : (
            <ResponsiveContainer width="100%" height={320}>
              <BarChart
                data={cities.slice(0, 10)}
                layout="vertical"
                margin={{ top: 10, right: 20, left: 20, bottom: 10 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" allowDecimals={false} />
                <YAxis
                  type="category"
                  dataKey="city"
                  width={110}
                  tick={{ fontSize: 12 }}
                />
                <Tooltip />
                <Bar
                  dataKey="count"
                  name="Businesses"
                  fill="#4f46e5"
                  radius={[0, 5, 5, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          )}
        </article>

        <article className="chart-card">
          <h2>Category-wise Distribution</h2>
          <p className="chart-subtitle">
            Business listings grouped by category
          </p>

          {categoryChart.length === 0 ? (
            <p>No category data available.</p>
          ) : (
            <ResponsiveContainer width="100%" height={320}>
              <PieChart>
                <Pie
                  data={categoryChart}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="45%"
                  outerRadius={100}
                  label
                >
                  {categoryChart.map((item, index) => (
                    <Cell
                      key={item.name}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </article>

        <article className="chart-card">
          <h2>Source-wise Distribution</h2>
          <p className="chart-subtitle">
            Where the business listings came from
          </p>

          {sourceChart.length === 0 ? (
            <p>No source data available.</p>
          ) : (
            <ResponsiveContainer width="100%" height={320}>
              <PieChart>
                <Pie
                  data={sourceChart}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="45%"
                  outerRadius={100}
                  label
                >
                  {sourceChart.map((item, index) => (
                    <Cell
                      key={item.name}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </article>
      </section>

      <footer>
        Business Listings Dashboard · React + FastAPI + MySQL
      </footer>
    </main>
  );
}

export default App;
