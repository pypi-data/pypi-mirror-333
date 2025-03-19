from sklearn.feature_extraction.text import HashingVectorizer
from compressor.semantic import count_tokens
from utility_pack.text import compress_text
from tokenizers import Tokenizer
import importlib.resources
import onnxruntime as ort
from enum import Enum
import numpy as np

embedding_model_tokenizer = Tokenizer.from_file(str(importlib.resources.files('utility_pack').joinpath('resources/embedding-model/tokenizer.json')))
embedding_model_session = ort.InferenceSession(str(importlib.resources.files('utility_pack').joinpath('resources/embedding-model/model.onnx')))

# enum for embedding type
class EmbeddingType(Enum):
    TEXTUAL = 1
    SEMANTIC = 2

def _get_textual_embeddings(texts, ngram_range=(1, 6), analyzer='char', n_features=256):
    vectorizer = HashingVectorizer(ngram_range=ngram_range, analyzer=analyzer, n_features=n_features)
    return vectorizer.transform(texts).toarray().tolist()

def _get_onnx_embeddings(texts):
    texts = [
        compress_text(t, target_token_count=500) if count_tokens(t) > 500 else t for t in texts
    ]

    # Tokenize texts with truncation
    encoded_inputs = embedding_model_tokenizer.encode_batch(texts)

    # Convert to lists and truncate sequences to max length (512)
    input_ids = [enc.ids[:512] for enc in encoded_inputs]  # Truncate here
    attention_mask = [[1] * len(ids) for ids in input_ids]

    # Find max length in batch (or cap at max_length)
    batch_max_length = max(len(ids) for ids in input_ids)  # No need for min() here, already truncated

    # Pad sequences
    def pad_sequence(seq, pad_value):
        return seq + [pad_value] * (batch_max_length - len(seq))

    input_ids = np.array([pad_sequence(ids, 1) for ids in input_ids], dtype=np.int64)
    attention_mask = np.array([pad_sequence(mask, 0) for mask in attention_mask], dtype=np.int64)  # Pad attention mask with 0s

    # Prepare ONNX input dict
    inputs_onnx = {
        "input_ids": input_ids,
        "attention_mask": attention_mask
    }

    # Run ONNX inference
    outputs = embedding_model_session.run(None, inputs_onnx)
    embeddings = outputs[0]
    embeddings = np.mean(embeddings, axis=1)
    
    return embeddings.tolist()


def extract_embeddings(texts, embedding_type=EmbeddingType.TEXTUAL):
    if embedding_type == EmbeddingType.TEXTUAL:
        return _get_textual_embeddings(texts)
    elif embedding_type == EmbeddingType.SEMANTIC:
        return _get_onnx_embeddings(texts)
    else:
        raise ValueError(f"Invalid embedding type: {embedding_type}")
