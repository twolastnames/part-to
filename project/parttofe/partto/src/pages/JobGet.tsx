import React from "react";
import { Stage, UUID } from "../api/helpers";
//import { JobGetResultType, useJobGet } from "../api/api.example";
import { useParams } from "react-router-dom";
import { ParttoGetResult, useParttoGet } from "../api/parttoget";
import { PartToId } from "../api/sharedschemas";

const useDefaultDataFetcher = () => {
  const { id } = useParams();
  // shouldn't be here if not in the URL
  const castedId = id as PartToId;
  //  return useJobGet({ id: castedId });
  return useParttoGet({ id: castedId });
};

export const JobGet = ({ useData }: { useData?: () => ParttoGetResult }) => {
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
