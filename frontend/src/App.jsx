import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles.css';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Exams from './pages/Exams';
import ExamDetail from './pages/ExamDetail';
import Result from './pages/Result'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/exams/" element={<Exams />} />
        <Route path="/exams/:id" element={<ExamDetail />} />
        <Route path="/result/:id" element={<Result />} />
      </Routes>
    </Router>
  );
}

export default App;
