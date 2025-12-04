export interface Team {
  id: number;
  full_name: string;
  abbreviation: string;
  city: string;
}

export interface TeamWithRoster extends Team {
  conference: string;
  division: string;
  roster: TeamPlayer[];
}

export interface TeamPlayer {
  id: number;
  name: string;
  position: string;
  per: number | null;
}