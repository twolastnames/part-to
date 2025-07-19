import React from "react";

import classes from "./NavigationBar.module.scss";
import { NavigationLogo } from "./NavigationLogo/NavigationLogo";
import { Menu } from "./Menu/Menu";
import { MobileMenu } from "./MobileMenu/MobileMenu";
import { NavigationBarProps } from "./NavigationBarTypes";
import { ThemeSwitch } from "./ThemeSwitch/ThemeSwitch";

export function NavigationBar({ extra }: NavigationBarProps) {
  // TODO: Reintroduce menu with new features
  const haveMenu = !!localStorage.getItem("haveUnfinishedMenu");
  return (
    <div className={classes.navigationBar} data-testid="NavigationBar">
      <div className={classes.nonNotes}>
        {haveMenu && (
          <div className={classes.mobileMenu}>
            <MobileMenu />
          </div>
        )}
        <NavigationLogo />
        {haveMenu && (
          <span className={classes.menu}>
            <Menu />
          </span>
        )}
        <div className={classes.themeSwitch}>
          <ThemeSwitch key={Math.random()} />
        </div>
      </div>
      {extra}
    </div>
  );
}
