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
  const [hideMock, setHideMock] = useState(false);
  const [sortKey, setSortKey] = useState<SortKey>("miles");
  const [sortDir, setSortDir] = useState<1 | -1>(1);

  const rows: FlightOffer[] = useMemo(() => {
    if (!data) return [];
    const filtered = hideMock ? data.offers.filter((o) => !o.is_mock) : data.offers;
    const sorted = [...filtered].sort((a, b) => {
      const dir = sortDir;
      if (sortKey === "miles") return (a.miles - b.miles) * dir;
      if (sortKey === "stops") return (a.stops - b.stops) * dir;
      if (sortKey === "program")
        return a.program_name.localeCompare(b.program_name) * dir;
      if (sortKey === "cabin") return a.cabin.localeCompare(b.cabin) * dir;
      return 0;
    });
    return sorted;
  }, [data, hideMock, sortKey, sortDir]);

  if (!data) {
    return (
      <div className="rounded-2xl border border-border bg-panel/60 p-10 text-center text-muted">
        Run a search to see award availability across programs.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="text-sm text-muted">
          <span className="text-slate-200 font-medium">
            {data.origin} → {data.destination}
          </span>{" "}
          • {data.depart_date} • {CABIN_LABEL[data.cabin]} • {rows.length} offers
          {data.cached && (
            <span className="ml-2 rounded-full border border-border bg-panel2 px-2 py-0.5 text-[10px] uppercase tracking-wider text-muted">
              cached
            </span>
          )}
        </div>
        <label className="flex items-center gap-2 text-xs text-muted">
          <input
            type="checkbox"
            className="accent-accent2"
            checked={hideMock}
            onChange={(e) => setHideMock(e.target.checked)}
          />
          Hide mock data
        </label>
      </div>

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
              <th className="px-3 py-2 text-left"></th>
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 && (
              <tr>
                <td colSpan={8} className="px-3 py-10 text-center text-muted">
                  No offers found.
                </td>
              </tr>
            )}
            {rows.map((o, i) => (
              <tr
                key={i}
                className="border-t border-border bg-panel/40 hover:bg-panel2/60"
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
                  {o.is_mock && (
                    <span className="rounded-full border border-yellow-700/40 bg-yellow-500/10 px-2 py-0.5 text-[10px] uppercase tracking-wider text-yellow-400">
                      mock
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

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

function ProgramStatusBar({ data }: { data: SearchResponse }) {
  return (
    <div className="rounded-2xl border border-border bg-panel/60 p-4">
      <div className="mb-2 text-xs uppercase tracking-wider text-muted">
        Provider status
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
              </div>
            </div>
            <div>
              {s.succeeded && !s.used_mock && (
                <span className="rounded-full bg-emerald-500/15 px-2 py-0.5 text-[10px] uppercase text-emerald-300">
                  live
                </span>
              )}
              {s.used_mock && (
                <span className="rounded-full bg-yellow-500/15 px-2 py-0.5 text-[10px] uppercase text-yellow-300">
                  mock
                </span>
              )}
              {!s.succeeded && !s.used_mock && (
                <span className="rounded-full bg-rose-500/15 px-2 py-0.5 text-[10px] uppercase text-rose-300">
                  fail
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
