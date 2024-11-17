import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Timer } from "./Timer";
import { ShellProvider } from "../../providers/ShellProvider";
import { getDateTime } from "../../shared/dateTime";
import { getDuration } from "../../shared/duration";

const meta: Meta<typeof Timer> = {
  component: Timer,
  decorators: (Story) => (
    <ShellProvider>
      <div style={{ width: "400px", height: "420px" }}>
        <Story />
      </div>
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Timer>;

export const Simple: Story = {
  args: {
    start: getDateTime(),
    duration: getDuration(65000),
  },
};

export const Hours: Story = {
  args: {
    start: getDateTime(),
    duration: getDuration(96000000),
  },
};
