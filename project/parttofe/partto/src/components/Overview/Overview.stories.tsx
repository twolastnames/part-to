import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Overview } from "./Overview";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof Overview> = {
  component: Overview,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Overview>;

export const Simple: Story = {
  args: {},
};
