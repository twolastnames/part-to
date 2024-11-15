import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { NavigationBar } from "./NavigationBar";
import { ShellProvider } from "../../../providers/ShellProvider";

const meta: Meta<typeof NavigationBar> = {
  component: NavigationBar,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof NavigationBar>;

export const Simple: Story = {
  args: {},
};
