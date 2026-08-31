import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { Layers, UploadCloud, LayoutDashboard, Database, CheckCircle2, Sun, Moon } from 'lucide-react';

export default function Navbar() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('sih_theme') || 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('sih_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <nav className="navbar">
      <NavLink to="/dashboard" className="brand">
        <div className="brand-icon">
          <Layers size={20} />
        </div>
        <span>Material Harmonizer</span>
      </NavLink>

      <div className="nav-links">
        <NavLink
          to="/upload"
          className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}
        >
          <UploadCloud size={18} />
          <span>Upload & Match</span>
        </NavLink>

        <NavLink
          to="/dashboard"
          className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}
        >
          <LayoutDashboard size={18} />
          <span>Dashboard</span>
        </NavLink>

        <NavLink
          to="/common-materials"
          className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}
        >
          <Database size={18} />
          <span>Common Materials</span>
        </NavLink>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <button
          className="theme-toggle-btn"
          onClick={toggleTheme}
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          {theme === 'dark' ? (
            <>
              <Sun size={16} color="#f59e0b" />
              <span>Light Mode</span>
            </>
          ) : (
            <>
              <Moon size={16} color="#6366f1" />
              <span>Dark Mode</span>
            </>
          )}
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', color: 'var(--success)', fontWeight: 600 }}>
          <CheckCircle2 size={14} />
          <span>System Online</span>
        </div>
      </div>
    </nav>
  );
}
