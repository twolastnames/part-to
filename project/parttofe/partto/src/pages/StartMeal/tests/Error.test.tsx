import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { StartMeal } from "../StartMeal";

test("error", async () => {
  fetchMock.mockResponse(() => {
    return Promise.reject("My Error");
  });
  render(
    <ShellProvider>
      <StartMeal />
    </ShellProvider>,
  );
  await waitFor(() => {
    const found = screen.getByText("0");
    expect(found).toBeTruthy();
  });
  await waitFor(() => {
    const found = screen.getByText(
      "This is bad. There is nothing here. You and your" +
        " family could starve if you expected to cook dinner" +
        " here. They could be saved by navigating to some" +
        " place more useful in the site navigation menu.",
    );
    expect(found).toBeTruthy();
  });
  const page = screen.getByTestId("Layout");
  expect(page).toMatchSnapshot();
});
