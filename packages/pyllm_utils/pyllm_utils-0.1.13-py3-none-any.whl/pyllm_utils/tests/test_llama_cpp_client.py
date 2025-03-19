import pytest
import base64
import logging
import inspect
from llm.llama_cpp_api.llama_cpp_client import LlamaCppClient
from test_llm import judge_authenticity
from unittest.mock import MagicMock
import pathlib
import json
from PIL import Image
from io import BytesIO
# ロギングの設定
logging.basicConfig(
    filename='test_llm_responses.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s' 
)

class Tool:
    def add_two_numbers(self, a: int, b: int) -> int:
        return a + b
    
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_two_numbers",
            "description": "2つの数値を足し合わせる関数",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "1つ目の数値"},
                    "b": {"type": "number", "description": "2つ目の数値"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

def log_test_response(response):
    """テストレスポンスをログに記録する補助関数"""
    current_function = inspect.currentframe().f_back.f_code.co_name
    logging.info(f"Test: {current_function} - Response: {response}")

client = LlamaCppClient(model="Phi-3-mini-4k-instruct-q4-GGUF")

def test_request_messages_with_user_message():
    response = client.request_messages(messages=[{'role': 'user', 'content': 'こんにちは、世界！'}])
    log_test_response(response)
    assert isinstance(response, str)

# def test_request_messages_with_user_image_local_path():
#     # PosixPathをstr型に変換
#     image_path = str(pathlib.Path(__file__).parent.parent.resolve() / 'test.png')
#     messages = [
#         {
#             'role': 'user',
#             'content': [
#                 {
#                     'type': 'text',
#                     'text': 'この画像は何の画像ですか？'
#                 },
#                 {
#                     'type': 'image',
#                     'image': {
#                         'type': 'path',
#                         'content': image_path, 
#                         'detail': 'high'
#                     }
#                 }
#             ]
#         }
#     ]
#     try:
#         response = client.request_messages(messages=messages)
#         log_test_response(response)
#         correct, reason = judge_authenticity("猫の画像に関することが書かれていれば正解です。", response)
#         assert correct, reason
#     except Exception as e:
#         logging.error(f"Error: {e}")
#         raise e

# def test_request_messages_with_user_image_url():
#     url = "https://th.bing.com/th/id/OIP.fyKxvsr3bvoNud-A5Ij2fAHaE6?w=271&h=180&c=7&r=0&o=5&pid=1.7"
#     messages = [
#         {
#             'role': 'user',
#             'content': [
#                 {
#                     'type': 'text',
#                     'text': 'この画像は何の画像ですか？'
#                 },
#                 {
#                     'type': 'image',
#                     'image': {
#                         'type': 'url',
#                         'content': url
#                     }
#                 }
#             ]
#         }
#     ]
#     response = client.request_messages(messages=messages)
#     log_test_response(response)
#     correct, reason = judge_authenticity("猫の画像に関することが書かれていれば正解です。", response)
#     assert correct, reason

# def test_request_messages_with_user_image_base64():
#     file_path = str(pathlib.Path(__file__).parent.parent.resolve() / 'test.png')
#     with open(file_path, 'rb') as file:
#         image_data = base64.b64encode(file.read()).decode('utf-8')
#     messages = [
#         {
#             'role': 'user',
#             'content': [
#                 {
#                     'type': 'text',
#                     'text': 'この画像は何の画像ですか？'
#                 },
#                 {
#                     'type': 'image',
#                     'image': {
#                         'type': 'base64',
#                         'content': image_data
#                     }
#                 }
#             ]
#         }
#     ]
#     response = client.request_messages(messages=messages)
#     log_test_response(response)
#     correct, reason = judge_authenticity("猫の画像に関することが書かれていれば正解です。", response)
#     assert correct, reason

def test_stream_response_messages():
    response_generator = client.request_messages(messages=[{'role': 'user', 'content': 'こんにちは、世界！'}], stream=True)
    for response in response_generator:
        pass
    response = client.get_latest_response()
    log_test_response(response)
    assert len(response) == 1
