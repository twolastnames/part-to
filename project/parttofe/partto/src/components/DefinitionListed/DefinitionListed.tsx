import React, { useEffect, useState } from "react";

import {
  DefinitionListedProps,
  ForData,
  ForDatas,
} from "./DefinitionListedTypes";
import { Accordion } from "../Accordion/Accordion";
import { PartToId } from "../../api/sharedschemas";
import { useTaskGet } from "../../api/taskget";
import { useParttoGet } from "../../api/parttoget";
import classes from "./DefinitionListed.module.scss";

export function PartTo({ definitionKey, id }: ForData<PartToId>) {
  const response = useParttoGet({ partTo: id });
  if (!response.data) {
    return <></>;
  }

  return (
    <>
      {response.data.tasks.map((id) => (
        <Definition id={id} definitionKey={definitionKey} />
      ))}
    </>
  );
}

export function Definition({ definitionKey, id }: ForData<PartToId>) {
  const response = useTaskGet({ task: id });
  const value = response?.data?.[definitionKey];
  return (
    <>
      {(Array.isArray(value) ? value : [value]).map((value) => (
        <li className={classes.item}>{value}</li>
      ))}
    </>
  );
}

export function Definitions({ definitionKey, ids }: ForDatas<PartToId>) {
  return (
    <>
      {ids.map((id) => (
        <Definition definitionKey={definitionKey} id={id} />
      ))}
    </>
  );
}

export function DefinitionListed({ summary, children }: DefinitionListedProps) {
  const [noneClassNames, setNoneClassnames] = useState<string>(classes.default);
  const [ulId] = useState<string>(
    `ulId${Math.random().toString().split(".")[1]}`,
  );
  useEffect(() => {
    if (noneClassNames === classes.hidden) {
      return;
    }
    const hasItems = () =>
      (document.querySelector(`#${ulId}`)?.childNodes.length || 0) > 0;
    setTimeout(() => {
      if (
        !hasItems() &&
        noneClassNames !== classes.showing &&
        noneClassNames !== classes.showing
      ) {
        setNoneClassnames(classes.showing);
      }
    }, 600);
    const id = setInterval(() => {
      if (hasItems() && noneClassNames !== classes.hidden) {
        setNoneClassnames(classes.hidden);
      }
    }, 100);
    return () => {
      clearInterval(id);
    };
  });

  return (
    <Accordion summary={summary}>
      <div className={noneClassNames}>None Specified</div>
      <ul className={classes.items} id={ulId}>
        {children}
      </ul>
    </Accordion>
  );
}
