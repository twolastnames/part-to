import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { AdjustableDigit } from "./AdjustableDigit";
import { ShellProvider } from "../../../providers/ShellProvider";

const meta: Meta<typeof AdjustableDigit> = {
  component: AdjustableDigit,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof AdjustableDigit>;

export const Simple: Story = {
  args: {
    children: "5",
    decrement: () => {},
    increment: () => {},
  },
};
