import React from "react";
import { Layout } from "../../components/Layout/Layout";
import { useParttosGet } from "../../api/parttosget";
import { EmptySimpleView } from "../../components/DynamicItemSet/EmptySimpleView/EmptySimpleView";
import { DynamicItemSet } from "../../components/DynamicItemSet/DynamicItemSet";
import { SelectPartTos } from "../../components/SelectPartTos/SelectPartTos";
import { Spinner } from "../../components/Spinner/Spinner";
import { RightContext } from "../../providers/DynamicItemSetPair";

const secondPairEmptyText = [
  "Select recipes from the first pane with the plus",
  "and add tasks for meal a meal to the second",
  "pane. When all your meal tasks are in the second pane,",
  "click the oven that will appear to start cooking.",
].join(" ");

export function StartMeal() {
  const allRecipes = useParttosGet();
  return (
    <Layout
      pair={[
        <SelectPartTos />,
        <DynamicItemSet
          items={[]}
          context={RightContext}
          setOperations={[]}
          emptyPage={
            <Spinner responses={[allRecipes]}>
              <EmptySimpleView content={secondPairEmptyText} />
            </Spinner>
          }
        />,
      ]}
    />
  );
}
