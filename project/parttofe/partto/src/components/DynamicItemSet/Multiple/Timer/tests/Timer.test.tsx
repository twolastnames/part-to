import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { Timer } from "../Timer";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { getDateTime } from "../../../../../shared/dateTime";
import { getDuration } from "../../../../../shared/duration";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Timer
        onClick={() => {}}
        title="world"
        start={getDateTime()}
        duration={getDuration(5000)}
        label="helllo"
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Timer");
  expect(component).toMatchSnapshot();
});
