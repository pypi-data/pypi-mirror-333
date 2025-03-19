import os, requests, json, aiohttp, asyncio, importlib
from compressor.semantic import count_tokens
from utility_pack.logger import log_exception
from tokenizers import Tokenizer
from utility_pack.text import compress_text
from ollama import AsyncClient
from ollama import Client
import onnxruntime as ort
import numpy as np

question_classifier_tokenizer = Tokenizer.from_file(str(importlib.resources.files('utility_pack').joinpath('resources/question-classifier/tokenizer.json')))
question_classifier_session = ort.InferenceSession(str(importlib.resources.files('utility_pack').joinpath('resources/question-classifier/model.onnx')))

reranker_tokenizer = Tokenizer.from_file(str(importlib.resources.files('utility_pack').joinpath('resources/reranker/tokenizer.json')))
reranker_session = ort.InferenceSession(str(importlib.resources.files('utility_pack').joinpath('resources/reranker/model.onnx')))

OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
VLLM_URL = os.environ.get("VLLM_URL", "http://127.0.0.1:8000")
if VLLM_URL.endswith("/"):
    VLLM_URL = VLLM_URL[:-1]
VLLM_KEY = os.environ.get("VLLM_KEY", "EMPTY")

OLLAMA_SYNC_CLIENT = Client(host=OLLAMA_HOST)
OLLAMA_ASYNC_CLIENT = AsyncClient(host=OLLAMA_HOST)

def openrouter_chat(messages: list, model: str = "google/gemini-flash-1.5-8b", max_tokens=None):
    """
    Needs the OPENROUTER_KEY environment variable set.

    Expects an array of messages, where each message is an object with a role and content.
    The role can be "user" or "assistant".

    Example:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"}
    ]
    """
    payload = {
        "model": model,
        "messages": messages
    }
    if max_tokens:
        payload["max_tokens"] = max_tokens
    response = requests.post(
        url=OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}"
        },
        data=json.dumps(payload)
    )
    json_response = response.json()
    return json_response["choices"][0]["message"]["content"].strip()

def openrouter_prompt(message: str, model: str = "google/gemini-flash-1.5-8b", max_tokens=None):
    """
    Needs the OPENROUTER_KEY environment variable set.
    """
    return openrouter_chat([{"role": "user", "content": message}], model, max_tokens)

async def openrouter_chat_stream(messages: list, model: str = "google/gemini-flash-1.5-8b", max_tokens=None):
    """
    Needs the OPENROUTER_KEY environment variable set.

    Expects an array of messages, where each message is an object with a role and content.
    The role can be "user" or "assistant".

    Example:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"}
    ]
    """
    payload = {
        "stream": True,
        "model": model,
        "messages": messages
    }
    if max_tokens:
        payload['max_tokens'] = max_tokens
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
                OPENROUTER_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {OPENROUTER_KEY}"
                },
                json=payload
            ) as response:
            
            buffer = ""
            async for chunk in response.content.iter_any():
                buffer += chunk.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)

                    if line.startswith("data: "):
                        event_data = line[len("data: "):]
                        if event_data != '[DONE]':
                            try:
                                current_text = json.loads(event_data)['choices'][0]['delta']['content']
                                yield current_text
                                await asyncio.sleep(0.01)
                            except Exception:
                                try:
                                    current_text = json.loads(event_data)['choices'][0]['text']
                                    yield current_text
                                    await asyncio.sleep(0.01)
                                except Exception:
                                    log_exception()

async def openrouter_prompt_stream(message: str, model: str = "google/gemini-flash-1.5-8b", max_tokens=None):
    """
    Needs the OPENROUTER_KEY environment variable set.
    """
    async for chunk in openrouter_chat_stream([{"role": "user", "content": message}], model, max_tokens):
        yield chunk

def ollama_chat(messages: list, model: str = "qwen2.5:0.5b", max_tokens=None):
    """
    Needs the OLLAMA_HOST environment variable set.

    Expects an array of messages, where each message is an object with a role and content.
    The role can be "user" or "assistant".

    Example:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"}
    ]
    """
    options = {}
    if max_tokens:
        options['num_predict'] = max_tokens

    response = OLLAMA_SYNC_CLIENT.chat(
        model=model,
        messages=messages,
        options=options
    )
    return response.message.content

def ollama_prompt(message: str, model: str = "qwen2.5:0.5b", max_tokens=None):
    """
    Needs the OLLAMA_HOST environment variable set.
    """
    return ollama_chat([{'role': 'user', 'content': message}], model, max_tokens)

async def ollama_chat_stream(messages: list, model: str = "qwen2.5:0.5b", max_tokens=None):
    """
    Needs the OLLAMA_HOST environment variable set.

    Expects an array of messages, where each message is an object with a role and content.
    The role can be "user" or "assistant".

    Example:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"}
    ]
    """
    options = {}
    if max_tokens:
        options['num_predict'] = max_tokens

    async for chunk in OLLAMA_ASYNC_CLIENT.chat(
        model=model,
        messages=messages,
        options=options,
        stream=True
    ):
        yield chunk.message.content

