import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { List } from "../List";
import { Next } from "../../../../Icon/Icon";
import { LeftContext } from "../../../../../providers/DynamicItemSetPair";

test("snapshot", async () => {
  render(
    <ShellProvider>
      <List
        context={LeftContext}
        items={[
          {
            key: "9",
            listView: <div>hello</div>,
            detailView: <div>goodbye</div>,
            itemOperations: [
              { text: "hello", icon: Next, onClick: () => undefined },
            ],
          },
          {
            key: "7",
            listView: <div>hello</div>,
            detailView: <div>goodbye</div>,
            itemOperations: [
              { text: "goodbye", icon: Next, onClick: () => undefined },
            ],
          },
        ]}
      />
    </ShellProvider>,
  );
  const component = await screen.findByTestId("List");
  expect(component).toMatchSnapshot();
});
