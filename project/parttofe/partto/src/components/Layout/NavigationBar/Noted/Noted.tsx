import React, {
  MutableRefObject,
  PropsWithChildren,
  ReactNode,
  useEffect,
  useState,
} from "react";
import classes from "./Noted.module.scss";
import { NavigationBar } from "../NavigationBar";
import { Notes } from "../Notes/Notes";
import { NoteProps } from "../Note/NoteTypes";
import { StoredNote } from "./NotedTypes";
import { NoteForNotesProps, TimeToLive } from "../Notes/NotesTypes";

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

const ChangingText = ({ children }: PropsWithChildren) => {
  const [classString, setClassString] = useState<string>("");
  useEffect(() => {
    const id = setInterval(() => {
      setClassString((previous) => (previous === "" ? classes.loudText : ""));
    }, 2000);
    return () => {
      clearInterval(id);
    };
  });
  return <span className={classString}>{children}</span>;
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
    heading: <ChangingText>{heading}</ChangingText>,
    detail: <ChangingText>{detail}</ChangingText>,
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
