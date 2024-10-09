import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Menu } from "./Menu";
import { ShellProvider } from "../../../../ShellProvider";

const meta: Meta<typeof Menu> = {
  component: Menu,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Menu>;

export const Simple: Story = {
  args: {},
};
