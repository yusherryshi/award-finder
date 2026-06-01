export type Cabin = "economy" | "premium_economy" | "business" | "first";

export interface SearchRequest {
  origin: string;
  destination: string;
  depart_date: string;
  return_date?: string | null;
  cabin: Cabin;
  passengers: number;
  programs?: string[] | null;
}

export interface FlightOffer {
  program: string;
  program_name: string;
  alliance?: string | null;
  origin: string;
  destination: string;
  depart_date: string;
  depart_time?: string | null;
  arrive_time?: string | null;
  flight_numbers: string[];
  operating_airlines: string[];
  cabin: Cabin;
  miles: number;
  taxes_currency?: string | null;
  taxes_amount?: number | null;
  seats_available?: number | null;
  direct: boolean;
  stops: number;
  source_url?: string | null;
  is_mock: boolean;
}

export interface ProgramStatus {
  program: string;
  program_name: string;
  alliance?: string | null;
  queried: boolean;
  succeeded: boolean;
  duration_ms: number;
  error?: string | null;
  used_mock: boolean;
}

export interface SearchResponse {
  origin: string;
  destination: string;
  depart_date: string;
  cabin: Cabin;
  passengers: number;
  cached: boolean;
  offers: FlightOffer[];
  program_statuses: ProgramStatus[];
}

export interface ProgramInfo {
  program: string;
  program_name: string;
  alliance?: string | null;
  implementation: "live" | "stub" | "mock";
  notes?: string | null;
}

export interface Airport {
  iata: string;
  city: string;
  country: string;
  tz: string;
}
