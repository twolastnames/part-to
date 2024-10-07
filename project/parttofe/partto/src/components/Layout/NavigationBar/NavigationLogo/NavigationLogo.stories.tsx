import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { NavigationLogo } from "./NavigationLogo";
import { ShellProvider } from "../../../../ShellProvider";

const meta: Meta<typeof NavigationLogo> = {
  component: NavigationLogo,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof NavigationLogo>;

export const Simple: Story = {
  args: {},
};
