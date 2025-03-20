import logging

from docketanalyzer_chat import Chat
from docketanalyzer_core import env


def test_anthropic():
    """Test Anthropic chat."""
    key_check = bool(env.ANTHROPIC_API_KEY)
    assert key_check, "ANTHROPIC_API_KEY is not set"

    chat = Chat(model="claude-3-5-haiku-latest")
    response = chat("Hi!")

    logging.info(f"Claude says: {response}")
    assert isinstance(response, str), "Response is not a string"
    assert len(response) > 0, "Response is empty"


def test_openai():
    """Test OpenAI chat."""
    key_check = bool(env.OPENAI_API_KEY)
    assert key_check, "OPENAI_API_KEY is not set"

    chat = Chat(model="openai/gpt-4o-mini")
    response = chat("Hi!")

    logging.info(f"GPT says: {response}")
    assert isinstance(response, str), "Response is not a string"
    assert len(response) > 0, "Response is empty"


def test_cohere():
    """Test Cohere chat."""
    key_check = bool(env.COHERE_API_KEY)
    assert key_check, "COHERE_API_KEY is not set"

    chat = Chat(model="command-light")
    response = chat("Hi!")

    logging.info(f"Command says: {response}")
    assert isinstance(response, str), "Response is not a string"
    assert len(response) > 0, "Response is empty"


def test_groq():
    """Test Groq chat."""
    key_check = bool(env.GROQ_API_KEY)
    assert key_check, "GROQ_API_KEY is not set"

    chat = Chat(model="groq/llama3-8b-8192")
    response = chat("Hi!")

    logging.info(f"Command says: {response}")
    assert isinstance(response, str), "Response is not a string"
    assert len(response) > 0, "Response is empty"


def test_together():
    """Test TogetherAI chat."""
    key_check = bool(env.TOGETHER_API_KEY)
    assert key_check, "TOGETHER_API_KEY is not set"

    chat = Chat(model="together_ai/meta-llama/Llama-3.2-3B-Instruct-Turbo")
    response = chat("Hi!")

    logging.info(f"Command says: {response}")
    assert isinstance(response, str), "Response is not a string"
    assert len(response) > 0, "Response is empty"
