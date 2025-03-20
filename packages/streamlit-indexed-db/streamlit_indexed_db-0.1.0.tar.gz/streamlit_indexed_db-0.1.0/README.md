# streamlit-indexed-db

A streamlit componente that allows you to request and receive data from indexedDB

## Installation instructions 

```sh
pip install streamlit-indexed-db
```

## Usage instructions

```python
import streamlit as st

from streamlit_indexed_db import streamlit_indexed_db

value = streamlit_indexed_db()

st.write(value)
