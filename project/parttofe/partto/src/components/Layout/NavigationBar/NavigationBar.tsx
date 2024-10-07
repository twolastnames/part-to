import React from "react";

import classes from "./NavigationBar.module.scss";
import { NavLink } from "@mantine/core";
import { ChefHat, Icon, Oven } from "../../Icon/Icon";
import { NavigationLogo } from "./NavigationLogo/NavigationLogo";
import { Note, NoteProps } from "./Note/Note";
import { ThemeSwitch } from "./ThemeSwitch/ThemeSwitch";

export interface NavigationBarProps {
  notes: Array<NoteProps>;
}

export function NavigationBar({ notes }: NavigationBarProps) {
  return (
    <div className={classes.navigationBar}>
      <div className={classes.nonNotes}>
        <NavigationLogo />
        <nav data-testid="NavigationBar">
          <NavLink
            className={classes.navLink}
            label="Start Run"
            leftSection={<Icon definition={ChefHat} />}
          />
          <NavLink
            className={classes.navLink}
            label="Continue Cooking"
            leftSection={<Icon definition={Oven} />}
          />
        </nav>
        <ThemeSwitch />
      </div>
      <div className={classes.notes}>
        {notes.map((note) => (
          <Note {...note} />
        ))}
      </div>
    </div>
  );
}
