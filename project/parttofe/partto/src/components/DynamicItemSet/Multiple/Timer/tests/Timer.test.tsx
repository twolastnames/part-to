import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { Timer } from "../Timer";
import { getDateTime, getDuration } from "../../../../../api/helpers";
import { ShellProvider } from "../../../../../ShellProvider";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Timer
        start={getDateTime()}
        duration={getDuration(5000)}
        label="helllo"
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Timer");
  expect(component).toMatchSnapshot();
});
