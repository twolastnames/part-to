import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { ThemeSwitch } from "./ThemeSwitch";
import { ShellProvider } from "../../../../ShellProvider";

const meta: Meta<typeof ThemeSwitch> = {
  component: ThemeSwitch,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof ThemeSwitch>;

export const Simple: Story = {
  args: {},
};
