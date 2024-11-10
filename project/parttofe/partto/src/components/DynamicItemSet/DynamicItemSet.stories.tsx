import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { DynamicItemSet } from "./DynamicItemSet";
import { ShellProvider } from "../../providers/ShellProvider";
import { Next, Start } from "../Icon/Icon";

const meta: Meta<typeof DynamicItemSet> = {
  component: DynamicItemSet,
  decorators: (Story) => (
    <ShellProvider>
      <div style={{ height: "600px" }}>
        <Story />
      </div>
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
        key: "5",
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

export const Multiple: Story = {
  args: {
    items: [
      {
        key: "6",
        listView: <div>Should see this first</div>,
        detailView: <div>This is a detail view 1</div>,
        itemOperations: [
          {
            icon: Next,
            text: "mark complete",
            onClick: () => console.log("clicked"),
          },
          {
            icon: Start,
            text: "start cooking",
            onClick: () => console.log("clicked"),
          },
        ],
      },
      {
        key: "7",
        listView: <div>Should see this second</div>,
        detailView: <div>This is a detail view 2</div>,
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

export const MultiPageList: Story = {
  args: {
    items: new Array(17).fill(1).map((_, index) => ({
      key: "9",
      listView: <div>Should see this {index}st</div>,
      detailView: <div>This is a detail view {index}</div>,
      itemOperations: [
        {
          icon: Next,
          text: "mark complete",
          onClick: () => console.log("clicked"),
        },
        {
          icon: Start,
          text: "start cooking",
          onClick: () => console.log("clicked"),
        },
      ],
    })),
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
