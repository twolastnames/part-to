import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Error } from "../Error";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Error code={500} />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Error");
  expect(component).toMatchSnapshot();
});
