import React, { ReactNode } from "react";

import { RunStateId } from "../../api/sharedschemas";
import { Stage } from "../../api/helpers";
import { DynamicItemSet } from "../DynamicItemSet/DynamicItemSet";
import { EmptySimpleView } from "../DynamicItemSet/EmptySimpleView/EmptySimpleView";
import { useRunGet } from "../../api/runget";

export interface ReviewStagedPartTosProps {
  runState: RunStateId;
}

export function ReviewStagedPartTos({ runState }: ReviewStagedPartTosProps) {
  const response = useRunGet({ runState });
  const loading = "Loading...";
  const errorMessage: ReactNode | null =
    response?.stage === Stage.Errored
      ? `Page Load Error: ${response.status}`
      : null;
  const secondPairEmptyText =
    response?.stage === Stage.Fetching
      ? loading
      : [
          "Select recipes from the left with the arrow",
          "button to put a meal together.",
        ].join(" ");
  return (
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
    />
  );
}
