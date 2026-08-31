import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Upload from './pages/Upload';
import Dashboard from './pages/Dashboard';
import MatchDetails from './pages/MatchDetails';
import CommonMaterials from './pages/CommonMaterials';

export default function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/matches/:id" element={<MatchDetails />} />
            <Route path="/common-materials" element={<CommonMaterials />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
