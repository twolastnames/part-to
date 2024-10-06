import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../ShellProvider";
import { List } from "../List";
import { Next } from "../../../../Icon/Icon";

test("snapshot", async () => {
  render(
    <ShellProvider>
      <List
        items={[
          {
            listView: <div>hello</div>,
            detailView: <div>goodbye</div>,
            itemOperations: [
              { text: "hello", icon: Next, onClick: () => undefined },
            ],
          },
          {
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