async def ollama_prompt_stream(message: str, model: str = "qwen2.5:0.5b", max_tokens=None):
    """
    Needs the OLLAMA_HOST environment variable set.
    """
    async for chunk in ollama_chat_stream([{"role": "user", "content": message}], model, max_tokens):
        yield chunk

def vllm_chat(messages: list, model: str = "Qwen/Qwen2.5-0.5B-Instruct", max_tokens=None):
    payload = {
        "messages": messages,
        "model": model,
        "stream": False
    }
    if max_tokens:
        payload["max_completion_tokens"] = max_tokens
    response = requests.post(
        url=f"{VLLM_URL}/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer EMPTY"
        },
        json=payload
    )
    return response.json()['choices'][0]['message']['content'].strip()

def vllm_prompt(message: str, model: str = "Qwen/Qwen2.5-0.5B-Instruct", max_tokens=None):
    return vllm_chat([{"role": "user", "content": message}], model, max_tokens)

async def vllm_chat_stream(messages: list, model: str = "Qwen/Qwen2.5-0.5B-Instruct", max_tokens=None):
    payload = {
        "messages": messages,
        "model": model,
        "stream": True
    }
    if max_tokens:
        payload["max_completion_tokens"] = max_tokens
    async with aiohttp.ClientSession() as session:
        async with session.post(
                VLLM_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {VLLM_KEY}"
                },
                json=payload
            ) as response:
            
            buffer = ""
            async for chunk in response.content.iter_any():
                buffer += chunk.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.startswith("data: "):
                        event_data = line[len("data: "):]
                        if event_data != '[DONE]':
                            try:
                                current_text = json.loads(event_data)['choices'][0]['delta']['content']
                                yield current_text
                                await asyncio.sleep(0.01)
                            except Exception:
                                try:
                                    current_text = json.loads(event_data)['choices'][0]['text']
                                    yield current_text
                                    await asyncio.sleep(0.01)
                                except Exception:
                                    log_exception()

async def vllm_prompt_stream(message: str, model: str = "Qwen/Qwen2.5-0.5B-Instruct", max_tokens=None):
    async for chunk in vllm_chat_stream([{"role": "user", "content": message}], model, max_tokens):
        yield chunk

def classify_question_generic_or_directed(question):
    # Ensure the question is truncated to a max of 500 tokens
    encoded_input = question_classifier_tokenizer.encode(question)
    input_ids = encoded_input.ids[:500]  # Truncate if needed
    attention_mask = [1] * len(input_ids)

    inputs_onnx = {
        "input_ids": [input_ids],
        "attention_mask": [attention_mask]
    }

    outputs = question_classifier_session.run(None, inputs_onnx)
    logits = outputs[0]
    prediction = "directed" if logits[0][0] > 0 else "generic"
    return prediction

def rerank(question, passages, normalize_scores=True):
    passages = [
        compress_text(p, target_token_count=500) if count_tokens(p) > 500 else p for p in passages
    ]
    # Format input templates
    templates = [f"Query: {question}\nSentence: {passage}" for passage in passages]
    encoded_inputs = reranker_tokenizer.encode_batch(templates)

    # Convert to lists and truncate sequences to max length (512)
    input_ids = [enc.ids[:512] for enc in encoded_inputs]  # Truncate here
    attention_mask = [[1] * len(ids) for ids in input_ids]
    token_type_ids = [[0] * len(ids) for ids in input_ids]

    # Find max length in batch
    batch_max_length = max(len(ids) for ids in input_ids)  # Already truncated to <=512

    # Pad sequences
    def pad_sequence(seq, pad_value=0):
        return seq + [pad_value] * (batch_max_length - len(seq))

    input_ids = np.array([pad_sequence(ids) for ids in input_ids], dtype=np.int64)
    attention_mask = np.array([pad_sequence(mask, pad_value=0) for mask in attention_mask], dtype=np.int64)
    token_type_ids = np.array([pad_sequence(types, pad_value=0) for types in token_type_ids], dtype=np.int64)

    # Create ONNX input dict
    inputs_onnx = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "token_type_ids": token_type_ids
    }

    # Run ONNX model
    outputs = reranker_session.run(None, inputs_onnx)
    logits = outputs[0]

    # Apply softmax to get probabilities
    probabilities = np.exp(logits) / np.sum(np.exp(logits), axis=1, keepdims=True)

    # Get predicted class and confidence score
    predicted_classes = np.argmax(probabilities, axis=1).tolist()
    confidences = np.max(probabilities, axis=1).tolist()

    results = [
        {"passage": passage, "prediction": pred, "confidence": conf}
        for passage, pred, conf in zip(passages, predicted_classes, confidences)
    ]

    final_results = []
    for document, result in zip(passages, results):
        # If the prediction is 0, adjust the confidence score
        if result['prediction'] == 0:
            result['confidence'] = 1 - result['confidence']
        final_results.append((document, result['confidence']))
    
    # Sort by confidence score in descending order
    sorted_results = sorted(final_results, key=lambda x: x[1], reverse=True)

    # Normalize scores if required
    if normalize_scores:
        total_score = sum(result[1] for result in sorted_results)
        if total_score > 0:
            sorted_results = [(result[0], result[1] / total_score) for result in sorted_results]

    return sorted_results
