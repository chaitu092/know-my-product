import streamlit as st
from product_info import get_product_info, Product

# Dropdown to choose LLM model
models_list = ["gpt-4.1", "llama-3.3-70b-versatile", "gemma2-9b-it", "qwen-qwq-32b"]
option = st.selectbox(
    "Choose an LLM model:", models_list, index=None, placeholder="Select a model"
)

# Text area to enter product name or description
product_name = st.text_area("Describe the product", placeholder="e.g. MacBook Pro 2024")

# Button logic
if st.button("Get Product Info"):
    if not product_name.strip():
        st.warning("Please enter a product query.")
    elif not option:
        st.warning("Please select an LLM model.")
    else:
        with st.spinner("Fetching product details..."):
            try:
                product = get_product_info(product_name, option)
                st.subheader("Product Information")
                st.markdown(f"**Name:** {product.product_name}")
                st.markdown(f"**Details:** {product.product_details}")
                st.markdown(f"**Price (USD):** ${product.product_price_usd}")
                st.markdown(f"**Price (EUR):** €{product.product_price_eur}")
                st.markdown(f"**Price (INR):** ₹{product.product_price_inr}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
