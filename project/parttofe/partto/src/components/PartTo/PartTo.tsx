import React from "react";

import { PartToId } from "../../api/sharedschemas";
import { useParttoGet } from "../../api/parttoget";
import { Stage } from "../../api/helpers";
import { PartToProps } from "./PartToTypes";
import {
  DefinitionListed,
  PartTo as DefinitionPartTo,
} from "../DefinitionListed/DefinitionListed";
import { ListItem } from "./ListItem/ListItem";
import { DetailShell } from "../DetailShell/DetailShell";

export function PartToIdFromer({ partTo }: { partTo: PartToId }) {
  const response = useParttoGet({ partTo });
  if (response.stage !== Stage.Ok || !response?.data) {
    return <></>;
  }
  const { workDuration, clockDuration } = response.data;

  return (
    <PartTo
      key={partTo}
      name={<ListItem partTo={partTo} />}
      workDuration={workDuration}
      clockDuration={clockDuration}
    >
      <DefinitionListed summary="Ingredients">
        <DefinitionPartTo definitionKey="ingredients" id={partTo} />
      </DefinitionListed>
      <DefinitionListed summary="Tools">
        <DefinitionPartTo definitionKey="tools" id={partTo} />
      </DefinitionListed>
      <DefinitionListed summary="Tasks">
        <DefinitionPartTo definitionKey="description" id={partTo} />
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
  return <DetailShell name={name}>{children}</DetailShell>;
}
