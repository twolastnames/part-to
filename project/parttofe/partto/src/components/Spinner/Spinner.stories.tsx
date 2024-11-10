import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Spinner } from "./Spinner";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof Spinner> = {
  component: Spinner,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Spinner>;

export const Simple: Story = {
  args: {},
};
