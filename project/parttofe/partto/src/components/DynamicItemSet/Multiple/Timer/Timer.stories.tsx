import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Timer } from "./Timer";
import { ShellProvider } from "../../../../ShellProvider";

const meta: Meta<typeof Timer> = {
  component: Timer,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Timer>;

export const Simple: Story = {
  args: {},
};
