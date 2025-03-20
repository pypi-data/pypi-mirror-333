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


# create a local indexedDB
def create_indexedDB(
    db: str,
    # db defines what DB you is manipulating
    version: int,
    # version defines what DB version you is manipulating
    object_store_name: str,
    # object_store_name defines the store you will manipulate
    index_mode: Optional[dict] = None,
    # define how the DB index the data
    _action='creat_db'
):
    if index_mode is None:
        index_mode = {"autoIncrement": True}

    return _component_func(
        action=_action,
        db=db,
        version=version,
        objectStoreName=object_store_name,
        indexMode=index_mode
    )


# put new indexes in objectStore and update existing indexes
def cursor_update_indexedDB(
    db: str,
    version: int,
    object_store_name: str,
    values: list[dict],
    _action='cursor_update'
):
    return _component_func(
        action=_action,
        db=db,
        version=version,
        objectStoreName=object_store_name,
        values=values
    )


# get all indexes in object store
def get_all_indexedDB(
    db: str,
    version: int,
    object_store_name: str,
    _action='get_all'
):
    return _component_func(
        action=_action,
        db=db,
        version=version,
        objectStoreName=object_store_name,
    )


def clear_object_store(
    db: str,
    version: int,
    object_store_name: str,
    _action='clear_object_store'
):
    return _component_func(
        action=_action,
        db=db,
        version=version,
        objectStoreName=object_store_name
    )
