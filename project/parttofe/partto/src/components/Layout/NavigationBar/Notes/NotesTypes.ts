import { NoteProps } from "../Note/NoteTypes";

export enum TimeToLive {
  NOTICABLE,
  UNTIL_CLICKED,
}

export interface NoteForNotesProps extends NoteProps {
  timeToLive?: TimeToLive;
}

export interface NotesProps {
  notes: Array<NoteForNotesProps>;
}
