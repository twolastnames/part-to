import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Icon } from "./Icon";
import { ShellProvider } from "../../../providers/ShellProvider";

const meta: Meta<typeof Icon> = {
  component: Icon,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Icon>;

export const Simple: Story = {
  args: {},
};
