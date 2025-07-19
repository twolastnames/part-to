import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Flasher } from "./Flasher";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof Flasher> = {
  component: Flasher,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Flasher>;

export const Simple: Story = {
  args: { children: "hello world" },
};
