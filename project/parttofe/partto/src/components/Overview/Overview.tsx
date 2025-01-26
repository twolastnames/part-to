import React from "react";

import { OverviewProps } from "./OverviewTypes";
import { Item } from "../DynamicItemSet/DynamicItemSetTypes";
import { useRunGet } from "../../api/runget";
import { Spinner } from "../Spinner/Spinner";
import {
  DefinitionListed,
  Definitions,
} from "../DefinitionListed/DefinitionListed";
import { DetailShell } from "../DetailShell/DetailShell";
import { Overview as OverviewIcon } from "../Icon/Icon";
import { ListItem } from "../ListItem/ListItem";
import { Timeline } from "./Timeline/Timeline";

const listView = (
  <ListItem precursor={<OverviewIcon />} description="Overview" />
);

export function Overview({ runState }: OverviewProps) {
  const response = useRunGet({ runState });
  const staged = response?.data?.staged || [];
  return (
    <Spinner responses={[response]}>
      <DetailShell name={listView}>
        <Timeline runState={runState} />
        <DefinitionListed summary="Ingredients">
          <Definitions definitionKey="ingredients" ids={staged} />
        </DefinitionListed>
        <DefinitionListed summary="Tools">
          <Definitions definitionKey="tools" ids={staged} />
        </DefinitionListed>
        <DefinitionListed summary="Tasks">
          <Definitions definitionKey="description" ids={staged} />
        </DefinitionListed>
      </DetailShell>
    </Spinner>
  );
}

export function asItem({ runState }: OverviewProps): Item {
  return {
    key: runState,
    listView,
    detailView: <Overview runState={runState} />,
    itemOperations: [],
  };
}
