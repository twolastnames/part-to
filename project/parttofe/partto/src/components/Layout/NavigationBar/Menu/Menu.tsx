import React from "react";

import classes from "./Menu.module.scss";
import { NavLink } from "@mantine/core";
import { Book, ChefHat, Icon, Oven, Settings } from "../../../Icon/Icon";
import { ThemeSwitch } from "../ThemeSwitch/ThemeSwitch";

export function Menu() {
  return (
    <>
      <nav data-testid="Menu" className={classes.nav}>
        <NavLink
          key={Math.random()}
          className={classes.navLink}
          label={<div className={classes.text}>Enter Recipe</div>}
          leftSection={<Icon definition={ChefHat} />}
        />
        <NavLink
          key={Math.random()}
          className={classes.navLink}
          label={<div className={classes.text}>Start Meal</div>}
          leftSection={<Icon definition={Book} />}
        />
        <NavLink
          key={Math.random()}
          className={classes.navLink}
          label={<div className={classes.text}>Continue Cooking</div>}
          leftSection={<Icon definition={Oven} />}
        />
        <NavLink
          key={Math.random()}
          className={classes.navLink}
          label={<div className={classes.text}>Settings</div>}
          leftSection={<Icon definition={Settings} />}
        />
      </nav>
      <ThemeSwitch key={Math.random()} />
    </>
  );
}
