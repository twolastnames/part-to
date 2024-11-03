import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { SelectPartTos } from "../SelectPartTos";

test("snapshot", () => {
  render(
    <ShellProvider>
      <SelectPartTos />
    </ShellProvider>,
  );
  const component = screen.getByTestId("DynamicItemSet");
  expect(component).toMatchSnapshot();
});
