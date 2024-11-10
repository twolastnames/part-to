import React, { useEffect, useRef } from "react";

import { Layout } from "../../components/Layout/Layout";
import { useParams } from "react-router-dom";
import { SelectPartTos } from "../../components/SelectPartTos/SelectPartTos";
import { ReviewStagedPartTosIdFromer } from "../../components/ReviewStagedPartTos/ReviewStagedPartTos";
import { RunStateId } from "../../api/sharedschemas";

export function StageMeal() {
  const params = useParams();
  const runState = useRef<RunStateId>(params.runState as RunStateId);
  useEffect(() => {
    runState.current = params.runState as RunStateId;
  }, [params]);
  return (
    <Layout
      pair={[
        <SelectPartTos runState={runState} />,
        <ReviewStagedPartTosIdFromer runState={runState} />,
      ]}
    />
  );
}
