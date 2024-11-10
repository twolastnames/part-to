import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { ReviewStagedPartTos } from "./ReviewStagedPartTos";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof ReviewStagedPartTos> = {
  component: ReviewStagedPartTos,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof ReviewStagedPartTos>;

export const Simple: Story = {
  args: {
    runState: { current: "hello" },
  },
};
