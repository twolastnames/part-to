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
  notePassRef.current({ heading, detail });
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
  heading,
  detail,
  onClick,
}: {
  heading: ReactNode;
  detail: ReactNode;
  onClick?: () => void;
}) => {
  new Audio(require("./messageAlert.mp3")).play();
  const id = setInterval(() => {
    new Audio(require("./messageAlert.mp3")).play();
  }, 6000);
  const onLocalClick = () => {
    clearInterval(id);
    onClick && onClick();
  };
  notePassRef.current({
    heading: <ChangingText>{heading}</ChangingText>,
    detail: <ChangingText>{detail}</ChangingText>,
    onClick: onLocalClick,
    timeToLive: TimeToLive.UNTIL_CLICKED,
  });
};

export function Noted() {
  const [notes, setNotes] = useState<Array<StoredNote>>([]);
  notePassRef.current = (note) => {
    const newKey = Math.random();
    const remove = () => {
      setNotes((previous) => previous.filter(({ key }) => key !== newKey));
    };
    if (note.timeToLive == null || note.timeToLive === TimeToLive.NOTICABLE) {
      setTimeout(remove, 20000);
    }
    const onClick =
      note.timeToLive === TimeToLive.UNTIL_CLICKED
        ? () => {
            remove();
            note.onClick && note.onClick();
          }
        : note.onClick;
    setNotes((previous) => [{ ...note, onClick, key: newKey }, ...previous]);
  };
  return <NavigationBar extra={<Notes notes={notes} />} />;
}
