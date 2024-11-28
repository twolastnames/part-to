import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { ManageTasks } from "./ManageTasks";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof ManageTasks> = {
  component: ManageTasks,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof ManageTasks>;

export const Simple: Story = {
  args: {},
};
