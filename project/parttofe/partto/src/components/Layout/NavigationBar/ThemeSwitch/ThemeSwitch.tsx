import React, { useState } from "react";

import classes from "./ThemeSwitch.module.scss";
import {
  Theme,
  changeTheme,
  getTheme,
} from "../../../../providers/ShellProvider";
import { Checkbox } from "@mantine/core";

export function ThemeSwitch() {
  const [theme, setTheme] = useState<Theme>(getTheme());
  return (
    <div className={classes.themeSwitch} data-testid="ThemeSwitch">
      <Checkbox
        id="ThemeSwitch"
        checked={getTheme() !== Theme.Default}
        onChange={() => {
          const changeTo = theme === Theme.Default ? Theme.Dark : Theme.Default;
          changeTheme(changeTo);
          setTheme(changeTo);
        }}
        label="Dark"
      />
    </div>
  );
}
