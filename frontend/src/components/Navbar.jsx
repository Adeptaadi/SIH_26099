import React from 'react';
import { NavLink } from 'react-router-dom';
import { Layers, UploadCloud, LayoutDashboard, Database, CheckCircle2 } from 'lucide-react';

export default function Navbar() {
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

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: '#10b981' }}>
        <CheckCircle2 size={14} />
        <span>System Ready</span>
      </div>
    </nav>
  );
}
