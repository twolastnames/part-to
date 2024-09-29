import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ParttoPost200Body, doParttoPost } from "../../api/parttopost";
import { getDuration } from "../../api/helpers";
//import { Button } from "@mantine/core";
import { Button } from "../../components/Button/Button";

const payload = {
  part_to: {
    name: "Corn on the Cob",
    depends: ["remove_from_heat"],
  },
  tasks: [
    {
      name: "wash_corn",
      duration: getDuration(1000),
      description: "wash the corn",
      ingredients: ["cobbed corn"],
    },
    {
      name: "half_cobs",
      duration: getDuration(2000),
      description:
        "cut partially with kitchen shears to weaken cob middle to break in half",
      tools: ["kitchen shears"],
      depends: ["wash_corn"],
    },
    {
      name: "boil_water",
      duration: getDuration(8000),
      description: "boil water in large pot",
      tools: ["large pot"],
      engagement: 2,
    },
    {
      name: "boil",
      duration: getDuration(4000),
      description: "put corn in and boil",
      engagement: 4,
      depends: ["boil_water", "half_cobs"],
    },
    {
      name: "remove_from_heat",
      duration: getDuration(600),
      description: "remove from heat",
      depends: ["boil"],
    },
  ],
};

export const JobPost = () => {
  const navigate = useNavigate();
  const response = useState<ParttoPost200Body | undefined>();
  if (!response) {
    return <div>Loading...</div>;
  }
  return (
    <div>
      <textarea rows={20} cols={60}></textarea>
      <Button
        onClick={() => {
          console.log();
          doParttoPost({
            body: payload,
            on200: ({ id }) => {
              navigate(`/job/${id}`);
            },
          });
        }}
      >
        Post Job
      </Button>
    </div>
  );
};
