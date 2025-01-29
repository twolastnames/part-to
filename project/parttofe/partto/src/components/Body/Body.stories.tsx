import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Body } from "./Body";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof Body> = {
  component: Body,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Body>;

export const Simple: Story = {
  args: {},
};
