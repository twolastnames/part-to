import React from "react";

import { Layout } from "../../components/Layout/Layout";
import { useParams } from "react-router-dom";
import { SelectPartTos } from "../../components/SelectPartTos/SelectPartTos";
import { ReviewStagedPartTosIdFromer } from "../../components/ReviewStagedPartTos/ReviewStagedPartTos";

export function StageMeal() {
  const params = useParams();
  return (
    <Layout
      pair={[
        <SelectPartTos runState={params.runState} />,
        <ReviewStagedPartTosIdFromer />,
      ]}
    />
  );
}
