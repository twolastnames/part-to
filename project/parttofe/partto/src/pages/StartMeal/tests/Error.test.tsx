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
    const found = screen.getAllByText("Page Load Error: 0");
    expect(found.length).toEqual(2);
  });
  const page = screen.getByTestId("Layout");
  expect(page).toMatchSnapshot();
});
