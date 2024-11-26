import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Detail } from "../Detail";
import { LeftContext } from "../../../../../providers/DynamicItemSetPair";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Detail
        context={LeftContext}
        items={[
          {
            key: "9",
            listView: <div>hello</div>,
            detailView: <div>hello</div>,
            itemOperations: [],
          },
          {
            key: "6",
            listView: <div>hello</div>,
            detailView: <div>hello</div>,
            itemOperations: [],
          },
        ]}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Detail");
  expect(component).toMatchSnapshot();
});
