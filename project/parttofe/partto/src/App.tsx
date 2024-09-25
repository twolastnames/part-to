import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { JobGet } from "./pages/JobGet/JobGet";
import { JobPost } from "./pages/JobPost/JobPost";
import { MantineProvider } from "@mantine/core";
import '@mantine/core/styles.layer.css';

function App() {
  return (
    <MantineProvider>
      <BrowserRouter>
        <Routes>
          <Route path="job/:id" element={<JobGet />} />
          <Route path="jobpost" element={<JobPost />} />
          <Route path="" element={<div>Hello Back</div>} />
        </Routes>
      </BrowserRouter>
    </MantineProvider>
  );
}

export default App;
