import React, { useEffect, useState } from "react";

import classes from "./Notes.module.scss";
import { Note } from "../Note/Note";
import { NotesProps } from "./NotesTypes";

export function Notes({ notes }: NotesProps) {
  const [active, setActive] = useState<number>(0);
  useEffect(() => {
    if (notes.length < 1) {
      return;
    }
    const id = setInterval(() => {
      setActive((previous) =>
        previous + 1 === notes.length ? 0 : previous + 1,
      );
    }, 5000);
    return () => {
      clearInterval(id);
    };
  });
  if (notes.length < 1) {
    return <></>;
  }
  return (
    <div className={classes.notes} data-testid="Notes">
      {notes.map((note, index) => (
        <div
          key={`${note.detail}-${note.heading}`}
          className={`${active !== index ? classes.inactive : ""} ${classes.note}`}
        >
          <Note {...note} />
        </div>
      ))}
    </div>
  );
}
