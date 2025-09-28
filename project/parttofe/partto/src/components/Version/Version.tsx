import React from "react";

import classes from "./Version.module.scss";
import { useVersionGet } from "../../api/versionget";
import { Stage } from "../../api/helpers";

export function Version() {
  const response = useVersionGet();
  if (response.stage === Stage.Errored) {
    return <div>Error Getting Version</div>;
  }
  if (response.stage !== Stage.Ok) {
    return <div></div>;
  }
  try {
    const { major, minor, variant, fix, build } = response.data || {};
    return (
      <div
        className={classes.version}
        data-testid="Version"
      >{`Part To: v${major}.${minor}.${fix}.${build}-${variant}`}</div>
    );
  } catch (e) {
    return <div>Error Reading Version</div>;
  }
}
