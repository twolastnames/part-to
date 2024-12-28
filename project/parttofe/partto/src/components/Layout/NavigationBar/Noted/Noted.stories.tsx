import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { addAlarmNote, addErrorNote, Noted } from "./Noted";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { Button } from "../../../Button/Button";
import { ChefHat, Oven } from "../../../Icon/Icon";
import { useTimerProvider } from "../../../../providers/Timer";
import { getDuration } from "../../../../shared/duration";
import { getDateTime } from "../../../../shared/dateTime";
import { Stage } from "../../../../api/helpers";
import { broadcastRunState } from "../../../../shared/runStateMessage";

const useRunState = () => {
  const runState = {
    data: {
      runState: "myRunState",
      duration: getDuration(900000),
      timestamp: getDateTime(),
      complete: getDateTime(),
      activePartTos: [],
      tasks: [],
      duties: [],
      staged: [],
      started: [],
      created: [],
      voided: [],
      completed: [],
      timers: {
        enforced: [
          {
            task: "enforcedId",
            started: getDateTime(),
            duration: getDuration(9000),
          },
        ],
        laxed: [],
        imminent: [],
      },
    },
    stage: Stage.Ok,
  };
  broadcastRunState(runState.data);
  return runState;
};

const TimerPage = () => {
  useRunState();
  const timer = useTimerProvider({ task: "enforcedId" });
  return <>{timer}</>;
};

const meta: Meta<typeof Noted> = {
  component: Noted,
  decorators: (Story) => (
    <ShellProvider>
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
            addAlarmNote({
              key: "enforcedId",
              heading: "my alarm",
              detail: "see it",
            })
          }
        />
        <TimerPage />
      </div>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Noted>;

export const Simple: Story = {
  args: {},
};
