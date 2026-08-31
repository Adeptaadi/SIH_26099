import numpy as np
from ml.embeddings.embedder import MaterialEmbedder

def test_embeddings():
    embedder = MaterialEmbedder()
    emb = embedder.embed(["test text 1", "test text 2"])
    
    assert isinstance(emb, np.ndarray)
    assert emb.ndim == 2
    assert emb.shape[0] == 2
    assert emb.shape[1] > 0  # Dimension is positive
    
    # Check L2 normalization
    norms = np.linalg.norm(emb, axis=1)
    for n in norms:
        assert np.isclose(n, 1.0)

