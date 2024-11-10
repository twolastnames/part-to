import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Noted } from "./Noted";
import { ShellProvider } from "../../../../providers/ShellProvider";

const meta: Meta<typeof Noted> = {
  component: Noted,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Noted>;

export const Simple: Story = {
  args: {},
};
