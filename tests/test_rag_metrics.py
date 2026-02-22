"""
Test RAG avec métriques DeepEval - Version Simple
"""
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

def test_rag_answer_relevance():
    """Test si la réponse est pertinente à la question"""
    
    # Exemple simple
    question = "Comment nettoyer un spectrophotomètre?"
    answer = "Pour nettoyer un spectrophotomètre, utilisez un chiffon doux et de l'alcool isopropylique."
    
    test_case = LLMTestCase(
        input=question,
        actual_output=answer
    )
    
    metric = AnswerRelevancyMetric(threshold=0.5)
    metric.measure(test_case)
    
    print(f"Score Answer Relevance: {metric.score}")
    assert metric.score >= 0.5


def test_rag_faithfulness():
    """Test si la réponse est fidèle au contexte"""
    
    question = "Comment calibrer une balance?"
    context = ["La calibration d'une balance se fait avec des poids étalons certifiés."]
    answer = "Utilisez des poids étalons certifiés pour calibrer la balance."
    
    test_case = LLMTestCase(
        input=question,
        actual_output=answer,
        retrieval_context=context
    )
    
    metric = FaithfulnessMetric(threshold=0.5)
    metric.measure(test_case)
    
    print(f"Score Faithfulness: {metric.score}")
    assert metric.score >= 0.5


if __name__ == "__main__":
    print("Test Answer Relevance...")
    test_rag_answer_relevance()
    
    print("\nTest Faithfulness...")
    test_rag_faithfulness()
    
    print("\n✅ Tous les tests RAG passés!")
