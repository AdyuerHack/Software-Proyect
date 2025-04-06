import React from "react";
import { Routes, Route } from "react-router-dom";
import LoginRegister from "./components/LoginRegister";
import Home from "./components/Home"; // Asegúrate de tener este archivo

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginRegister />} />
      <Route path="/home" element={<Home />} />
    </Routes>
  );
}

export default App;
