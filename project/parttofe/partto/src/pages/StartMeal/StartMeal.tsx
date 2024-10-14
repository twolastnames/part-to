import React from "react";

import classes from "./StartMeal.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { Notes } from "../../components/Layout/NavigationBar/Notes/Notes";

export function StartMeal() {
  return (
    <Layout
      pair={[
        { items: [], setOperations: [], emptyPage: <>WIP: StartMeal 1</> },
        { items: [], setOperations: [], emptyPage: <>WIP: StartMeal 2</> },
      ]}
      extra={<Notes notes={[]} />}
    />
  );
}
