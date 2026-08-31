import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, Play, CheckCircle, AlertCircle, FileText, Sparkles, RefreshCw } from 'lucide-react';
import { uploadMaterials, runMatching } from '../services/api';

export default function Upload() {
  const navigate = useNavigate();

  const [fileA, setFileA] = useState(null);
  const [fileB, setFileB] = useState(null);

  const [uploadStatusA, setUploadStatusA] = useState(null);
  const [uploadStatusB, setUploadStatusB] = useState(null);

  const [loadingA, setLoadingA] = useState(false);
  const [loadingB, setLoadingB] = useState(false);
  const [matchingLoading, setMatchingLoading] = useState(false);

  const [error, setError] = useState(null);
  const [matchResult, setMatchResult] = useState(null);

  const handleFileUpload = async (file, orgId, setStatus, setLoading) => {
    if (!file) return;
    setError(null);
    setLoading(true);
    try {
      const res = await uploadMaterials(file, orgId);
      setStatus(res);
    } catch (err) {
      setError(`[${orgId}] ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRunMatching = async () => {
    setError(null);
    setMatchingLoading(true);
    try {
      const res = await runMatching('ORG_A', 'ORG_B');
      setMatchResult(res);
      setTimeout(() => {
        navigate('/dashboard');
      }, 1200);
    } catch (err) {
      setError(err.message);
    } finally {
      setMatchingLoading(false);
    }
  };

  const handleLoadSamples = async () => {
    setError(null);
    setLoadingA(true);
    setLoadingB(true);
    try {
      const sampleAContent = `material_id,description\nA001,SS PIPE 2 IN SCH40 ASTM A312 TP304\nA002,CARBON STEEL VALVE GATE 3 IN 150# RF FLANGED\nA003,BALL BEARING 6205-2RS 25MM BORE\nA004,HEX BOLT M12 X 50MM SS304\nA005,COPPER CABLE 3 CORE 2.5 SQMM XLPE`;
      const sampleBContent = `material_id,description\nB001,STAINLESS STEEL SEAMLESS PIPE 50.8MM SCHEDULE 40 ASTM A312 GRADE 304\nB002,CS GATE VALVE 3 INCH CLASS 150 RF FLANGED\nB003,DEEP GROOVE BALL BEARING 6205 2RS\nB004,HEXAGONAL HEAD BOLT M12X50 STAINLESS 304\nB005,COPPER POWER CABLE 3C X 2.5 SQ MM ARMOURED`;

      const fileAObj = new File([sampleAContent], 'organization_a.csv', { type: 'text/csv' });
      const fileBObj = new File([sampleBContent], 'organization_b.csv', { type: 'text/csv' });

      setFileA(fileAObj);
      setFileB(fileBObj);

      const resA = await uploadMaterials(fileAObj, 'ORG_A');
      setUploadStatusA(resA);

      const resB = await uploadMaterials(fileBObj, 'ORG_B');
      setUploadStatusB(resB);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingA(false);
      setLoadingB(false);
    }
  };

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 className="page-title">Upload Material Inventories</h1>
          <p className="page-subtitle">
            Upload CSV datasets from two organizations to normalize, extract attributes, and run AI harmonization.
          </p>
        </div>

        <button className="btn btn-secondary" onClick={handleLoadSamples} disabled={loadingA || loadingB}>
          <Sparkles size={16} />
          Load Demo Datasets
        </button>
      </div>

      {error && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.15)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          color: '#ef4444',
          padding: '1rem',
          borderRadius: '12px',
          marginBottom: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem'
        }}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      <div className="dropzone-grid">
        {/* Organization A */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1.1rem', color: '#fff' }}>Organization A Dataset</h3>
            <span className="badge badge-pending">ORG_A</span>
          </div>

          <label className="dropzone" style={{ display: 'block' }}>
            <input
              type="file"
              accept=".csv"
              style={{ display: 'none' }}
              onChange={(e) => {
                const file = e.target.files[0];
                if (file) {
                  setFileA(file);
                  handleFileUpload(file, 'ORG_A', setUploadStatusA, setLoadingA);
                }
              }}
            />
            <UploadCloud size={36} color="#6366f1" style={{ marginBottom: '0.75rem' }} />
            <p style={{ fontWeight: 600, color: '#fff', marginBottom: '0.25rem' }}>
              {fileA ? fileA.name : 'Click or Drop CSV File for Org A'}
            </p>
            <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
              Required columns: <code>material_id</code>, <code>description</code>
            </p>
          </label>

          {loadingA && (
            <p style={{ marginTop: '0.75rem', fontSize: '0.875rem', color: 'var(--primary)' }}>
              Uploading & validating...
            </p>
          )}

          {uploadStatusA && (
            <div style={{ marginTop: '1rem', background: 'rgba(16, 185, 129, 0.08)', border: '1px solid rgba(16, 185, 129, 0.2)', padding: '0.75rem', borderRadius: '8px', fontSize: '0.85rem' }}>
              <div style={{ color: '#10b981', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.25rem' }}>
                <CheckCircle size={15} /> Uploaded Successfully
              </div>
              <div>Processed: <strong>{uploadStatusA.records_processed}</strong> records | Rejected: {uploadStatusA.records_rejected}</div>
            </div>
          )}
        </div>

        {/* Organization B */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1.1rem', color: '#fff' }}>Organization B Dataset</h3>
            <span className="badge badge-pending">ORG_B</span>
          </div>

          <label className="dropzone" style={{ display: 'block' }}>
            <input
              type="file"
              accept=".csv"
              style={{ display: 'none' }}
              onChange={(e) => {
                const file = e.target.files[0];
                if (file) {
                  setFileB(file);
                  handleFileUpload(file, 'ORG_B', setUploadStatusB, setLoadingB);
                }
              }}
            />
            <UploadCloud size={36} color="#8b5cf6" style={{ marginBottom: '0.75rem' }} />
            <p style={{ fontWeight: 600, color: '#fff', marginBottom: '0.25rem' }}>
              {fileB ? fileB.name : 'Click or Drop CSV File for Org B'}
            </p>
            <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
              Required columns: <code>material_id</code>, <code>description</code>
            </p>
          </label>

          {loadingB && (
            <p style={{ marginTop: '0.75rem', fontSize: '0.875rem', color: 'var(--accent)' }}>
              Uploading & validating...
            </p>
          )}

          {uploadStatusB && (
            <div style={{ marginTop: '1rem', background: 'rgba(16, 185, 129, 0.08)', border: '1px solid rgba(16, 185, 129, 0.2)', padding: '0.75rem', borderRadius: '8px', fontSize: '0.85rem' }}>
              <div style={{ color: '#10b981', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.25rem' }}>
                <CheckCircle size={15} /> Uploaded Successfully
              </div>
              <div>Processed: <strong>{uploadStatusB.records_processed}</strong> records | Rejected: {uploadStatusB.records_rejected}</div>
            </div>
          )}
        </div>
      </div>

      {/* Action Footer */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <FileText size={22} color="var(--text-muted)" />
          <div>
            <div style={{ fontWeight: 600, color: '#fff' }}>Harmonization Engine Ready</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Runs Normalization → Attribute Extraction → Hybrid Match Pipeline
            </div>
          </div>
        </div>

        <button
          className="btn btn-primary"
          style={{ padding: '0.85rem 2rem', fontSize: '1rem' }}
          onClick={handleRunMatching}
          disabled={matchingLoading || (!uploadStatusA && !uploadStatusB)}
        >
          {matchingLoading ? (
            <>
              <RefreshCw size={18} className="spin" style={{ animation: 'spin 1s linear infinite' }} />
              Running Matching Engine...
            </>
          ) : (
            <>
              <Play size={18} />
              Run AI Matching
            </>
          )}
        </button>
      </div>

      {matchResult && (
        <div style={{ marginTop: '1.5rem', background: 'rgba(99, 102, 241, 0.15)', border: '1px solid var(--primary)', padding: '1rem 1.5rem', borderRadius: '12px', color: '#fff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>Matching Completed!</div>
            <div>Found <strong>{matchResult.matches_found}</strong> candidate pairs. Redirecting to dashboard...</div>
          </div>
        </div>
      )}
    </div>
  );
}
