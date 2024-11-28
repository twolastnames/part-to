import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { ManageTasks } from "../ManageTasks";
import { LeftContext } from "../../../providers/DynamicItemSetPair";

test("snapshot", () => {
  render(
    <ShellProvider>
      <ManageTasks
        context={LeftContext}
        emptyText="Empty Yo"
        tasks={["a", "task", "list"]}
        runState="aRunState"
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("ManageTasks");
  expect(component).toMatchSnapshot();
});
