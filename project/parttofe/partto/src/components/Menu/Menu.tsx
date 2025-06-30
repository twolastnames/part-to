import React from "react";

import classes from "./Menu.module.scss";
import { MenuProps } from "./MenuTypes";
import { useRunGet } from "../../api/runget";
import { Spinner } from "../Spinner/Spinner";
import { Accordion } from "../Accordion/Accordion";
import { useParttoGet } from "../../api/parttoget";

const Row = ({ partTo }: { partTo: string }) => {
  const response = useParttoGet({ partTo });
  return (
    <Spinner responses={[response]}>
      <li>{response.data?.name}</li>
    </Spinner>
  );
};

export function Menu({ runState }: MenuProps) {
  const response = useRunGet({ runState });

  return (
    <Spinner responses={[response]}>
      <Accordion summary="Menu">
        <ul data-testid="Menu" className={classes.items}>
          {response.data?.activePartTos?.map((partTo) => (
            <Row partTo={partTo} />
          ))}
        </ul>
      </Accordion>
    </Spinner>
  );
}
