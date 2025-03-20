from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called streamlit_indexed_db,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"streamlit_indexed_db", path=str(frontend_dir)
)


def create_indexedDB(
    db: str,
    version: int,
    object_store_name: str,
    index_mode: Optional[dict] = None,
    action='creat_db'
):
    if index_mode is None:
        index_mode = {"autoIncrement": True}

    return _component_func(
        action=action,
        db=db,
        version=version,
        objectStoreName=object_store_name,
        indexMode=index_mode
    )


def cursor_update_indexedDB(
    db: str,
    version: int,
    object_store_name: str,
    values: list[dict],
    action='cursor_update'
):
    return _component_func(
        action=action,
        db=db,
        version=version,
        objectStoreName=object_store_name,
        values=values
    )


def get_all_indexedDB(
    db: str,
    version: int,
    object_store_name: str,
    action='get_all'
):
    return _component_func(
        action=action,
        db=db,
        version=version,
        objectStoreName=object_store_name,
    )


def main():
    st.title('Testando indexedDB com Streamlit')
    # create_indexedDB(db="TestDB", version=1, object_store_name="TestName")
    # cursor_update_indexedDB(db="TestDB", version=1, object_store_name="TestName", values=[{"role": "ai", "content": "olá tudo bem? Como posso te ajudar"}, {"role": "user", "content": "você tem uma lista de ramais?"}])
    all_values = get_all_indexedDB('TestDB', 1, 'TestName')
    st.write('o indexed db foi inicializado no frontend')
    st.write(all_values)


if __name__ == "__main__":
    main()
