import React, { useEffect, useState } from "react";

import { DefinitionListedProps, ForData } from "./DefinitionListedTypes";
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
  return (
    <>{response?.data?.[definitionKey].map((value) => <li>{value}</li>)}</>
  );
}

export function DefinitionListed({ summary, children }: DefinitionListedProps) {
  const [ulId] = useState<string>(
    `ulId${Math.random().toString().split(".")[1]}`,
  );
  const [noneClassNames, setNoneClassnames] = useState<string>(
    classes.noneSpecified,
  );
  useEffect(() => {
    if (noneClassNames === classes.hidden) {
      return;
    }
    const id = setInterval(() => {
      const ul = document.querySelector(`#${ulId}`);
      if ((ul?.childNodes.length || 0) > 0) {
        setNoneClassnames(classes.hidden);
      }
    }, 500);
    return () => {
      clearInterval(id);
    };
  });

  return (
    <Accordion summary={summary}>
      <div className={noneClassNames}>None Specified</div>
      {<ul id={ulId}>{children}</ul>}
    </Accordion>
  );
}
