import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { ReviewStagedPartTos } from "../ReviewStagedPartTos";

test("snapshot", () => {
  render(
    <ShellProvider>
      <ReviewStagedPartTos
        taskDefinitions={["Hello", "World"]}
        runState={{ current: "Goodbye" }}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("DynamicItemSet");
  expect(component).toMatchSnapshot();
});
