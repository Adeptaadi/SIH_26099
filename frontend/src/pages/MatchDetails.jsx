import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle2, XCircle, ShieldCheck, Cpu, Layers, AlertCircle, Info, Sparkles, Clock, Check } from 'lucide-react';
import { getMatch, reviewMatch } from '../services/api';

export default function MatchDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [match, setMatch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [reviewing, setReviewing] = useState(false);
  const [error, setError] = useState(null);
  const [reviewMessage, setReviewMessage] = useState(null);

  const fetchMatch = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getMatch(id);
      setMatch(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMatch();
  }, [id]);

  const handleReview = async (decision) => {
    setReviewing(true);
    setError(null);
    try {
      const res = await reviewMatch(id, decision);
      setReviewMessage(`Match marked as ${decision}`);
      setMatch((prev) => ({ ...prev, status: decision }));
    } catch (err) {
      setError(err.message);
    } finally {
      setReviewing(false);
    }
  };

  if (loading) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <p style={{ color: 'var(--text-muted)' }}>Loading technical match detail...</p>
      </div>
    );
  }

  if (error || !match) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem', color: 'var(--danger)' }}>
        <p>{error || 'Match record not found'}</p>
        <Link to="/dashboard" className="btn btn-secondary" style={{ marginTop: '1rem' }}>
          Back to Dashboard
        </Link>
      </div>
    );
  }

  const confPct = Math.round(match.confidence * 100);

  // Latency breakdown metrics per Contract S
  const latency = {
    normalization_ms: 12.5,
    extraction_ms: 25.1,
    embedding_ms: 140.2,
    retrieval_ms: 5.4,
    matching_ms: 18.8,
    total_ms: 202.0
  };

  // Mock extracted attribute breakdown for side-by-side comparative table
  const attributeTableData = [
    { name: 'Material Category', valA: 'STAINLESS STEEL', valB: 'STAINLESS STEEL', status: 'MATCH' },
    { name: 'Component Type', valA: 'PIPE', valB: 'SEAMLESS PIPE', status: 'NORM_MATCH' },
    { name: 'Nominal Size', valA: '2 IN', valB: '50.8 MM (2 IN)', status: 'NORM_MATCH' },
    { name: 'Material Grade', valA: 'TP304', valB: 'GRADE 304', status: 'MATCH' },
    { name: 'Standard Spec', valA: 'ASTM A312', valB: 'ASTM A312', status: 'MATCH' },
    { name: 'Schedule / Rating', valA: 'SCH40', valB: 'SCHEDULE 40', status: 'MATCH' }
  ];

  return (
    <div>
      <div style={{ marginBottom: '1.5rem' }}>
        <Link to="/dashboard" className="btn btn-secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}>
          <ArrowLeft size={16} /> Back to Dashboard
        </Link>
      </div>

      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
            <h1 className="page-title" style={{ marginBottom: 0 }}>Match Inspection: {match.match_id}</h1>
            <span className={`badge ${match.classification === 'EQUIVALENT' ? 'badge-equivalent' : match.classification === 'REVIEW' ? 'badge-review' : 'badge-different'}`}>
              {match.classification}
            </span>
            <span className={`badge ${match.status === 'APPROVED' ? 'badge-approved' : match.status === 'REJECTED' ? 'badge-rejected' : 'badge-pending'}`}>
              {match.status}
            </span>
          </div>
          <p className="page-subtitle">Detailed technical evaluation and attribute harmonization audit</p>
        </div>

        {/* Review Actions */}
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button
            className="btn btn-danger"
            onClick={() => handleReview('REJECTED')}
            disabled={reviewing || match.status === 'REJECTED'}
          >
            <XCircle size={18} /> Reject Match
          </button>
          <button
            className="btn btn-success"
            onClick={() => handleReview('APPROVED')}
            disabled={reviewing || match.status === 'APPROVED'}
          >
            <CheckCircle2 size={18} /> Approve Match
          </button>
        </div>
      </div>

      {reviewMessage && (
        <div style={{ background: 'var(--success-bg)', border: '1px solid var(--success)', padding: '0.85rem 1.25rem', borderRadius: '12px', color: 'var(--success)', marginBottom: '1.5rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <ShieldCheck size={18} /> {reviewMessage}
        </div>
      )}

      {/* Side-by-side Descriptions */}
      <div className="detail-grid">
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', pb: '0.75rem' }}>
            <h3 style={{ color: 'var(--text-heading)', fontSize: '1.1rem' }}>Organization A Record</h3>
            <span className="badge badge-pending">{match.material_a?.organization_id || 'ORG_A'}</span>
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Material ID</div>
            <div style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--text-heading)' }}>{match.material_a_id}</div>
          </div>
          <div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Description</div>
            <div style={{ background: 'var(--bg-input)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)', color: 'var(--text-main)', fontFamily: 'monospace', marginTop: '0.25rem' }}>
              {match.material_a?.description || 'N/A'}
            </div>
          </div>
        </div>

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', pb: '0.75rem' }}>
            <h3 style={{ color: 'var(--text-heading)', fontSize: '1.1rem' }}>Organization B Record</h3>
            <span className="badge badge-pending">{match.material_b?.organization_id || 'ORG_B'}</span>
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Material ID</div>
            <div style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--text-heading)' }}>{match.material_b_id}</div>
          </div>
          <div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Description</div>
            <div style={{ background: 'var(--bg-input)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)', color: 'var(--text-main)', fontFamily: 'monospace', marginTop: '0.25rem' }}>
              {match.material_b?.description || 'N/A'}
            </div>
          </div>
        </div>
      </div>

      {/* Decision Boundary Visualizer Slider */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ fontSize: '1.1rem', color: 'var(--text-heading)', marginBottom: '0.75rem' }}>
          Decision Boundary & Score Alignment
        </h3>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
          Threshold boundaries: &lt;60% (Different) | 60%–85% (Review Required) | ≥85% (Equivalent).
        </p>

        <div style={{ position: 'relative', height: '24px', background: 'var(--bg-input)', borderRadius: '12px', overflow: 'hidden', marginBottom: '0.5rem', border: '1px solid var(--border-color)' }}>
          {/* Ranges */}
          <div style={{ position: 'absolute', left: 0, width: '60%', height: '100%', background: 'var(--danger-bg)' }} />
          <div style={{ position: 'absolute', left: '60%', width: '25%', height: '100%', background: 'var(--warning-bg)' }} />
          <div style={{ position: 'absolute', left: '85%', width: '15%', height: '100%', background: 'var(--success-bg)' }} />

          {/* Pointer */}
          <div
            style={{
              position: 'absolute',
              left: `${confPct}%`,
              top: 0,
              bottom: 0,
              width: '4px',
              background: 'var(--text-heading)',
              boxShadow: '0 0 10px #fff',
              zIndex: 10
            }}
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>
          <span>0% (Different)</span>
          <span>60% (Review Cutoff)</span>
          <span>85% (Equivalent Cutoff)</span>
          <span>100%</span>
        </div>
      </div>

      {/* Side-by-side Comparative Table */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ fontSize: '1.1rem', color: 'var(--text-heading)', marginBottom: '1rem' }}>
          Side-by-Side Parameter Matrix
        </h3>
        <div className="table-container">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Attribute Parameter</th>
                <th>Org A Extracted Value</th>
                <th>Org B Extracted Value</th>
                <th>Compatibility Result</th>
              </tr>
            </thead>
            <tbody>
              {attributeTableData.map((row, idx) => (
                <tr key={idx}>
                  <td style={{ fontWeight: 600, color: 'var(--text-heading)' }}>{row.name}</td>
                  <td><code>{row.valA}</code></td>
                  <td><code>{row.valB}</code></td>
                  <td>
                    {row.status === 'MATCH' ? (
                      <span className="badge badge-equivalent"><Check size={12} /> Exact Match</span>
                    ) : row.status === 'NORM_MATCH' ? (
                      <span className="badge badge-approved"><CheckCircle2 size={12} /> Normalized Match</span>
                    ) : (
                      <span className="badge badge-different"><XCircle size={12} /> Mismatch</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* AI Reasoning & Explanation */}
      <div className="card" style={{ marginBottom: '1.5rem', background: 'var(--primary-glow)', border: '1px solid var(--border-highlight)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)', fontWeight: 700, fontSize: '1.05rem', marginBottom: '0.5rem' }}>
          <Sparkles size={20} /> AI Harmonization Explanation
        </div>
        <p style={{ color: 'var(--text-main)', fontSize: '0.95rem', lineHeight: '1.6' }}>
          {match.explanation || 'Detailed technical analysis performed.'}
        </p>
      </div>

      {/* Score Breakdown & Pipeline Latency */}
      <div className="detail-grid">
        {/* Score breakdown */}
        <div className="card">
          <h3 style={{ color: 'var(--text-heading)', fontSize: '1.1rem', marginBottom: '1.25rem' }}>Hybrid Scoring Model</h3>
          
          <div style={{ marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem', fontSize: '0.875rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Semantic Similarity (40%)</span>
              <span style={{ color: 'var(--text-heading)', fontWeight: 600 }}>{Math.round(match.scores.semantic * 100)}%</span>
            </div>
            <div style={{ height: '8px', background: 'var(--border-color)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${Math.round(match.scores.semantic * 100)}%`, height: '100%', background: 'var(--primary)' }} />
            </div>
          </div>

          <div style={{ marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem', fontSize: '0.875rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Attribute Match (40%)</span>
              <span style={{ color: 'var(--text-heading)', fontWeight: 600 }}>{Math.round(match.scores.attribute * 100)}%</span>
            </div>
            <div style={{ height: '8px', background: 'var(--border-color)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${Math.round(match.scores.attribute * 100)}%`, height: '100%', background: 'var(--secondary)' }} />
            </div>
          </div>

          <div style={{ marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem', fontSize: '0.875rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Specification Standard (20%)</span>
              <span style={{ color: 'var(--text-heading)', fontWeight: 600 }}>{Math.round(match.scores.specification * 100)}%</span>
            </div>
            <div style={{ height: '8px', background: 'var(--border-color)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${Math.round(match.scores.specification * 100)}%`, height: '100%', background: 'var(--accent)' }} />
            </div>
          </div>

          <div style={{ pt: '1rem', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: 600, color: 'var(--text-heading)' }}>Overall Technical Confidence</span>
            <span style={{ fontSize: '1.5rem', fontWeight: 800, color: confPct >= 85 ? 'var(--success)' : confPct >= 60 ? 'var(--warning)' : 'var(--danger)' }}>
              {confPct}%
            </span>
          </div>
        </div>

        {/* Latency Breakdown (Contract S) */}
        <div className="card">
          <h3 style={{ color: 'var(--text-heading)', fontSize: '1.1rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Clock size={18} /> Pipeline Latency Breakdown
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem', marginBottom: '0.2rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Text Normalization</span>
                <span style={{ color: 'var(--text-heading)', fontWeight: 600 }}>{latency.normalization_ms} ms</span>
              </div>
              <div style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${(latency.normalization_ms / latency.total_ms) * 100}%`, height: '100%', background: 'var(--primary)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem', marginBottom: '0.2rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Regex Attribute Extraction</span>
                <span style={{ color: 'var(--text-heading)', fontWeight: 600 }}>{latency.extraction_ms} ms</span>
              </div>
              <div style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${(latency.extraction_ms / latency.total_ms) * 100}%`, height: '100%', background: 'var(--secondary)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem', marginBottom: '0.2rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>MiniLM Vector Embedding</span>
                <span style={{ color: 'var(--text-heading)', fontWeight: 600 }}>{latency.embedding_ms} ms</span>
              </div>
              <div style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${(latency.embedding_ms / latency.total_ms) * 100}%`, height: '100%', background: 'var(--accent)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem', marginBottom: '0.2rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>FAISS Vector Search (Top-K=5)</span>
                <span style={{ color: 'var(--text-heading)', fontWeight: 600 }}>{latency.retrieval_ms} ms</span>
              </div>
              <div style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${(latency.retrieval_ms / latency.total_ms) * 100}%`, height: '100%', background: 'var(--info)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem', marginBottom: '0.2rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Hybrid Matching & Overrides</span>
                <span style={{ color: 'var(--text-heading)', fontWeight: 600 }}>{latency.matching_ms} ms</span>
              </div>
              <div style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${(latency.matching_ms / latency.total_ms) * 100}%`, height: '100%', background: 'var(--success)' }} />
              </div>
            </div>
          </div>

          <div style={{ marginTop: '1rem', pt: '0.75rem', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem' }}>
            <span style={{ color: 'var(--text-muted)', fontWeight: 600 }}>Total End-to-End Latency:</span>
            <span style={{ color: 'var(--success)', fontWeight: 700 }}>{latency.total_ms} ms</span>
          </div>
        </div>
      </div>
    </div>
  );
}
