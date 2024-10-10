import React, { useState } from "react";

import classes from "./ThemeSwitch.module.scss";
import { Theme, changeTheme } from "../../../../providers/ShellProvider";
import { Checkbox } from "@mantine/core";

export function ThemeSwitch() {
  const [theme, setTheme] = useState<Theme>(Theme.Default);
  return (
    <div className={classes.themeSwitch} data-testid="ThemeSwitch">
      <Checkbox
        checked={theme !== Theme.Default}
        onChange={() => {
          const changeTo = theme === Theme.Default ? Theme.Dark : Theme.Default;
          changeTheme(changeTo);
          setTheme(changeTo);
        }}
        label="Dark Theme"
      />
    </div>
  );
}
