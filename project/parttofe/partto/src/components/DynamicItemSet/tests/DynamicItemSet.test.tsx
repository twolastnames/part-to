import React from "react";
import { describe, expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { DynamicItemSet } from "../DynamicItemSet";
import { LeftContext } from "../../../providers/DynamicItemSetPair";

describe("DynamicItemSet", () => {
  beforeAll(() => {});

  test("snapshot", () => {
    render(
      <DynamicItemSet
        items={[]}
        context={LeftContext}
        setOperations={[]}
        emptyPage={<div>still empty</div>}
      />,
    );
    const component = screen.getByTestId("DynamicItemSet");
    expect(component).toMatchSnapshot();
  });
});
