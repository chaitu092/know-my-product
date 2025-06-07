# product_info.py
import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Load environment variables
load_dotenv()


class Product(BaseModel):
    product_name: str = Field(description="The name of the product")
    product_details: str = Field(description="The details of the product")
    product_price_usd: int = Field(description="The tentative price in USD")
    product_price_eur: int = Field(description="The tentative price in Euros")
    product_price_inr: int = Field(description="The tentative price in INR")


def get_product_info(product_query: str, model_name: str) -> Product:
    parser = JsonOutputParser(pydantic_object=Product)
    format_instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate(
        messages=[
            (
                "system",
                "You are a product expert and assistant. Respond with product name, detailed description, and estimated prices in JSON format. Always return USD, EUR, and INR prices (integers).",
            ),
            ("user", "{input}"),
            ("assistant", "{format_instructions}"),
        ],
        input_variables=["input"],
        partial_variables={"format_instructions": format_instructions},
    )

    if model_name == "gpt-4.1":
        llm = ChatOpenAI(
            model=model_name, temperature=0.0, api_key=os.getenv("OPENAI_API_KEY")
        )
    else:
        llm = ChatGroq(
            model=model_name, temperature=0.0, api_key=os.getenv("GROQ_API_KEY")
        )

    chain = prompt | llm | parser
    response_dict = chain.invoke({"input": product_query})
    return Product(**response_dict)
