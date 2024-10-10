import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Note } from "../Note";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Note
        heading="Due North"
        detail="$500 for fancy cars, $20 if it looks like you're poor"
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Note");
  expect(component).toMatchSnapshot();
});
