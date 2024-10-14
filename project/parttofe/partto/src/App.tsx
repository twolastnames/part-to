import { ApplicationRouter } from "./Router";
import { ShellProvider } from "./providers/ShellProvider";

function App() {
  return (
    <ShellProvider>
      <ApplicationRouter />
    </ShellProvider>
  );
}

export default App;
