import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { TimerString } from "./TimerString";
import { ShellProvider } from "../../../../providers/ShellProvider";

const meta: Meta<typeof TimerString> = {
  component: TimerString,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof TimerString>;

export const Simple: Story = {
  args: {},
};
