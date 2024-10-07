import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../ShellProvider";
import { Note } from "../Note";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Note />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Note");
  expect(component).toMatchSnapshot();
});
