import React, { ReactNode } from "react";
// eslint-disable-next-line  @typescript-eslint/no-unused-vars
import classes from "./StartMeal.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { Notes } from "../../components/Layout/NavigationBar/Notes/Notes";
import { useParttosGet } from "../../api/parttosget";
import { EmptySimpleView } from "../../components/DynamicItemSet/EmptySimpleView/EmptySimpleView";
import { Stage } from "../../api/helpers";
import { PartToIdFromer } from "../../components/PartTo/PartTo";

export function StartMeal() {
  const allRecipes = useParttosGet();
  const firstPairItems = (allRecipes?.data?.partTos || []).map((id) => ({
    listView: <>{id}</>,
    detailView: <PartToIdFromer partTo={id} />,
    itemOperations: [],
  }));
  const loading = "Loading...";
  const noRecipesMessage = [
    'Select "Enter Recipe" from the menu to',
    "put menus in the system.",
  ].join(" ");
  const errorMessage: ReactNode | null =
    allRecipes?.stage === Stage.Errored
      ? `Page Load Error: ${allRecipes.status}`
      : null;
  const firstPairEmptyText =
    allRecipes?.stage === Stage.Ok ? noRecipesMessage : loading;
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
        {
          items: firstPairItems,
          setOperations: [],
          emptyPage: errorMessage ? (
            <>{errorMessage}</>
          ) : (
            <EmptySimpleView content={firstPairEmptyText} />
          ),
        },
        {
          items: [],
          setOperations: [],
          emptyPage: errorMessage ? (
            <>{errorMessage}</>
          ) : (
            <EmptySimpleView content={secondPairEmptyText} />
          ),
        },
      ]}
      extra={<Notes notes={[]} />}
    />
  );
}
