import { ReactNode } from "react";

export interface NoteProps {
  heading: ReactNode;
  detail: ReactNode;
  onClick?: () => void;
  sound?: string;
}
