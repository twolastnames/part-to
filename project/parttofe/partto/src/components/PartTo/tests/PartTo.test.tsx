import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { PartTo } from "../PartTo";

test("snapshot", () => {
  render(
    <ShellProvider>
      <PartTo name="A simple part to" tasks={["more", "things"]} />
    </ShellProvider>,
  );
  const component = screen.getByTestId("PartTo");
  expect(component).toMatchSnapshot();
});
