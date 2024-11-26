import React from "react";
import { Layout } from "../../components/Layout/Layout";
import { useParttosGet } from "../../api/parttosget";
import { EmptySimpleView } from "../../components/DynamicItemSet/EmptySimpleView/EmptySimpleView";
import { DynamicItemSet } from "../../components/DynamicItemSet/DynamicItemSet";
import { SelectPartTos } from "../../components/SelectPartTos/SelectPartTos";
import { Spinner } from "../../components/Spinner/Spinner";
import { RightContext } from "../../providers/DynamicItemSetPair";

const secondPairEmptyText = [
  "Select recipes from the left with the arrow",
  "button to put a meal together.",
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
