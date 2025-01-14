import React from "react";

import classes from "./PartTo.module.scss";
import { PartToId } from "../../api/sharedschemas";
import { useParttoGet } from "../../api/parttoget";
import { Stage } from "../../api/helpers";
import { PartToProps } from "./PartToTypes";
import { DurationFormat } from "../../shared/duration";
import {
  DefinitionListed,
  PartTo as DefinitionPartTo,
} from "../DefinitionListed/DefinitionListed";

export function PartToIdFromer({ partTo }: { partTo: PartToId }) {
  const response = useParttoGet({ partTo });
  if (response.stage !== Stage.Ok || !response?.data) {
    return <></>;
  }
  const { name, workDuration, clockDuration } = response.data;

  return (
    <PartTo
      key={partTo}
      name={name}
      workDuration={workDuration}
      clockDuration={clockDuration}
    >
      <DefinitionListed summary="Ingredients">
        <DefinitionPartTo definitionKey="ingredients" id={partTo} />
      </DefinitionListed>
      <DefinitionListed summary="Tools">
        <DefinitionPartTo definitionKey="tools" id={partTo} />
      </DefinitionListed>
    </PartTo>
  );
}

export function PartTo({
  name,
  workDuration,
  clockDuration,
  children,
}: PartToProps) {
  return (
    <div className={classes.partTo} data-testid="PartTo">
      <div className={classes.name}>{name}</div>
      <div className={classes.workDuration}>
        {workDuration?.format(DurationFormat.LONG) || ""}
      </div>
      <div className={classes.clockDuration}>
        {clockDuration?.format(DurationFormat.LONG) || ""}
      </div>
      {children}
    </div>
  );
}
