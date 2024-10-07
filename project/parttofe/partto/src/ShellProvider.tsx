import React, { MutableRefObject, useRef, useState } from "react";

import { MantineProvider, createTheme } from "@mantine/core";
import { PropsWithChildren } from "react";
import "@mantine/core/styles.layer.css";
import "./App.scss";

const themes = {
  default: createTheme({
    primaryColor: "red",
  }),
  dark: createTheme({
    primaryColor: "red",
  }),
};

let themeChangeRef: MutableRefObject<(theme: Theme) => void>;

export enum Theme {
  Default = "default",
  Dark = "dark",
}

export function changeTheme(theme: Theme) {
  const themeNode = document.getElementById("theme");
  if (!themeNode || !themeNode.className) {
    console.error("developers should have created an theme ID in the project");
    return;
  }
  themeChangeRef?.current && themeChangeRef.current(theme);
  themeNode.className = `${theme}Theme`;
}

export const ShellProvider = ({ children }: PropsWithChildren) => {
  const [theme, setTheme] = useState<Theme>(Theme.Default);
  themeChangeRef = useRef(setTheme);
  return (
    <div id="theme" className="defaultTheme">
      <MantineProvider theme={themes[theme]}>{children}</MantineProvider>
    </div>
  );
};
