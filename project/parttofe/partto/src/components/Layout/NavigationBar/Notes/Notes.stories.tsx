import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Notes } from "./Notes";
import { ShellProvider } from "../../../../ShellProvider";

const meta: Meta<typeof Notes> = {
  component: Notes,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Notes>;

export const Simple: Story = {
  args: {},
};