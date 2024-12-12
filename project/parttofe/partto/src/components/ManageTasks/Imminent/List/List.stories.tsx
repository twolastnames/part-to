import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { List } from "./List";
import { ShellProvider } from "../../../../providers/ShellProvider";

const meta: Meta<typeof List> = {
  component: List,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof List>;

export const Simple: Story = {
  args: {},
};
