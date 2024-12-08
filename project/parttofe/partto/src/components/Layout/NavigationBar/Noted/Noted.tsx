import React, { MutableRefObject, ReactNode, useState } from "react";

import { NavigationBar } from "../NavigationBar";
import { Notes } from "../Notes/Notes";
import { NoteProps } from "../Note/NoteTypes";
import { StoredNote } from "./NotedTypes";

let notePassRef: MutableRefObject<(arg: NoteProps) => void> = {
  current: (arg: NoteProps) => undefined,
};

export const addErrorNote = ({
  heading,
  detail,
}: {
  heading: ReactNode;
  detail: ReactNode;
}) => {
  notePassRef.current({ heading, detail });
};

export function Noted() {
  const [notes, setNotes] = useState<Array<StoredNote>>([]);
  notePassRef.current = (note) => {
    const newKey = Math.random();
    setTimeout(() => {
      setNotes((previous) => previous.filter(({ key }) => key !== newKey));
    }, 20000);
    setNotes((previous) => [{ ...note, key: newKey }, ...previous]);
  };
  return <NavigationBar extra={<Notes notes={notes} />} />;
}
