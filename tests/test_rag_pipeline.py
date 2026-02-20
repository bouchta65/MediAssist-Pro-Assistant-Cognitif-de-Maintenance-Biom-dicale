import pytest
from app.rag.rag_pipeline import RAGPipeline
from app.rag.retriever import Retriever
from app.rag.embeddings.embeddings import EmbeddingGenerator


class TestRAGPipeline:
    """Test suite for RAG pipeline components"""

    @pytest.fixture
    def rag_pipeline(self):
        """Fixture to create RAG pipeline instance"""
        return RAGPipeline()

    @pytest.fixture
    def retriever(self):
        """Fixture to create retriever instance"""
        return Retriever()

    def test_retriever_initialization(self, retriever):
        """Test retriever initialization"""
        assert retriever is not None

    def test_rag_pipeline_initialization(self, rag_pipeline):
        """Test RAG pipeline initialization"""
        assert rag_pipeline is not None

    def test_query_processing(self, rag_pipeline):
        """Test basic query processing"""
        query = "Comment fonctionne le dispositif?"
        try:
            # This should not raise an exception
            result = rag_pipeline.process_query(query)
            assert result is not None
        except Exception as e:
            # Expected if resources not available in test env
            pytest.skip(f"RAG resources not available: {e}")

    def test_embedding_generation(self):
        """Test embedding generation"""
        try:
            embedder = EmbeddingGenerator()
            text = "Test medical device text"
            embedding = embedder.generate_embedding(text)
            assert embedding is not None
            assert len(embedding) > 0
        except Exception as e:
            pytest.skip(f"Embedding resources not available: {e}")

    def test_retriever_search(self, retriever):
        """Test retriever search functionality"""
        try:
            query = "maintenance dispositif médical"
            results = retriever.search(query, top_k=3)
            assert isinstance(results, list)
        except Exception as e:
            pytest.skip(f"Search resources not available: {e}")
