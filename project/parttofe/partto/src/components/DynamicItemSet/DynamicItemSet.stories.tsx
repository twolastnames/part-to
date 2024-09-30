import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { DynamicItemSet } from "./DynamicItemSet";
import { ShellProvider } from "../../ShellProvider";
import { Next, Start } from "../Icon/Icon";

const meta: Meta<typeof DynamicItemSet> = {
  component: DynamicItemSet,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof DynamicItemSet>;

export const Empty: Story = {
  args: {
    items: [],
    setOperations: [
      {
        icon: Start,
        text: "start cooking",
        onClick: () => console.log("clicked"),
      },
      {
        icon: Next,
        text: "mark complete",
        onClick: () => console.log("clicked"),
      },
    ],
    emptyPage: <div>Empty Yo</div>,
  },
};

export const Single: Story = {
  args: {
    items: [
      {
        listView: <div>Should never see this</div>,
        detailView: <div>This is a detail view</div>,
        itemOperations: [
          {
            icon: Start,
            text: "start cooking",
            onClick: () => console.log("clicked"),
          },
          {
            icon: Next,
            text: "mark complete",
            onClick: () => console.log("clicked"),
          },
        ],
      },
    ],
    setOperations: [
      {
        icon: Start,
        text: "start cooking",
        onClick: () => console.log("clicked"),
      },
      {
        icon: Next,
        text: "mark complete",
        onClick: () => console.log("clicked"),
      },
    ],
    emptyPage: <div>Empty Yo</div>,
  },
};
