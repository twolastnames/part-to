import React, { useState } from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { DynamicItemSet } from "../DynamicItemSet";
import { ChefHat } from "../../Icon/Icon";
import { Item } from "../DynamicItemSetTypes";
import { LeftContext } from "../../../providers/DynamicItemSetPair";

const ItemSet = () => {
  const [items, setItems] = useState<Array<Item>>(
    Array.from(new Array(9)).map((_, index) => ({
      key: index.toString(),
      listView: <div>List View {index}</div>,
      detailView: <div>Detail View {index}</div>,
      itemOperations: [
        {
          text: `Delete Item ${index}`,
          icon: ChefHat,
          onClick: () => {
            setItems((items) =>
              items.filter(({ key }) => key !== index.toString()),
            );
          },
        },
      ],
    })),
  );

  return (
    <DynamicItemSet
      context={LeftContext}
      key={items.length.toString()}
      items={items}
      setOperations={[]}
      emptyPage={<div>Empty</div>}
    />
  );
};

test("snapshot", async () => {
  render(
    <ShellProvider>
      <ItemSet />
    </ShellProvider>,
  );
  expect(screen.getByTestId("DynamicItemSet")).toMatchSnapshot();
  expect(await waitFor(() => screen.findByText("Detail View 0"))).toBeTruthy();
  (await waitFor(() => screen.findByLabelText("Forward One"))).click();
  expect(await waitFor(() => screen.findByText("Detail View 1"))).toBeTruthy();
  (await waitFor(() => screen.findByLabelText("Forward One"))).click();
  expect(await waitFor(() => screen.findByText("Detail View 2"))).toBeTruthy();
  (await waitFor(() => screen.findByLabelText("Forward One"))).click();
  expect(await waitFor(() => screen.findByText("Detail View 3"))).toBeTruthy();
  (await waitFor(() => screen.findByLabelText("Forward One"))).click();
  expect(await waitFor(() => screen.findByText("Detail View 4"))).toBeTruthy();
  (await waitFor(() => screen.findByLabelText("Forward One"))).click();
  expect(await waitFor(() => screen.findByText("Detail View 5"))).toBeTruthy();
  expect(screen.getByTestId("DynamicItemSet")).toMatchSnapshot();
  const deleter = await waitFor(() => screen.findByLabelText("Delete Item 5"));
  await deleter.click();
  expect(await waitFor(() => screen.findByText("Detail View 6"))).toBeTruthy();
  expect(
    await waitFor(() => screen.findByLabelText("Delete Item 6")),
  ).toBeTruthy();
  expect(screen.getByTestId("DynamicItemSet")).toMatchSnapshot();
});
