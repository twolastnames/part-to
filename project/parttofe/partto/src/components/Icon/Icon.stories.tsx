import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Icon, Next } from "./Icon";
import { ShellProvider } from "../../providers/ShellProvider";
import { Size } from "./IconTypes";

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

export const Medium: Story = {
  args: { definition: Next },
};

export const Small: Story = {
  args: { definition: Next, size: Size.Small },
};

export const Large: Story = {
  args: { definition: Next, size: Size.Large },
};

export const ExtraLarge: Story = {
  args: { definition: Next, size: Size.ExtraLarge },
};
