from ml.embeddings.embedder import MaterialEmbedder
from ml.retrieval.vector_search import VectorIndex
from ml.matching.matcher import match_materials

def find_matches(materials_a, materials_b):
    """
    Find matches between materials in organization A and organization B.
    Args:
        materials_a (list): list of dicts with 'material_id', 'description'.
        materials_b (list): list of dicts with 'material_id', 'description'.
    Returns:
        matches (list): list of MatchResult dictionaries.
    """
    if not materials_a or not materials_b:
        return []
        
    # 1. Initialize embedder
    # Dimension is 384 for all-MiniLM-L6-v2, but handle fallback dynamically
    # Get a dummy embedding to know the dimension
    embedder = MaterialEmbedder()
    test_emb = embedder.embed(["test"])
    dimension = test_emb.shape[1]
    
    # 2. Embed and Index Organization B
    from ml.normalization.normalizer import normalize_description
    texts_b = [normalize_description(m.get("description", "")) for m in materials_b]
    embeddings_b = embedder.embed(texts_b)
    
    index = VectorIndex(dimension=dimension)
    index.add(embeddings_b)
    
    # 3. Embed Organization A
    texts_a = [normalize_description(m.get("description", "")) for m in materials_a]
    embeddings_a = embedder.embed(texts_a)

    
    # 4. Retrieve Top-K candidates (K=5 or len(materials_b), whichever is smaller)
    k = min(5, len(materials_b))
    distances, indices = index.search(embeddings_a, k=k)
    
    # 5. Perform detailed matching for candidates
    match_results = []
    
    for i, mat_a in enumerate(materials_a):
        emb_a = embeddings_a[i]
        
        # Get candidate indices for this material A
        cand_indices = indices[i]
        
        for rank, idx in enumerate(cand_indices, 1):
            if idx == -1:
                continue
                
            mat_b = materials_b[idx]
            emb_b = embeddings_b[idx]
            
            # Match
            res = match_materials(mat_a, mat_b, emb_a, emb_b)
            # Add rank info (optional, but good for tracking)
            res["rank"] = rank
            
            match_results.append(res)
            
    # Sort match results by confidence descending
    match_results.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    return match_results

