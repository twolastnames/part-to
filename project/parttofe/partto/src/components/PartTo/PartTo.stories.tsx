import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { PartTo } from "./PartTo";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof PartTo> = {
  component: PartTo,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof PartTo>;

export const Simple: Story = {
  args: {
    name: "A simple part to",
    children: (
      <>
        <div>More</div>
        <div>Things</div>
      </>
    ),
  },
};
