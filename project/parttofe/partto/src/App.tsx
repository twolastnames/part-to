import React from "react";
import { ApplicationRouter } from "./Router";
import { ShellProvider } from "./providers/ShellProvider";
import classes from "./App.module.scss";

function App() {
  return (
    <ShellProvider>
      <div className={classes.shell}>
        <ApplicationRouter />
      </div>
    </ShellProvider>
  );
}

export default App;
