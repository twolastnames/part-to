import React, { useEffect } from "react";
import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom";
import { getRoute } from "./routes";
import { StartMeal } from "./pages/StartMeal/StartMeal";

const BaseRedirect = () => {
  const navigate = useNavigate();
  useEffect(() => {
    navigate(getRoute("StartMeal"));
  });
  return <>Redirecting ...</>;
};

export function ApplicationRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path={getRoute("StartMeal")} element={<StartMeal />} />
        <Route path="/" element={<BaseRedirect />} />
      </Routes>
    </BrowserRouter>
  );
}
