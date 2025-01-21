import { ReactNode } from "react";

export interface ForData<ID_TYPE> {
  definitionKey: "ingredients" | "tools" | "description";
  id: ID_TYPE;
}

export interface DefinitionListedProps {
  summary: ReactNode;
  children: ReactNode;
}
