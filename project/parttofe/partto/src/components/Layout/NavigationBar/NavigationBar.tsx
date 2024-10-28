import React, { PropsWithChildren, ReactNode } from "react";

import classes from "./NavigationBar.module.scss";
import { NavigationLogo } from "./NavigationLogo/NavigationLogo";
import { Menu } from "./Menu/Menu";
import { MobileMenu } from "./MobileMenu/MobileMenu";

export interface NavigationBarProps extends PropsWithChildren {
  extra: ReactNode;
}

export function NavigationBar({ extra }: NavigationBarProps) {
  return (
    <div className={classes.navigationBar} data-testid="NavigationBar">
      <div className={classes.nonNotes}>
        <div className={classes.mobileMenu}>
          <MobileMenu />
        </div>
        <NavigationLogo />
        <span className={classes.menu}>
          <Menu />
        </span>
      </div>
      {extra}
    </div>
  );
}
