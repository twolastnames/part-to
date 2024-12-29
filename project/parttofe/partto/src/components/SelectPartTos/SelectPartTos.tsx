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
import { PartToId, RunStateId } from "../../api/sharedschemas";
import { useRunGet } from "../../api/runget";
import { SelectPartTosProps } from "./SelectPartTosTypes";
import { LeftContext } from "../../providers/DynamicItemSetPair";

function getFirstPairItems(
  navigate: (arg: string) => void,
  partTos: Array<PartToId>,
  ommittablePartTos: Array<PartToId>,
  runState?: RunStateId,
) {
  return partTos
    .filter((partTo) => !(ommittablePartTos || []).includes(partTo))
    .map((partTo) => ({
      key: partTo,
      listView: <>{partTo}</>,
      detailView: <PartToIdFromer partTo={partTo} />,
      itemOperations: [
        {
          text: "Add to Meal",
          icon: Plus,
          onClick: () =>
            doRunstagePost({
              body: {
                ...(runState ? { runState } : {}),
                partTos: [partTo],
              },
              on200: ({ runState }) =>
                navigate(getRoute("StageMeal", { runState })),
            }),
        },
      ],
    }));
}

const noRecipesMessage = [
  'Select "Enter Recipe" from the menu to',
  "put menus in the system.",
].join(" ");

export function SelectPartTos({ runState }: SelectPartTosProps) {
  const navigate = useNavigate();
  const run = useRunGet(
    { runState: runState as RunStateId },
    { shouldSkip: () => !runState },
  );
  const loading = "Loading...";
  const allRecipes = useParttosGet();
  const errorMessage: ReactNode | null =
    allRecipes?.stage === Stage.Errored
      ? `Page Load Error: ${allRecipes.status}`
      : null;
  const firstPairEmptyText =
    allRecipes?.stage === Stage.Ok ? noRecipesMessage : loading;

  return (
    <DynamicItemSet
      items={getFirstPairItems(
        navigate,
        allRecipes?.data?.partTos || [],
        run?.data?.activePartTos || [],
        runState,
      )}
      context={LeftContext}
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
