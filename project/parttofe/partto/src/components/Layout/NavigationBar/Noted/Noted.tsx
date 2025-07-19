import React, { MutableRefObject, ReactNode, useState } from "react";
import { NavigationBar } from "../NavigationBar";
import { Notes } from "../Notes/Notes";
import { NoteProps } from "../Note/NoteTypes";
import { StoredNote } from "./NotedTypes";
import { NoteForNotesProps, TimeToLive } from "../Notes/NotesTypes";
import { Flasher } from "../../../Flasher/Flasher";

let notePassRef: MutableRefObject<(arg: NoteForNotesProps) => void> = {
  current: (arg: NoteProps) => undefined,
};

export const addErrorNote = ({
  heading,
  detail,
}: {
  heading: ReactNode;
  detail: ReactNode;
}) => {
  notePassRef.current({ heading, detail, timeToLive: TimeToLive.NOTICABLE });
};

export const addAlarmNote = ({
  key,
  heading,
  detail,
  onClick,
}: {
  key: string;
  heading: ReactNode;
  detail: ReactNode;
  onClick?: () => void;
}) => {
  const onLocalClick = () => {
    onClick && onClick();
  };
  notePassRef.current({
    key,
    heading: <Flasher>{heading}</Flasher>,
    detail: <Flasher>{detail}</Flasher>,
    onClick: onLocalClick,
    timeToLive: TimeToLive.UNTIL_CLICKED,
  });
};

const noteRemovalRef: MutableRefObject<(key: string) => void> = {
  current: (key: string) => undefined,
};

export function removeNote(key: string) {
  noteRemovalRef.current(key);
}

export function Noted() {
  const [notes, setNotes] = useState<Array<StoredNote>>([]);
  const removeNote = (newKey: string) => {
    setNotes((previous) => previous.filter(({ key }) => key !== newKey));
  };
  noteRemovalRef.current = removeNote;

  notePassRef.current = (note) => {
    const newKey = note.key || Math.random().toString();
    if (notes.some(({ key }) => key === newKey)) {
      return;
    }
    const remove = () => {
      removeNote(newKey);
    };
    if (note.timeToLive === TimeToLive.NOTICABLE) {
      setTimeout(remove, 20000);
    }
    const onClick =
      note.timeToLive === TimeToLive.UNTIL_CLICKED
        ? () => {
            remove();
            note.onClick && note.onClick();
          }
        : () => note.onClick && note.onClick();
    setNotes((previous) => [{ ...note, onClick, key: newKey }, ...previous]);
  };
  return <NavigationBar extra={<Notes notes={notes} />} />;
}
