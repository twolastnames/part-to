import React, { ReactNode } from "react";

import { Stage } from "../../api/helpers";
import { useParttosGet } from "../../api/parttosget";
import { PartToIdFromer } from "../PartTo/PartTo";
import { DynamicItemSet } from "../DynamicItemSet/DynamicItemSet";
import { EmptySimpleView } from "../DynamicItemSet/EmptySimpleView/EmptySimpleView";
import { Plus } from "../Icon/Icon";
import { useNavigate } from "react-router-dom";
import { getRoute } from "../../routes";
import { doRunstagePost } from "../../api/runstagepost";

export function SelectPartTos() {
  const navigate = useNavigate();
  const loading = "Loading...";
  const noRecipesMessage = [
    'Select "Enter Recipe" from the menu to',
    "put menus in the system.",
  ].join(" ");
  const allRecipes = useParttosGet();
  const firstPairItems = (allRecipes?.data?.partTos || []).map((partTo) => ({
    listView: <>{partTo}</>,
    detailView: <PartToIdFromer partTo={partTo} />,
    itemOperations: [
      {
        text: "Add to Meal",
        icon: Plus,
        onClick: () =>
          doRunstagePost({
            body: { partTos: [partTo] },
            on200: ({ runState }) =>
              navigate(getRoute("StageMeal", { runState })),
          }),
      },
    ],
  }));
  const errorMessage: ReactNode | null =
    allRecipes?.stage === Stage.Errored
      ? `Page Load Error: ${allRecipes.status}`
      : null;
  const firstPairEmptyText =
    allRecipes?.stage === Stage.Ok ? noRecipesMessage : loading;

  return (
    <DynamicItemSet
      items={firstPairItems}
      setOperations={[]}
      emptyPage={
        errorMessage ? (
          <>{errorMessage}</>
        ) : (
          <EmptySimpleView content={firstPairEmptyText} />
        )
      }
    />
  );
}
