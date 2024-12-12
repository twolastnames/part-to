import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Detail } from "./Detail";
import { ShellProvider } from "../../../../providers/ShellProvider";

const meta: Meta<typeof Detail> = {
  component: Detail,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Detail>;

export const Simple: Story = {
  args: {},
};
