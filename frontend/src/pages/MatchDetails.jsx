import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle2, XCircle, ShieldCheck, Cpu, Layers, AlertCircle, Info, Sparkles } from 'lucide-react';
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
      <div className="card" style={{ textAlign: 'center', padding: '3rem', color: '#ef4444' }}>
        <p>{error || 'Match record not found'}</p>
        <Link to="/dashboard" className="btn btn-secondary" style={{ marginTop: '1rem' }}>
          Back to Dashboard
        </Link>
      </div>
    );
  }

  const confPct = Math.round(match.confidence * 100);

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
        <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid var(--success)', padding: '0.85rem 1.25rem', borderRadius: '12px', color: '#10b981', marginBottom: '1.5rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <ShieldCheck size={18} /> {reviewMessage}
        </div>
      )}

      {/* Side-by-side Descriptions */}
      <div className="detail-grid">
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', pb: '0.75rem' }}>
            <h3 style={{ color: '#fff', fontSize: '1.1rem' }}>Organization A Record</h3>
            <span className="badge badge-pending">{match.material_a?.organization_id || 'ORG_A'}</span>
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Material ID</div>
            <div style={{ fontWeight: 700, fontSize: '1.1rem', color: '#fff' }}>{match.material_a_id}</div>
          </div>
          <div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Description</div>
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)', color: '#f3f4f6', fontFamily: 'monospace', marginTop: '0.25rem' }}>
              {match.material_a?.description || 'N/A'}
            </div>
          </div>
        </div>

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', pb: '0.75rem' }}>
            <h3 style={{ color: '#fff', fontSize: '1.1rem' }}>Organization B Record</h3>
            <span className="badge badge-pending">{match.material_b?.organization_id || 'ORG_B'}</span>
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Material ID</div>
            <div style={{ fontWeight: 700, fontSize: '1.1rem', color: '#fff' }}>{match.material_b_id}</div>
          </div>
          <div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Description</div>
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)', color: '#f3f4f6', fontFamily: 'monospace', marginTop: '0.25rem' }}>
              {match.material_b?.description || 'N/A'}
            </div>
          </div>
        </div>
      </div>

      {/* AI Reasoning & Explanation */}
      <div className="card" style={{ marginBottom: '1.5rem', background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(139, 92, 246, 0.08))', border: '1px solid var(--border-highlight)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)', fontWeight: 700, fontSize: '1.05rem', marginBottom: '0.5rem' }}>
          <Sparkles size={20} /> AI Harmonization Explanation
        </div>
        <p style={{ color: '#fff', fontSize: '0.95rem', lineHeight: '1.6' }}>
          {match.explanation || 'Detailed technical analysis performed.'}
        </p>
      </div>

      {/* Score Components & Attributes */}
      <div className="detail-grid">
        {/* Score breakdown */}
        <div className="card">
          <h3 style={{ color: '#fff', fontSize: '1.1rem', marginBottom: '1.25rem' }}>Hybrid Scoring Model</h3>
          
          <div style={{ marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem', fontSize: '0.875rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Semantic Similarity (40%)</span>
              <span style={{ color: '#fff', fontWeight: 600 }}>{Math.round(match.scores.semantic * 100)}%</span>
            </div>
            <div style={{ height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${Math.round(match.scores.semantic * 100)}%`, height: '100%', background: 'var(--primary)' }} />
            </div>
          </div>

          <div style={{ marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem', fontSize: '0.875rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Attribute Match (40%)</span>
              <span style={{ color: '#fff', fontWeight: 600 }}>{Math.round(match.scores.attribute * 100)}%</span>
            </div>
            <div style={{ height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${Math.round(match.scores.attribute * 100)}%`, height: '100%', background: 'var(--secondary)' }} />
            </div>
          </div>

          <div style={{ marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem', fontSize: '0.875rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Specification Standard (20%)</span>
              <span style={{ color: '#fff', fontWeight: 600 }}>{Math.round(match.scores.specification * 100)}%</span>
            </div>
            <div style={{ height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${Math.round(match.scores.specification * 100)}%`, height: '100%', background: 'var(--accent)' }} />
            </div>
          </div>

          <div style={{ pt: '1rem', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: 600, color: '#fff' }}>Overall Technical Confidence</span>
            <span style={{ fontSize: '1.5rem', fontWeight: 800, color: confPct >= 85 ? 'var(--success)' : confPct >= 60 ? 'var(--warning)' : 'var(--danger)' }}>
              {confPct}%
            </span>
          </div>
        </div>

        {/* Attribute matrix */}
        <div className="card">
          <h3 style={{ color: '#fff', fontSize: '1.1rem', marginBottom: '1rem' }}>Extracted Technical Attributes</h3>
          
          <div style={{ marginBottom: '1.25rem' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Matched Attributes</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {match.matched_attributes && match.matched_attributes.length > 0 ? (
                match.matched_attributes.map((attr) => (
                  <span key={attr} className="badge badge-equivalent" style={{ padding: '0.4rem 0.75rem' }}>
                    <CheckCircle2 size={12} /> {attr}
                  </span>
                ))
              ) : (
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>None matched</span>
              )}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Technical Differences</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {match.differences && match.differences.length > 0 ? (
                match.differences.map((diff, i) => (
                  <span key={i} className="badge badge-different" style={{ padding: '0.4rem 0.75rem' }}>
                    <XCircle size={12} /> {typeof diff === 'string' ? diff : JSON.stringify(diff)}
                  </span>
                ))
              ) : (
                <span style={{ color: 'var(--success)', fontSize: '0.85rem', fontWeight: 500 }}>
                  No technical mismatches detected
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
