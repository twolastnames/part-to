import { NoteProps } from "../Note/NoteTypes";

export interface StoredNote extends NoteProps {
  key: number;
}
