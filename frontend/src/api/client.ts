import type { Airport, ProgramInfo, SearchRequest, SearchResponse } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE || "";

async function http<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  return (await res.json()) as T;
}

export const api = {
  search: (req: SearchRequest) =>
    http<SearchResponse>("/api/search", {
      method: "POST",
      body: JSON.stringify(req),
    }),
  programs: () => http<ProgramInfo[]>("/api/programs"),
  airports: () => http<Airport[]>("/api/airports"),
};
