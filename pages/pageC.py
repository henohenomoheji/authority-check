import streamlit as st

def get_roles() -> list[str]:
    roles = st.user.get("roles", [])
    if roles is None:
        return []
    if isinstance(roles, str):
        return [roles]
    return list(roles)

def has_pagec_access() -> bool:
    if not st.user.is_logged_in:
        return False
    return "PageCReader" in get_roles()

if not has_pagec_access():
    st.error("このページにアクセスする権限がありません。")
    st.stop()

st.title("PageC")
st.write("このページは PageCReader を持つユーザーだけが見られます。")

with st.expander("確認用: 現在の roles"):
    st.write(get_roles())