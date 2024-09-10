import React from "react";
import { Stage, UUID } from "../api/helpers";
import { useJobGet } from "../api/api.example";
import { useParams } from "react-router-dom";

export const JobGet = () => {
  const { id } = useParams();
  // shouldn't be here if not in the URL
  const castedId = id as UUID;
  const { data, status, stage } = useJobGet({ id: castedId });
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
