import React, { useEffect, useState } from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle2, XCircle, ArrowRight, Zap, Info } from 'lucide-react';
import { getHardNegatives } from '../services/api';

export default function HardNegativesDemo() {
  const [demos, setDemos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDemos = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getHardNegatives();
      setDemos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDemos();
  }, []);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Hard Negative Overrides Demonstration</h1>
        <p className="page-subtitle">
          Demonstrating why vector similarity search alone fails on industrial specifications, and how critical parameter overrides prevent costly false equivalences.
        </p>
      </div>

      {/* Explanatory Banner */}
      <div className="card" style={{ marginBottom: '2rem', background: 'var(--warning-bg)', border: '1px solid var(--warning)' }}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
          <ShieldAlert size={28} color="var(--warning)" style={{ flexShrink: 0, marginTop: '0.2rem' }} />
          <div>
            <h3 style={{ color: 'var(--warning)', fontSize: '1.1rem', marginBottom: '0.35rem' }}>
              The "Black-Box AI" Trap in Industrial Data
            </h3>
            <p style={{ color: 'var(--text-main)', fontSize: '0.925rem', lineHeight: '1.6' }}>
              Standard LLMs and Sentence Transformers assign <strong>&gt;95% similarity</strong> to descriptions differing by a single grade or pressure rating (e.g. <code>TP304</code> vs <code>TP316</code>). Equating these leads to critical engineering failures. Our system enforces <strong>deterministic parameter override rules</strong> over pure semantic scores.
            </p>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: 'var(--text-muted)' }}>Loading hard negative demonstration cases...</p>
        </div>
      ) : error ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem', color: 'var(--danger)' }}>
          <p>Failed to load demo cases: {error}</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {demos.map((demo) => {
            const semPct = Math.round(demo.semantic_similarity * 100);
            return (
              <div key={demo.match_id} className="card" style={{ borderLeft: '4px solid var(--danger)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span className="badge badge-different">
                      <XCircle size={14} /> CLASSIFICATION: {demo.classification}
                    </span>
                    <span className="badge badge-review">
                      <Zap size={14} /> OVERRIDE TRIGGERED
                    </span>
                  </div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    Test ID: <strong>{demo.match_id}</strong>
                  </div>
                </div>

                {/* Side-by-side materials */}
                <div className="detail-grid" style={{ marginBottom: '1.25rem' }}>
                  <div style={{ background: 'var(--bg-input)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                      <span style={{ fontWeight: 700, color: 'var(--primary)' }}>{demo.material_a.organization_id}</span>
                      <span style={{ fontWeight: 600, color: 'var(--text-heading)' }}>{demo.material_a.material_id}</span>
                    </div>
                    <div style={{ fontFamily: 'monospace', fontSize: '0.9rem', color: 'var(--text-main)' }}>
                      {demo.material_a.description}
                    </div>
                  </div>

                  <div style={{ background: 'var(--bg-input)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                      <span style={{ fontWeight: 700, color: 'var(--accent)' }}>{demo.material_b.organization_id}</span>
                      <span style={{ fontWeight: 600, color: 'var(--text-heading)' }}>{demo.material_b.material_id}</span>
                    </div>
                    <div style={{ fontFamily: 'monospace', fontSize: '0.9rem', color: 'var(--text-main)' }}>
                      {demo.material_b.description}
                    </div>
                  </div>
                </div>

                {/* Conflict Breakdown */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1rem', background: 'var(--bg-card-hover)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                  <div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Semantic Similarity</div>
                    <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--warning)' }}>{semPct}% (High)</div>
                  </div>
                  <div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Critical Technical Mismatch</div>
                    <div style={{ fontWeight: 700, color: 'var(--danger)', fontSize: '0.95rem', marginTop: '0.2rem' }}>
                      {demo.mismatch_reason}
                    </div>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                      {demo.explanation}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
