import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Accordion } from "./Accordion";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof Accordion> = {
  component: Accordion,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Accordion>;

export const Simple: Story = {
  args: {
    summary: "An Accordian",
    children: (
      <ul>
        <li>Some</li>
        <li>List</li>
      </ul>
    ),
  },
};
