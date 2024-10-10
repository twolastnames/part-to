import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { MobileMenu } from "./MobileMenu";
import { ShellProvider } from "../../../../providers/ShellProvider";

const meta: Meta<typeof MobileMenu> = {
  component: MobileMenu,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof MobileMenu>;

export const Simple: Story = {
  args: {},
};
