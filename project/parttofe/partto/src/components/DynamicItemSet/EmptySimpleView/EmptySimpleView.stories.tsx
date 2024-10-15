import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { EmptySimpleView } from "./EmptySimpleView";
import { ShellProvider } from "../../../providers/ShellProvider";

const meta: Meta<typeof EmptySimpleView> = {
  component: EmptySimpleView,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof EmptySimpleView>;

export const Simple: Story = {
  args: { content: "Hello World" },
};

export const Long: Story = {
  args: {
    content:
      "I only seem to get sick on weekdays." +
      " I must have a weekend immune system.",
  },
};
