import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { ButtonSet } from "./ButtonSet";
import { ShellProvider } from "../../../ShellProvider";

const meta: Meta<typeof ButtonSet> = {
  component: ButtonSet,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof ButtonSet>;

export const Simple: Story = {
  args: {},
};
