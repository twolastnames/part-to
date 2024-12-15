import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { addAlarmNote, addErrorNote, Noted } from "./Noted";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { MemoryRouter } from "react-router-dom";
import { Button } from "../../../Button/Button";
import { ChefHat, Oven } from "../../../Icon/Icon";

const meta: Meta<typeof Noted> = {
  component: Noted,
  decorators: (Story) => (
    <ShellProvider>
      <MemoryRouter>
        <div style={{ position: "fixed", left: "250px" }}>
          <Button
            icon={Oven}
            text="error note"
            onClick={() =>
              addErrorNote({ heading: "A heading", detail: "some detail" })
            }
          />
          <Button
            icon={ChefHat}
            text="alarm note"
            onClick={() =>
              addAlarmNote({ heading: "my alarm", detail: "see it" })
            }
          />
        </div>
        <Story />
      </MemoryRouter>
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Noted>;

export const Simple: Story = {
  args: {},
};
