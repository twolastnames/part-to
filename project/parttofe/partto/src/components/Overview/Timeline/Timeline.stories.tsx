import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Timeline } from "./Timeline";
import { ShellProvider } from "../../../providers/ShellProvider";

const meta: Meta<typeof Timeline> = {
  component: Timeline,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Timeline>;

export const Simple: Story = {
  args: {},
};
