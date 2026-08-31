const API_BASE_URL = 'http://localhost:8000/api';

export async function uploadMaterials(file, organizationId) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('organization_id', organizationId);

  const response = await fetch(`${API_BASE_URL}/materials/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail?.error?.message || 'Failed to upload materials');
  }

  return response.json();
}

export async function runMatching(organizationA = 'ORG_A', organizationB = 'ORG_B') {
  const response = await fetch(`${API_BASE_URL}/matching/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      organization_a: organizationA,
      organization_b: organizationB,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail?.error?.message || 'Matching failed');
  }

  return response.json();
}

export async function getMatches() {
  const response = await fetch(`${API_BASE_URL}/matches`);
  if (!response.ok) {
    throw new Error('Failed to fetch matches');
  }
  return response.json();
}

export async function getMatch(matchId) {
  const response = await fetch(`${API_BASE_URL}/matches/${matchId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch match ${matchId}`);
  }
  return response.json();
}

export async function reviewMatch(matchId, decision) {
  const response = await fetch(`${API_BASE_URL}/matches/${matchId}/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ decision }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail?.error?.message || 'Failed to submit review');
  }

  return response.json();
}

export async function getCommonMaterials() {
  const response = await fetch(`${API_BASE_URL}/common-materials`);
  if (!response.ok) {
    throw new Error('Failed to fetch common materials');
  }
  return response.json();
}

export async function getMaterials(organizationId) {
  const url = organizationId 
    ? `${API_BASE_URL}/materials?organization_id=${encodeURIComponent(organizationId)}`
    : `${API_BASE_URL}/materials`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch materials');
  }
  return response.json();
}
