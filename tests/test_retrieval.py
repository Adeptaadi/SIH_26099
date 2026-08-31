import numpy as np
from ml.retrieval.vector_search import VectorIndex

def test_retrieval():
    dimension = 4
    index = VectorIndex(dimension=dimension)
    
    # 3 mock indexed items
    embeddings = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0]
    ])
    
    index.add(embeddings)
    
    # Query matching second item closest
    query = np.array([[0.1, 0.9, 0.0, 0.0]])
    distances, indices = index.search(query, k=2)
    
    assert indices[0][0] == 1  # closest should be index 1
    assert indices[0][1] == 0  # second closest should be index 0
    assert distances[0][0] > distances[0][1]

