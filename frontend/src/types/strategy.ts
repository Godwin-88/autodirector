export interface Pillar {
  id: string;
  series: string;
  pillar_number: number;
  name: string;
  code: string;
  publish_day: string;
  description: string | null;
  color: string;
  active: boolean;
}

export interface PlannedEpisode {
  id: string;
  pillar_id?: string;
  sequence_number: number;
  topic: string;
  suggested_title: string | null;
  notes: string | null;
  status: "planned" | "scheduled" | "in_production" | "produced" | "skipped";
  target_date: string | null;
  episode_id: string | null;
}

export interface Suggestion {
  status: string;
  date: string;
  day: string;
  source: string;
  pillar: {
    id: string;
    name: string;
    code: string;
    color: string;
  };
  suggestion: PlannedEpisode | null;
}

export interface WeekPreview {
  [index: number]: Suggestion;
}