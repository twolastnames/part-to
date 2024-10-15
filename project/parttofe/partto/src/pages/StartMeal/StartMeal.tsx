import React from "react";
// eslint-disable-next-line  @typescript-eslint/no-unused-vars
import classes from "./StartMeal.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { Notes } from "../../components/Layout/NavigationBar/Notes/Notes";
import { useParttosGet } from "../../api/parttosget";
import { EmptySimpleView } from "../../components/DynamicItemSet/EmptySimpleView/EmptySimpleView";

export function StartMeal() {
  const allRecipes = useParttosGet();
  const firstPairItems = (allRecipes?.data?.partTos || []).map((id) => ({
    listView: <>{id}</>,
    detailView: <>{id}</>,
    itemOperations: [],
  }));
  const noRecipesMessage = [
    'Select "Enter Recipe" from the menu to',
    "put menus in the system.",
  ].join(" ");
  const firstPairEmptyText = allRecipes?.data ? noRecipesMessage : "Loading...";
  const secondPairEmptyText = allRecipes?.data
    ? noRecipesMessage
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
          emptyPage: <EmptySimpleView content={firstPairEmptyText} />,
        },
        {
          items: [],
          setOperations: [],
          emptyPage: <EmptySimpleView content={secondPairEmptyText} />,
        },
      ]}
      extra={<Notes notes={[]} />}
    />
  );
}
