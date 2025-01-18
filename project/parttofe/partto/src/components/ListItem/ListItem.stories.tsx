import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { ListItem } from "./ListItem";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof ListItem> = {
  component: ListItem,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof ListItem>;

export const Simple: Story = {
  args: {},
};
