import { useMemo, useState } from "react";
import type { FlightOffer, SearchResponse } from "../types";

interface Props {
  data: SearchResponse | null;
}

type SortKey = "miles" | "program" | "cabin" | "stops";

const CABIN_LABEL: Record<string, string> = {
  economy: "Economy",
  premium_economy: "Premium",
  business: "Business",
  first: "First",
};

export default function ResultsTable({ data }: Props) {
  const [sortKey, setSortKey] = useState<SortKey>("miles");
  const [sortDir, setSortDir] = useState<1 | -1>(1);

  const rows: FlightOffer[] = useMemo(() => {
    if (!data) return [];
    const sorted = [...data.offers].sort((a, b) => {
      const dir = sortDir;
      if (sortKey === "miles") return (a.miles - b.miles) * dir;
      if (sortKey === "stops") return (a.stops - b.stops) * dir;
      if (sortKey === "program")
        return a.program_name.localeCompare(b.program_name) * dir;
      if (sortKey === "cabin") return a.cabin.localeCompare(b.cabin) * dir;
      return 0;
    });
    return sorted;
  }, [data, sortKey, sortDir]);

  if (!data) {
    return (
      <div className="rounded-2xl border border-border bg-panel/60 p-10 text-center text-muted">
        Run a search to see award availability across programs.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="text-sm text-muted">
        <span className="text-slate-200 font-medium">
          {data.origin} → {data.destination}
        </span>{" "}
        • {data.depart_date} • {CABIN_LABEL[data.cabin]} • {rows.length} live{" "}
        {rows.length === 1 ? "offer" : "offers"}
        {data.cached && (
          <span className="ml-2 rounded-full border border-border bg-panel2 px-2 py-0.5 text-[10px] uppercase tracking-wider text-muted">
            cached
          </span>
        )}
      </div>

      {rows.length > 0 && (
        <div className="overflow-hidden rounded-2xl border border-border">
          <table className="w-full text-sm">
            <thead className="bg-panel2 text-xs uppercase tracking-wider text-muted">
              <tr>
                <Th sortKey="program" current={sortKey} dir={sortDir} setSort={setSort}>
                  Program
                </Th>
                <th className="px-3 py-2 text-left">Route</th>
                <Th sortKey="cabin" current={sortKey} dir={sortDir} setSort={setSort}>
                  Cabin
                </Th>
                <Th sortKey="miles" current={sortKey} dir={sortDir} setSort={setSort}>
                  Miles
                </Th>
                <th className="px-3 py-2 text-left">Taxes</th>
                <Th sortKey="stops" current={sortKey} dir={sortDir} setSort={setSort}>
                  Stops
                </Th>
                <th className="px-3 py-2 text-left">Flights</th>
                <th className="px-3 py-2 text-left">Book</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((o, i) => (
                <tr
                  key={i}
                  onClick={() => o.source_url && window.open(o.source_url, "_blank", "noopener,noreferrer")}
                  className={`border-t border-border bg-panel/40 transition ${
                    o.source_url ? "cursor-pointer hover:bg-accent2/10" : ""
                  }`}
                >
                  <td className="px-3 py-2.5">
                    <div className="font-medium text-slate-100">{o.program_name}</div>
                    {o.alliance && (
                      <div className="text-[11px] text-muted">{o.alliance}</div>
                    )}
                  </td>
                  <td className="px-3 py-2.5 text-slate-300">
                    {o.origin} → {o.destination}
                    {o.depart_time && (
                      <span className="ml-2 text-[11px] text-muted">
                        {o.depart_time}
                        {o.arrive_time ? ` → ${o.arrive_time}` : ""}
                      </span>
                    )}
                  </td>
                  <td className="px-3 py-2.5 text-slate-300">{CABIN_LABEL[o.cabin]}</td>
                  <td className="px-3 py-2.5 font-mono text-accent">
                    {o.miles.toLocaleString()}
                  </td>
                  <td className="px-3 py-2.5 text-slate-300">
                    {o.taxes_amount != null
                      ? `${o.taxes_currency || ""} ${o.taxes_amount.toFixed(2)}`
                      : "—"}
                  </td>
                  <td className="px-3 py-2.5 text-slate-300">
                    {o.direct ? "Nonstop" : `${o.stops} stop${o.stops > 1 ? "s" : ""}`}
                  </td>
                  <td className="px-3 py-2.5 text-slate-300">
                    {o.flight_numbers.length ? o.flight_numbers.join(", ") : "—"}
                  </td>
                  <td className="px-3 py-2.5">
                    {o.source_url && (
                      <span className="text-accent2 underline-offset-2 hover:underline">
                        Open ↗
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <ProviderLinksPanel data={data} />
      <ProgramStatusBar data={data} />
    </div>
  );

  function setSort(k: SortKey) {
    if (k === sortKey) setSortDir((d) => (d === 1 ? -1 : 1));
    else {
      setSortKey(k);
      setSortDir(1);
    }
  }
}

function Th(props: {
  sortKey: SortKey;
  current: SortKey;
  dir: 1 | -1;
  setSort: (k: SortKey) => void;
  children: React.ReactNode;
}) {
  const active = props.current === props.sortKey;
  return (
    <th className="px-3 py-2 text-left">
      <button
        onClick={() => props.setSort(props.sortKey)}
        className={`inline-flex items-center gap-1 ${
          active ? "text-slate-200" : "hover:text-slate-200"
        }`}
      >
        {props.children}
        {active && <span>{props.dir === 1 ? "▲" : "▼"}</span>}
      </button>
    </th>
  );
}

function ProviderLinksPanel({ data }: { data: SearchResponse }) {
  if (!data.provider_links?.length) return null;
  return (
    <div className="rounded-2xl border border-border bg-panel/60 p-4">
      <div className="mb-2 flex items-baseline justify-between">
        <div className="text-xs uppercase tracking-wider text-muted">
          Search directly on airline sites
        </div>
        <div className="text-[11px] text-muted">
          Each opens the airline's own award search with your route pre-filled
        </div>
      </div>
      <div className="grid grid-cols-1 gap-2 md:grid-cols-2 lg:grid-cols-3">
        {data.provider_links.map((l) => (
          <a
            key={l.program}
            href={l.url}
            target="_blank"
            rel="noopener noreferrer"
            className="group flex items-center justify-between rounded-lg border border-border bg-panel2 px-3 py-2.5 text-sm transition hover:border-accent2 hover:bg-accent2/10"
          >
            <div>
              <div className="font-medium text-slate-100 group-hover:text-accent2">
                {l.program_name}
              </div>
              <div className="text-[11px] text-muted">{l.alliance || "—"}</div>
            </div>
            <div className="text-accent2 opacity-60 group-hover:opacity-100">
              Open ↗
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}

function ProgramStatusBar({ data }: { data: SearchResponse }) {
  if (!data.program_statuses?.length) return null;
  return (
    <div className="rounded-2xl border border-border bg-panel/60 p-4">
      <div className="mb-2 text-xs uppercase tracking-wider text-muted">
        Live provider status
      </div>
      <div className="grid grid-cols-1 gap-2 md:grid-cols-2 lg:grid-cols-3">
        {data.program_statuses.map((s) => (
          <div
            key={s.program}
            className="flex items-center justify-between rounded-lg border border-border bg-panel2 px-3 py-2 text-xs"
          >
            <div>
              <div className="font-medium text-slate-200">{s.program_name}</div>
              <div className="text-muted">
                {s.duration_ms}ms{s.alliance ? ` • ${s.alliance}` : ""}
                {s.error ? ` • ${s.error.slice(0, 40)}` : ""}
              </div>
            </div>
            <div>
              {s.succeeded && s.offers_found > 0 && (
                <span className="rounded-full bg-emerald-500/15 px-2 py-0.5 text-[10px] uppercase text-emerald-300">
                  {s.offers_found} offer{s.offers_found > 1 ? "s" : ""}
                </span>
              )}
              {s.succeeded && s.offers_found === 0 && (
                <span className="rounded-full bg-slate-500/15 px-2 py-0.5 text-[10px] uppercase text-slate-300">
                  none
                </span>
              )}
              {!s.succeeded && (
                <span className="rounded-full bg-rose-500/15 px-2 py-0.5 text-[10px] uppercase text-rose-300">
                  blocked
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
