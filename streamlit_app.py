import requests
import streamlit as st

st.write("# Module Extraction AI Agent")

links_input = st.text_area("Enter multiple links (one per line):")
if links_input:
    links = [link.strip() for link in links_input.splitlines() if link.strip()]
    st.write("You entered the following links:")
    for link in links:
        st.write(link)
    if st.button("Extract Modules"):        
        results = []
        for link in links:
            with st.spinner(f"Processing {link}..."):
                try:
                    response = requests.get(f"http://127.0.0.1:8000/ask", params={"url": link}, timeout=120)
                    if response.status_code == 200:
                        results.append({"link": link, "response": response.json()["response"]})
                    else:
                        results.append({"link": link, "response": f"Error: {response.status_code}"})
                except Exception as e:
                    results.append({"link": link, "response": f"Exception: {e}"})
        st.write("## Results")
        for result in results:
            st.write(f"{result['link']}")
            st.code(result['response'])


