import numpy as np

class VectorIndex:
    def __init__(self, dimension):
        self.dimension = dimension
        self.use_faiss = False
        self.index = None
        self.indexed_embeddings = []
        
        try:
            import faiss
            # Normalize embeddings and use Inner Product for Cosine Similarity
            self.index = faiss.IndexFlatIP(dimension)
            self.use_faiss = True
            print("FAISS index initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize FAISS ({e}). Falling back to NumPy Vector Search.")
            self.indexed_embeddings = []
            
    def add(self, embeddings):
        # Convert to numpy array
        embeddings = np.array(embeddings).astype('float32')
        
        # Ensure L2 normalization
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        normalized_embeddings = embeddings / norms
        
        if self.use_faiss:
            self.index.add(normalized_embeddings)
        else:
            if len(self.indexed_embeddings) == 0:
                self.indexed_embeddings = normalized_embeddings
            else:
                self.indexed_embeddings = np.vstack([self.indexed_embeddings, normalized_embeddings])
                
    def search(self, query_embeddings, k=5):
        query_embeddings = np.array(query_embeddings).astype('float32')
        
        # Ensure L2 normalization of queries
        norms = np.linalg.norm(query_embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        normalized_queries = query_embeddings / norms
        
        num_queries = len(query_embeddings)
        
        if self.use_faiss:
            # FAISS search returns (distances, indices)
            # For IndexFlatIP, distances are inner products (cosine similarity)
            distances, indices = self.index.search(normalized_queries, k)
            return distances, indices
        else:
            # NumPy search
            if len(self.indexed_embeddings) == 0:
                return np.zeros((num_queries, k)), -np.ones((num_queries, k), dtype=int)
                
            distances = []
            indices = []
            
            for q in normalized_queries:
                # Compute inner product (cosine similarity)
                scores = np.dot(self.indexed_embeddings, q)
                # Sort descending
                top_indices = np.argsort(scores)[::-1][:k]
                top_scores = scores[top_indices]
                
                # If we have fewer than k items, pad with -1 / 0.0
                if len(top_indices) < k:
                    pad_len = k - len(top_indices)
                    top_indices = np.concatenate([top_indices, -np.ones(pad_len, dtype=int)])
                    top_scores = np.concatenate([top_scores, np.zeros(pad_len)])
                    
                distances.append(top_scores)
                indices.append(top_indices)
                
            return np.array(distances), np.array(indices)

