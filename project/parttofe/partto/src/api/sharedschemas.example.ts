export interface Task {
  name: string;
  duration: number;
  description: string;
  depends?: Array<string>;
  engagement: number;
}

export interface WireTask {
  name: string;
  duration: number;
  description: string;
  depends?: Array<string>;
  engagement: number;
}
