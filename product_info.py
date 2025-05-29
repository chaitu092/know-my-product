import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import streamlit as st

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_Project"] = os.getenv("LANGCHAIN_Project")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Define supported models
models_list = ["gpt-4.1", "llama-3.3-70b-versatile", "gemma2-9b-it", "qwen-qwq-32b"]


# Define Pydantic model for structured output
class Product(BaseModel):
    product_name: str = Field(description="The name of the product")
    product_details: str = Field(description="The details of the product")
    product_price_usd: int = Field(description="The tentative price in USD")
    product_price_eur: int = Field(description="The tentative price in Euros")
    product_price_inr: int = Field(description="The tentative price in INR")


# Define output parser
parser = JsonOutputParser(pydantic_object=Product)
format_instructions = parser.get_format_instructions()


# Load prompt template from JSON file
def load_prompt_template(filepath: str) -> PromptTemplate:
    with open(filepath, "r") as f:
        prompt_json = json.load(f)
    return PromptTemplate(
        template=prompt_json["template"], input_variables=prompt_json["input_variables"]
    )


# Streamlit UI
st.title("Know My Product")
st.sidebar.title("Product Information Tool")
st.sidebar.markdown(
    "This tool provides detailed product information and pricing estimates in multiple currencies."
)
st.markdown(
    "**Enter a product name to get estimated pricing and details in USD, EUR, and INR.**"
)

option = st.selectbox(
    "Choose an LLM model:", models_list, index=None, placeholder="Select a model"
)

# Load LLM
llm = None
if option:
    if option == "gpt-4.1":
        llm = ChatOpenAI(
            model=option, temperature=0.0, api_key=os.getenv("OPENAI_API_KEY")
        )
    else:
        llm = ChatGroq(model=option, temperature=0.0, api_key=os.getenv("GROQ_API_KEY"))
else:
    st.stop()

# ChatPromptTemplate with proper variable parsing
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

# User input
st.markdown("**Product Query**")
product_name = st.text_area("Describe the product", placeholder="e.g. MacBook Pro 2024")

if st.button("Get Product Info"):
    if not product_name.strip():
        st.warning("Please enter a product query.")
    else:
        with st.spinner("Fetching product details..."):
            try:
                chain = prompt | llm | parser
                # response = chain.invoke({"input": product_name})
                response_dict = chain.invoke({"input": product_name})
                response = Product(**response_dict)

                st.subheader("Product Information")
                st.markdown(f"**Name:** {response.product_name}")
                st.markdown(f"**Details:** {response.product_details}")
                st.markdown(f"**Price (USD):** ${response.product_price_usd}")
                st.markdown(f"**Price (EUR):** €{response.product_price_eur}")
                st.markdown(f"**Price (INR):** ₹{response.product_price_inr}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
