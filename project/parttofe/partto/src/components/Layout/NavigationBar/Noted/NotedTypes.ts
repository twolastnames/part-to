import { NoteProps } from "../Note/NoteTypes";
import { TimeToLive } from "../Notes/NotesTypes";

export interface StoredNote extends NoteProps {
  timeToLive: TimeToLive;
  key: string;
}
