import os
from typing import Dict, Optional, Type

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers.pydantic import TBaseModel
from langchain_openai.chat_models import ChatOpenAI


def call_gpt_with_prompt_model(
    api_key: str | None,
    prompt: str,
    pydantic_object: Optional[Type[TBaseModel]],
    model: str = "gpt-4o",
) -> Dict:
    """
    Generic function to ask for GPT's inference. Return value will be in pydantic_object
    :param api_key:
    :param prompt:
    :param pydantic_object:
    :return:
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY is not set")
    
    chat = ChatOpenAI(model=model, api_key=api_key)
    parser = JsonOutputParser(pydantic_object=pydantic_object)
    format_instructions = parser.get_format_instructions()
    _prompt = f"Answer the user query.\n{format_instructions}\n{prompt}\n"
    messages = [
        HumanMessage(
            content=[
                {"type": "text", "text": _prompt},
            ]
        )
    ]

    text_result = chat.invoke(messages)
    return parser.invoke(text_result)
