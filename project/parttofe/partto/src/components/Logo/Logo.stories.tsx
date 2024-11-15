import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Logo } from "./Logo";
import { ShellProvider } from "../../providers/ShellProvider";
import { Size } from "./LogoTypes";

const meta: Meta<typeof Logo> = {
  component: Logo,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Logo>;

export const Default: Story = {
  args: {},
};

export const Large: Story = {
  args: { size: Size.Large },
};
