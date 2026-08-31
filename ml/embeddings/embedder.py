import numpy as np

class MaterialEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.fallback_vectorizer = None
        
        try:
            from sentence_transformers import SentenceTransformer
            print(f"Loading sentence-transformer model: {self.model_name}...")
            self.model = SentenceTransformer(self.model_name)
            print("SentenceTransformer loaded successfully.")
        except Exception as e:
            print(f"Failed to load SentenceTransformer ({e}). Falling back to TF-IDF Embeddings.")
            from sklearn.feature_extraction.text import TfidfVectorizer
            # Predefined vocabulary of domain terms to keep TF-IDF stable
            vocab = [
                "STAINLESS", "STEEL", "CARBON", "ALLOY", "BRASS", "COPPER", "ALUMINUM", "BRONZE", "CAST", "IRON", "CHROME",
                "PIPE", "SEAMLESS", "WELDED", "VALVE", "BALL", "GATE", "GLOBE", "BUTTERFLY", "CHECK", "BEARING", "ROLLER",
                "TAPERED", "NEEDLE", "FASTENER", "BOLT", "HEX", "NUT", "SCREW", "WASHER", "SOCKET", "HEAD", "CAP",
                "CABLE", "XLPE", "PVC", "INSTRUMENTATION", "FLEXIBLE", "IN", "MM", "SQMM", "CORE", "PAIR",
                "ASTM", "ANSI", "API", "DIN", "ISO", "IEC", "IS", "BS", "MSS", "SP", "SCHEDULE", "SCH", "LB", "CLASS", "GRADE",
                "V", "KV", "M", "TP304", "TP316", "CF8", "CF8M", "WCB", "A2-70", "A4", "A4-70", "P11"
            ] + [str(i) for i in range(200)]
            self.fallback_vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
            self.fallback_vectorizer.fit(vocab)

            
    def embed(self, texts):
        if isinstance(texts, str):
            texts = [texts]
            
        if self.model is not None:
            # Generate sentence-transformer embeddings
            embeddings = self.model.encode(texts, show_progress_bar=False)
            return np.array(embeddings)
        else:
            # TF-IDF Fallback
            # If the vectorizer has not been fitted, fit it on this corpus
            if self.fallback_vectorizer is not None:
                try:
                    matrix = self.fallback_vectorizer.transform(texts)

                    # Convert to dense array
                    embeddings = matrix.toarray()
                    
                    # Normalize L2-wise so that dot-product is equivalent to cosine similarity
                    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                    norms[norms == 0] = 1.0  # avoid division by zero
                    embeddings = embeddings / norms
                    return embeddings
                except Exception as ex:
                    print(f"TF-IDF embedding generation failed: {ex}. Using basic character count fallback.")
            
            # Simple character bag fallback if everything else fails
            vocab = sorted(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/\"-# "))
            char_to_idx = {char: idx for idx, char in enumerate(vocab)}
            embeddings = []
            for t in texts:
                vec = np.zeros(len(vocab))
                for char in t.upper():
                    if char in char_to_idx:
                        vec[char_to_idx[char]] += 1
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec = vec / norm
                embeddings.append(vec)
            return np.array(embeddings)

