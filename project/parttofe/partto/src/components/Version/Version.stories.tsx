import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Version } from "./Version";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof Version> = {
  component: Version,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Version>;

export const Simple: Story = {
  args: {},
};
