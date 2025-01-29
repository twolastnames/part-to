import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { TaskTitle } from "./TaskTitle";
import { ShellProvider } from "../../../../providers/ShellProvider";

const meta: Meta<typeof TaskTitle> = {
  component: TaskTitle,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof TaskTitle>;

export const Simple: Story = {
  args: {},
};
