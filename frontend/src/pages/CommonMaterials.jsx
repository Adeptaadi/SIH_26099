import React, { useEffect, useState } from 'react';
import { Database, Layers, CheckCircle2, Search, ArrowRight } from 'lucide-react';
import { getCommonMaterials } from '../services/api';

export default function CommonMaterials() {
  const [commonMaterials, setCommonMaterials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchCMs = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCommonMaterials();
      setCommonMaterials(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCMs();
  }, []);

  const filteredCMs = commonMaterials.filter((cm) => {
    return (
      searchQuery === '' ||
      cm.common_material_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cm.canonical_description.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Canonical Common Material Master</h1>
        <p className="page-subtitle">
          Approved harmonized master records unifying duplicate materials across enterprise catalogs.
        </p>
      </div>

      {/* Filter bar */}
      <div className="card" style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <Search size={18} color="var(--text-muted)" />
        <input
          type="text"
          placeholder="Filter common materials by ID or canonical description..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{ background: 'transparent', border: 'none', color: 'var(--text-main)', outline: 'none', width: '100%', fontSize: '0.925rem' }}
        />
      </div>

      {loading ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: 'var(--text-muted)' }}>Loading canonical master catalog...</p>
        </div>
      ) : error ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem', color: 'var(--danger)' }}>
          <p>Failed to load common materials: {error}</p>
        </div>
      ) : filteredCMs.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <Database size={48} color="var(--text-muted)" style={{ marginBottom: '1rem' }} />
          <h3 style={{ color: 'var(--text-heading)', marginBottom: '0.5rem' }}>No Approved Common Materials Yet</h3>
          <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
            Approve equivalent candidate matches in the Dashboard or Match Inspection to generate canonical records.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {filteredCMs.map((cm) => (
            <div key={cm.common_material_id} className="card" style={{ borderLeft: '4px solid var(--success)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                <div>
                  <span className="badge badge-approved" style={{ marginBottom: '0.5rem' }}>
                    <CheckCircle2 size={12} /> {cm.common_material_id}
                  </span>
                  <h3 style={{ color: 'var(--text-heading)', fontSize: '1.2rem', marginTop: '0.25rem' }}>
                    {cm.canonical_description}
                  </h3>
                </div>
              </div>

              {/* Source Records Mapping */}
              <div style={{ background: 'var(--bg-input)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>
                  Unified Source Records ({cm.source_materials?.length || 0})
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '0.75rem' }}>
                  {cm.source_materials && cm.source_materials.map((src, idx) => (
                    <div key={idx} style={{ background: 'var(--bg-card)', padding: '0.75rem', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                        <span style={{ fontWeight: 700, color: 'var(--primary)', fontSize: '0.85rem' }}>{src.organization_id}</span>
                        <span style={{ fontWeight: 600, color: 'var(--text-heading)', fontSize: '0.85rem' }}>ID: {src.material_id}</span>
                      </div>
                      {src.description && (
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {src.description}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
