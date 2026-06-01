import { useEffect, useMemo, useState } from "react";
import type { Airport, Cabin, ProgramInfo, SearchRequest } from "../types";
import { api } from "../api/client";

interface Props {
  onSubmit: (req: SearchRequest) => void;
  loading: boolean;
}

const CABINS: { value: Cabin; label: string }[] = [
  { value: "economy", label: "Economy" },
  { value: "premium_economy", label: "Premium Economy" },
  { value: "business", label: "Business" },
  { value: "first", label: "First" },
];

function todayPlus(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}

export default function SearchForm({ onSubmit, loading }: Props) {
  const [origin, setOrigin] = useState("JFK");
  const [destination, setDestination] = useState("LHR");
  const [departDate, setDepartDate] = useState(todayPlus(30));
  const [cabin, setCabin] = useState<Cabin>("business");
  const [passengers, setPassengers] = useState(1);
  const [airports, setAirports] = useState<Airport[]>([]);
  const [programs, setPrograms] = useState<ProgramInfo[]>([]);
  const [selectedPrograms, setSelectedPrograms] = useState<string[]>([]);

  useEffect(() => {
    api.airports().then(setAirports).catch(() => {});
    api.programs().then(setPrograms).catch(() => {});
  }, []);

  const airportOptions = useMemo(
    () => airports.map((a) => ({ value: a.iata, label: `${a.iata} — ${a.city}` })),
    [airports],
  );

  function toggleProgram(p: string) {
    setSelectedPrograms((prev) =>
      prev.includes(p) ? prev.filter((x) => x !== p) : [...prev, p],
    );
  }

  function submit(e: React.FormEvent) {
    e.preventDefault();
    onSubmit({
      origin,
      destination,
      depart_date: departDate,
      cabin,
      passengers,
      programs: selectedPrograms.length ? selectedPrograms : null,
    });
  }

  return (
    <form
      onSubmit={submit}
      className="rounded-2xl border border-border bg-panel/80 p-5 shadow-2xl shadow-black/30"
    >
      <div className="grid grid-cols-1 gap-3 md:grid-cols-6">
        <Select
          label="From"
          value={origin}
          onChange={setOrigin}
          options={airportOptions}
          className="md:col-span-2"
        />
        <Select
          label="To"
          value={destination}
          onChange={setDestination}
          options={airportOptions}
          className="md:col-span-2"
        />
        <Field label="Depart">
          <input
            type="date"
            className="input"
            value={departDate}
            min={todayPlus(0)}
            onChange={(e) => setDepartDate(e.target.value)}
          />
        </Field>
        <Field label="Pax">
          <input
            type="number"
            className="input"
            min={1}
            max={9}
            value={passengers}
            onChange={(e) => setPassengers(Number(e.target.value))}
          />
        </Field>

        <Field label="Cabin" className="md:col-span-2">
          <div className="flex flex-wrap gap-1">
            {CABINS.map((c) => (
              <button
                key={c.value}
                type="button"
                onClick={() => setCabin(c.value)}
                className={`rounded-md border px-3 py-1.5 text-xs transition ${
                  cabin === c.value
                    ? "border-accent bg-accent/10 text-accent"
                    : "border-border bg-panel2 text-slate-300 hover:border-slate-500"
                }`}
              >
                {c.label}
              </button>
            ))}
          </div>
        </Field>

        <div className="md:col-span-4">
          <div className="mb-1.5 text-xs uppercase tracking-wider text-muted">
            Programs (leave empty for all)
          </div>
          <div className="flex flex-wrap gap-1.5">
            {programs.map((p) => {
              const on = selectedPrograms.includes(p.program);
              return (
                <button
                  key={p.program}
                  type="button"
                  onClick={() => toggleProgram(p.program)}
                  className={`rounded-md border px-2.5 py-1 text-xs transition ${
                    on
                      ? "border-accent2 bg-accent2/10 text-accent2"
                      : "border-border bg-panel2 text-slate-300 hover:border-slate-500"
                  }`}
                  title={p.notes || ""}
                >
                  {p.program_name}
                  {p.implementation !== "live" && (
                    <span className="ml-1 text-[10px] uppercase opacity-60">
                      {p.implementation}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      <div className="mt-4 flex items-center justify-end">
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-gradient-to-br from-accent2 to-accent px-5 py-2 text-sm font-semibold text-ink shadow hover:opacity-95 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search Awards"}
        </button>
      </div>

      <style>{`
        .input {
          width: 100%;
          background: #161a23;
          border: 1px solid #1f2433;
          color: #e2e8f0;
          padding: 0.5rem 0.65rem;
          border-radius: 0.5rem;
          font-size: 0.875rem;
        }
        .input:focus { outline: none; border-color: #60a5fa; }
      `}</style>
    </form>
  );
}

function Field(props: { label: string; className?: string; children: React.ReactNode }) {
  return (
    <div className={props.className}>
      <div className="mb-1.5 text-xs uppercase tracking-wider text-muted">{props.label}</div>
      {props.children}
    </div>
  );
}

function Select(props: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: { value: string; label: string }[];
  className?: string;
}) {
  return (
    <Field label={props.label} className={props.className}>
      <input
        list={`list-${props.label}`}
        className="input"
        value={props.value}
        onChange={(e) => props.onChange(e.target.value.toUpperCase())}
      />
      <datalist id={`list-${props.label}`}>
        {props.options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </datalist>
    </Field>
  );
}
