import "./App.scss";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { JobGet } from "./pages/JobGet/JobGet";
import { JobPost } from "./pages/JobPost/JobPost";
import { ShellProvider } from "./ShellProvider";

function App() {
  return (
    <ShellProvider>
      <BrowserRouter>
        <Routes>
          <Route path="job/:id" element={<JobGet />} />
          <Route path="jobpost" element={<JobPost />} />
          <Route path="" element={<div>Hello Back</div>} />
        </Routes>
      </BrowserRouter>
    </ShellProvider>
  );
}

export default App;
