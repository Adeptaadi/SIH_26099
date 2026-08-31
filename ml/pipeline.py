import time
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
        
    start_total = time.perf_counter()
    
    # 1. Initialize embedder
    embedder = MaterialEmbedder()
    test_emb = embedder.embed(["test"])
    dimension = test_emb.shape[1]
    
    # 2. Normalize and Index B
    start_norm = time.perf_counter()
    from ml.normalization.normalizer import normalize_description
    texts_b = [normalize_description(m.get("description", "")) for m in materials_b]
    
    # 3. Normalize A
    texts_a = [normalize_description(m.get("description", "")) for m in materials_a]
    norm_time_ms = (time.perf_counter() - start_norm) * 1000
    
    # 4. Embed B and A
    start_embed = time.perf_counter()
    embeddings_b = embedder.embed(texts_b)
    embeddings_a = embedder.embed(texts_a)
    embed_time_ms = (time.perf_counter() - start_embed) * 1000
    
    # 5. Build Index and Retrieve (Retrieval Phase)
    start_retrieve = time.perf_counter()
    index = VectorIndex(dimension=dimension)
    index.add(embeddings_b)
    
    # Retrieve Top-K candidates
    k = min(5, len(materials_b))
    distances, indices = index.search(embeddings_a, k=k)
    retrieve_time_ms = (time.perf_counter() - start_retrieve) * 1000
    
    # 6. Perform detailed matching for candidates
    match_results = []
    
    for i, mat_a in enumerate(materials_a):
        emb_a = embeddings_a[i]
        cand_indices = indices[i]
        
        for rank, idx in enumerate(cand_indices, 1):
            if idx == -1:
                continue
                
            mat_b = materials_b[idx]
            emb_b = embeddings_b[idx]
            
            # Match (times extraction and core matching)
            res = match_materials(mat_a, mat_b, emb_a, emb_b)
            res["rank"] = rank
            
            match_results.append(res)
            
    # Sort match results by confidence descending
    match_results.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    
    # 7. Distribute global latencies and structure Contract S block
    num_matches = max(1, len(match_results))
    
    norm_per_match = norm_time_ms / num_matches
    embed_per_match = embed_time_ms / num_matches
    retrieve_per_match = retrieve_time_ms / num_matches
    
    for res in match_results:
        # Extract per-pair timings
        extract_ms = res.pop("extraction_ms", 0.0)
        match_ms = res.pop("matching_ms", 0.0)
        
        # Calculate total latency for this pair
        pair_total_ms = norm_per_match + embed_per_match + retrieve_per_match + extract_ms + match_ms
        
        res["latency"] = {
            "normalization_ms": round(norm_per_match, 2),
            "extraction_ms": round(extract_ms, 2),
            "embedding_ms": round(embed_per_match, 2),
            "retrieval_ms": round(retrieve_per_match, 2),
            "matching_ms": round(match_ms, 2),
            "total_ms": round(pair_total_ms, 2)
        }
        
    return match_results
