import React from "react";

import classes from "./NavigationLogo.module.scss";
import { Logo, Size } from "../../../Logo/Logo";

export function NavigationLogo() {
  return (
    <div className={classes.navigationLogo} data-testid="NavigationLogo">
      <span className={classes.mediumLogo}>
        <Logo />
      </span>
      <span className={classes.smallLogo}>
        <Logo size={Size.Small} />
      </span>
      <div className={classes.navigationLogoText}>
        <div className={classes.navigationLogoTitle}>Part To</div>
        <div className={classes.navigationLogoDescription}>
          Interactive cookbook
        </div>
      </div>
    </div>
  );
}
