import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { IterationProgress } from "../IterationProgress";
import { ShellProvider } from "../../../../../providers/ShellProvider";

test("snapshot", () => {
  render(
    <ShellProvider>
      <IterationProgress
        setPaused={(arg) => undefined}
        paused={false}
        showDuration={2}
        total={5}
        on={2}
        setShowDuration={(arg: number) => undefined}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("IterationProgress");
  expect(component).toMatchSnapshot();
});
