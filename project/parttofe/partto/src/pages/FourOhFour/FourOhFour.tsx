import React from "react";

import classes from "./FourOhFour.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { Error } from "../../components/Error/Error";

export function FourOhFour() {
  return (
    <Layout
      pair={[
        <Error code={404} />,
        <div className={classes.page}>
          <div>Part</div>
          <div>Fore</div>
          <div>,</div>
          <div>Owe</div>
          <div>Fore</div>
        </div>,
      ]}
    />
  );
}
