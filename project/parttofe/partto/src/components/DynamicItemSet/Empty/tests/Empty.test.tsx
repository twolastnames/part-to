import React from "react";
import { describe, expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { Empty } from "../Empty";

describe("Empty", () => {
  test("snapshot", () => {
    render(<Empty content={<div>Empty</div>} />);
    const component = screen.getByTestId("Empty");
    expect(component).toMatchSnapshot();
  });
});
