import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { DefinitionListed, PartTo } from "../DefinitionListed";
import task2 from "../../../mocks/task2.json";
import partTo1 from "../../../mocks/partTo1.json";

test("snapshot", () => {
  jest.spyOn(Math, 'random').mockReturnValue(0.123456789);
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/parttos/")) {
      return Promise.resolve(
        JSON.stringify({
          partTos: ["partTo1"],
        }),
      );
    }
    if (request.url.includes("/api/partto/")) {
      return Promise.resolve(JSON.stringify(partTo1));
    }
    if (request.url.includes("/api/task/")) {
      return Promise.resolve(JSON.stringify(task2));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <DefinitionListed summary="Some Summary">
        <PartTo definitionKey="ingredients" id="SomeId" />
      </DefinitionListed>
    </ShellProvider>,
  );
  const component = screen.getByTestId("Accordion");
  expect(component).toMatchSnapshot();
});
