import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Cook } from "../Cook";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Cook />
    </ShellProvider>,
  );
  const page = screen.getByTestId("Layout");
  expect(page).toMatchSnapshot();
});
