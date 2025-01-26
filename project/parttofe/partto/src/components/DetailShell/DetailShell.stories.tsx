import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { DetailShell } from "./DetailShell";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof DetailShell> = {
  component: DetailShell,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof DetailShell>;

export const Simple: Story = {
  args: {},
};
