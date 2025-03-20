from typing import List, Dict, Any, Optional
import json
import pandas as pd


class QAPair:
    """A question-answer pair for RAG evaluation."""
    
    def __init__(
        self,
        question: str,
        answer: str,
        context: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a QA pair.
        
        Args:
            question: The input query
            answer: The expected output/answer
            context: List of relevant documents/passages
            metadata: Additional information about the QA pair
        """
        self.question = question  # input query
        self.answer = answer     # expected output
        self.context = context   # retrieved documents
        self.metadata = metadata or {}
    
    def to_dict(self):
        """Convert to dictionary format."""
        return {
            "input": self.question,
            "expected_output": self.answer,
            "context": self.context,
            "metadata": self.metadata
        }


class Testset:
    """A collection of question-answer pairs for RAG evaluation."""
    
    def __init__(self, qa_pairs: List[QAPair], metadata: Optional[Dict[str, Any]] = None):
        self.qa_pairs = qa_pairs
        self.metadata = metadata or {}
    
    @classmethod
    def from_ragas(cls, ragas_dataset):
        """Convert Ragas dataset to Phinity Testset."""
        df = ragas_dataset.to_pandas()
        
        qa_pairs = []
        for _, row in df.iterrows():
            qa_pairs.append(
                QAPair(
                    question=row.get("user_input", ""),
                    answer=row.get("reference", ""),
                    context=row.get("reference_contexts", []),
                    metadata={
                        "type": row.get("synthesizer_name", "unknown"),
                        "difficulty": row.get("difficulty", "medium")
                    }
                )
            )
        
        return cls(qa_pairs=qa_pairs)
    
    def to_dict(self):
        """Convert to dictionary format."""
        return {
            "qa_pairs": [qa.to_dict() for qa in self.qa_pairs],
            "metadata": self.metadata
        }
    
    def to_json(self, file_path: Optional[str] = None):
        """Export testset to JSON."""
        data = self.to_dict()
        
        if file_path:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            return file_path
            
        return json.dumps(data, indent=2)
    
    def to_pandas(self):
        """Convert to pandas DataFrame."""
        data = []
        for qa in self.qa_pairs:
            item = {
                "input": qa.question,
                "expected_output": qa.answer,
                "context": qa.context,
            }
            
            # Add all metadata
            for k, v in qa.metadata.items():
                item[k] = v
                
            data.append(item)
            
        return pd.DataFrame(data)