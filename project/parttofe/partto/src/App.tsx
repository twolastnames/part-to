import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { JobGet } from "./pages/JobGet";
import { JobPost } from "./pages/JobPost";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="job/:id" element={<JobGet />} />
        <Route path="jobpost" element={<JobPost/>} />
        <Route path="" element={<div>Hello Back</div>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
