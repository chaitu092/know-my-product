# test_product_info.py
import pytest
from product_info import Product, get_product_info

from unittest.mock import patch

mock_response = {
    "product_name": "Test Product",
    "product_details": "This is a mock product.",
    "product_price_usd": 100,
    "product_price_eur": 90,
    "product_price_inr": 8000,
}


@patch("product_info.ChatOpenAI")
@patch("product_info.ChatPromptTemplate")
@patch("product_info.JsonOutputParser")
def test_get_product_info(mock_parser_class, mock_prompt_class, mock_llm_class):
    # Mock the parser
    mock_parser = mock_parser_class.return_value
    mock_parser.get_format_instructions.return_value = "{}"
    mock_parser.__or__.return_value.invoke.return_value = mock_response

    # Mock the prompt
    mock_prompt = mock_prompt_class.return_value
    mock_prompt.partial.return_value = mock_prompt

    # Mock the LLM class
    mock_llm = mock_llm_class.return_value
    mock_prompt.__or__.return_value = mock_llm
    mock_llm.__or__.return_value = mock_parser
    mock_chain = mock_prompt | mock_llm | mock_parser
    mock_chain.invoke.return_value = mock_response

    # Act
    product = get_product_info("test", "gpt-4.1")

    # Assert
    assert isinstance(product, Product)
    assert product.product_name == "Test Product"
    assert product.product_price_usd == 100
