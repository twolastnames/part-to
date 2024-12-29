import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { ReviewStagedPartTos } from "./ReviewStagedPartTos";
import { ShellProvider } from "../../providers/ShellProvider";
import { MemoryRouter } from "react-router-dom";

const meta: Meta<typeof ReviewStagedPartTos> = {
  component: ReviewStagedPartTos,
  decorators: (Story) => (
    <ShellProvider>
      <MemoryRouter>
        <Story />
      </MemoryRouter>
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof ReviewStagedPartTos>;

export const Simple: Story = {
  args: {
    taskDefinitions: [],
  },
};
