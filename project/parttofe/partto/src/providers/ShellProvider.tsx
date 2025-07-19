import React, { MutableRefObject, useRef, useState } from "react";

import { MantineProvider, createTheme } from "@mantine/core";
import { PropsWithChildren } from "react";
import "@mantine/core/styles.layer.css";
import "../App.scss";
import {
  LeftDynamicItemSetPairProvider,
  RightDynamicItemSetPairProvider,
} from "./DynamicItemSetPair";
import { TimerProvider } from "./Timer";

export enum Theme {
  Default = "default",
  Dark = "dark",
}

const themeStorageKey = "theme";

export function getTheme(): Theme {
  return (localStorage.getItem(themeStorageKey) || Theme.Default) as Theme;
}

const themes = {
  default: createTheme({
    primaryColor: "red",
  }),
  dark: createTheme({
    primaryColor: "red",
  }),
};

let themeChangeRef: MutableRefObject<(theme: Theme) => void>;

function setThemeClass() {
  const themeNode = document.getElementById("theme");
  if (!themeNode || !themeNode.className) {
    console.error("developers should have created an theme ID in the project");
    return;
  }
  themeNode.className = `${getTheme()}Theme`;
}

export function changeTheme(theme: Theme) {
  localStorage.setItem(themeStorageKey, theme.toString());
  themeChangeRef?.current && themeChangeRef.current(theme);
}

export const ShellProvider = ({ children }: PropsWithChildren) => {
  const [theme, setTheme] = useState<Theme>(getTheme());
  themeChangeRef = useRef(setTheme);
  setTimeout(() => {
    setThemeClass();
  }, 0);
  return (
    <div id="theme" className="defaultTheme">
      <LeftDynamicItemSetPairProvider>
        <RightDynamicItemSetPairProvider>
          <TimerProvider>
            <MantineProvider theme={themes[theme]}>{children}</MantineProvider>
          </TimerProvider>
        </RightDynamicItemSetPairProvider>
      </LeftDynamicItemSetPairProvider>
    </div>
  );
};
