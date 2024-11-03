import React, { ReactNode } from "react";
// eslint-disable-next-line  @typescript-eslint/no-unused-vars
import classes from "./StartMeal.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useParttosGet } from "../../api/parttosget";
import { EmptySimpleView } from "../../components/DynamicItemSet/EmptySimpleView/EmptySimpleView";
import { Stage } from "../../api/helpers";
import { DynamicItemSet } from "../../components/DynamicItemSet/DynamicItemSet";
import { SelectPartTos } from "../../components/SelectPartTos/SelectPartTos";

export function StartMeal() {
  const allRecipes = useParttosGet();
  const loading = "Loading...";
  const errorMessage: ReactNode | null =
    allRecipes?.stage === Stage.Errored
      ? `Page Load Error: ${allRecipes.status}`
      : null;
  const secondPairEmptyText =
    allRecipes?.stage === Stage.Fetching
      ? loading
      : [
          "Select recipes from the left with the arrow",
          "button to put a meal together.",
        ].join(" ");
  return (
    <Layout
      pair={[
        <SelectPartTos />,
        <DynamicItemSet
          items={[]}
          setOperations={[]}
          emptyPage={
            errorMessage ? (
              <>{errorMessage}</>
            ) : (
              <EmptySimpleView content={secondPairEmptyText} />
            )
          }
        />,
      ]}
    />
  );
}
