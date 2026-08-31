import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { LayoutDashboard, CheckCircle2, AlertTriangle, XCircle, Search, Filter, Eye, ArrowRight } from 'lucide-react';
import { getMatches } from '../services/api';

export default function Dashboard() {
  const navigate = useNavigate();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [classificationFilter, setClassificationFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const fetchMatchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getMatches();
      setMatches(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMatchData();
  }, []);

  // Compute metrics
  const totalCount = matches.length;
  const equivalentCount = matches.filter((m) => m.classification === 'EQUIVALENT').length;
  const reviewCount = matches.filter((m) => m.classification === 'REVIEW').length;
  const differentCount = matches.filter((m) => m.classification === 'DIFFERENT').length;

  // Filtered matches
  const filteredMatches = matches.filter((m) => {
    const matchesClassification = classificationFilter === 'ALL' || m.classification === classificationFilter;
    const descA = m.material_a?.description || '';
    const descB = m.material_b?.description || '';
    const matchesSearch =
      searchQuery === '' ||
      m.material_a_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.material_b_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      descA.toLowerCase().includes(searchQuery.toLowerCase()) ||
      descB.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesClassification && matchesSearch;
  });

  const getBadgeClass = (classification) => {
    switch (classification) {
      case 'EQUIVALENT':
        return 'badge-equivalent';
      case 'REVIEW':
        return 'badge-review';
      case 'DIFFERENT':
        return 'badge-different';
      default:
        return 'badge-pending';
    }
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'APPROVED':
        return 'badge-approved';
      case 'REJECTED':
        return 'badge-rejected';
      default:
        return 'badge-pending';
    }
  };

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 className="page-title">Harmonization Dashboard</h1>
          <p className="page-subtitle">
            Overview of AI matched material pairs, confidence scores, and pending reviews.
          </p>
        </div>

        <Link to="/upload" className="btn btn-primary">
          Upload New Inventory
        </Link>
      </div>

      {/* KPI Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon" style={{ background: 'var(--primary-glow)', color: 'var(--primary)' }}>
            <LayoutDashboard size={24} />
          </div>
          <div>
            <div className="metric-val">{totalCount}</div>
            <div className="metric-lbl">Total Candidate Pairs</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{ background: 'var(--success-bg)', color: 'var(--success)' }}>
            <CheckCircle2 size={24} />
          </div>
          <div>
            <div className="metric-val">{equivalentCount}</div>
            <div className="metric-lbl">Equivalent Matches</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{ background: 'var(--warning-bg)', color: 'var(--warning)' }}>
            <AlertTriangle size={24} />
          </div>
          <div>
            <div className="metric-val">{reviewCount}</div>
            <div className="metric-lbl">Requires Review</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon" style={{ background: 'var(--danger-bg)', color: 'var(--danger)' }}>
            <XCircle size={24} />
          </div>
          <div>
            <div className="metric-val">{differentCount}</div>
            <div className="metric-lbl">Clearly Different</div>
          </div>
        </div>
      </div>

      {/* Controls & Filter Bar */}
      <div className="card" style={{ marginBottom: '1.5rem', display: 'flex', flexWrap: 'wrap', gap: '1rem', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'var(--bg-input)', padding: '0.5rem 1rem', borderRadius: '8px', flex: '1', minWidth: '260px' }}>
          <Search size={18} color="var(--text-muted)" />
          <input
            type="text"
            placeholder="Search material description or ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ background: 'transparent', border: 'none', color: 'var(--text-main)', outline: 'none', width: '100%', fontSize: '0.9rem' }}
          />
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Filter size={16} color="var(--text-muted)" />
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Classification:</span>
          {['ALL', 'EQUIVALENT', 'REVIEW', 'DIFFERENT'].map((cat) => (
            <button
              key={cat}
              onClick={() => setClassificationFilter(cat)}
              className={`btn ${classificationFilter === cat ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Results Table */}
      {loading ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: 'var(--text-muted)' }}>Loading harmonization matches...</p>
        </div>
      ) : error ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem', color: 'var(--danger)' }}>
          <p>Failed to load matches: {error}</p>
        </div>
      ) : filteredMatches.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <h3 style={{ color: 'var(--text-heading)', marginBottom: '0.5rem' }}>No Matches Found</h3>
          <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
            Upload inventory files or adjust your classification filter.
          </p>
          <Link to="/upload" className="btn btn-primary">
            Upload CSV Datasets
          </Link>
        </div>
      ) : (
        <div className="table-container">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Material A (Org A)</th>
                <th>Material B (Org B)</th>
                <th>Classification</th>
                <th>Confidence</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredMatches.map((m) => {
                const confPct = Math.round(m.confidence * 100);
                return (
                  <tr key={m.match_id}>
                    <td>
                      <div style={{ fontWeight: 600, color: 'var(--text-heading)' }}>{m.material_a_id}</div>
                      <div style={{ fontSize: '0.825rem', color: 'var(--text-muted)', maxWidth: '280px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {m.material_a?.description || 'N/A'}
                      </div>
                    </td>

                    <td>
                      <div style={{ fontWeight: 600, color: 'var(--text-heading)' }}>{m.material_b_id}</div>
                      <div style={{ fontSize: '0.825rem', color: 'var(--text-muted)', maxWidth: '280px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {m.material_b?.description || 'N/A'}
                      </div>
                    </td>

                    <td>
                      <span className={`badge ${getBadgeClass(m.classification)}`}>
                        {m.classification}
                      </span>
                    </td>

                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                        <div style={{ flex: '1', height: '6px', background: 'var(--border-color)', borderRadius: '3px', overflow: 'hidden', minWidth: '60px' }}>
                          <div
                            style={{
                              width: `${confPct}%`,
                              height: '100%',
                              background: confPct >= 85 ? 'var(--success)' : confPct >= 60 ? 'var(--warning)' : 'var(--danger)',
                              borderRadius: '3px'
                            }}
                          />
                        </div>
                        <span style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--text-heading)' }}>{confPct}%</span>
                      </div>
                    </td>

                    <td>
                      <span className={`badge ${getStatusBadgeClass(m.status)}`}>
                        {m.status}
                      </span>
                    </td>

                    <td>
                      <button
                        className="btn btn-secondary"
                        style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}
                        onClick={() => navigate(`/matches/${m.match_id}`)}
                      >
                        <Eye size={14} />
                        Inspect
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
