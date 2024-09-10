import React from "react";
import { Stage, UUID } from "../api/helpers";
import { JobGetResultType, useJobGet } from "../api/api.example";
import { useParams } from "react-router-dom";

const useDefaultDataFetcher = () => {
  const { id } = useParams();
  // shouldn't be here if not in the URL
  const castedId = id as UUID;
  return useJobGet({ id: castedId });
};

export const JobGet = ({ useData }: { useData?: () => JobGetResultType }) => {
  const { data, status, stage } = (useData || useDefaultDataFetcher)();
  if (stage !== Stage.Ok || !data) {
    return <div>Loading...</div>;
  }
  const { name, tasks } = data;
  return (
    <div>
      <div>{status}</div>
      <div>{name}</div>
      {tasks.map((uuid: UUID) => (
        <div>{uuid}</div>
      ))}
    </div>
  );
};
