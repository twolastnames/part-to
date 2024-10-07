import React from "react";

import classes from "./NavigationLogo.module.scss";
import { Logo } from "../../../Logo/Logo";

export function NavigationLogo() {
  return (
    <div className={classes.navigationLogo}>
      <Logo />
      <div className={classes.navigationLogoText}>
        <div className={classes.navigationLogoTitle}>Part To</div>
        <div className={classes.navigationLogoDescription}>
          Interactive cookbook
        </div>
      </div>
    </div>
  );
}
