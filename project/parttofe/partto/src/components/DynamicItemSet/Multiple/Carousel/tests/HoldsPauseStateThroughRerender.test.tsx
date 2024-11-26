import React, { useState } from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Carousel } from "../Carousel";
import { LeftContext } from "../../../../../providers/DynamicItemSetPair";
import { Item } from "../../../DynamicItemSetTypes";

let setter: (items: Array<Item>) => void;

const allItems = [
  {
    key: "9",
    detailView: <div>hello</div>,
    listView: <div>hello</div>,
    itemOperations: [],
  },
  {
    key: "7",
    detailView: <div>world</div>,
    listView: <div>world</div>,
    itemOperations: [],
  },
];

const ChangingCarousel = () => {
  const [items, setItems] = useState<Array<Item>>(allItems);
  setter = setItems as (items: Array<Item>) => void;
  return (
    <Carousel
      key={items.length.toString()}
      context={LeftContext}
      items={items}
    />
  );
};

test("holding paused state through rerender", async () => {
  render(
    <ShellProvider>
      <ChangingCarousel />
    </ShellProvider>,
  );
  expect(screen.getByText("hello")).toBeTruthy();
  expect(screen.queryByText("world")).toBeFalsy();
  const pauseButton = screen.getByTitle("Unpaused");
  await pauseButton.click();
  expect(await screen.findByTitle("Paused")).toBeTruthy();
  setter([allItems[1]]);
  let seenPause = false;
  try {
    await waitFor(() => screen.findByTitle("Unpaused"));
    seenPause = true;
  } catch (e) {}
  expect(seenPause).toBeFalsy();
  expect(await screen.findByTitle("Paused")).toBeTruthy();
});
