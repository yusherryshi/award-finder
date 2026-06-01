import { useState } from "react";
import Header from "./components/Header";
import SearchForm from "./components/SearchForm";
import ResultsTable from "./components/ResultsTable";
import { api } from "./api/client";
import type { SearchRequest, SearchResponse } from "./types";

export default function App() {
  const [data, setData] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(req: SearchRequest) {
    setLoading(true);
    setError(null);
    try {
      const res = await api.search(req);
      setData(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Search failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-full">
      <Header />
      <main className="mx-auto max-w-6xl space-y-6 px-6 py-8">
        <SearchForm onSubmit={handleSubmit} loading={loading} />
        {error && (
          <div className="rounded-lg border border-rose-700/40 bg-rose-500/10 px-4 py-2 text-sm text-rose-300">
            {error}
          </div>
        )}
        <ResultsTable data={data} />
        <footer className="pt-8 text-center text-xs text-muted">
          Award Finder is a free, open project. Live offers come from public airline
          endpoints; for programs without working live access, use the airline links to
          search on their own site. Not affiliated with any airline.
        </footer>
      </main>
    </div>
  );
}
