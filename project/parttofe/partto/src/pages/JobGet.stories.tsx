import type { Meta, StoryObj } from "@storybook/react";

import { JobGet } from "./JobGet";
import { Stage } from "../api/helpers";

const meta: Meta<typeof JobGet> = {
  component: JobGet,
};
export default meta;

type Story = StoryObj<typeof JobGet>;

export const Fetching: Story = {
  args: {
    useData: () => ({
      stage: Stage.Fetching,
    }),
  },
};

export const WithData: Story = {
  args: {
    useData: () => ({
      stage: Stage.Ok,
      status: 200,
      data: {
        id: "6",
        name: "my Job",
        tasks: ["1", "2"],
      },
    }),
  },
};
