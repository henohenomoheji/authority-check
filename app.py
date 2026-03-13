import streamlit as st

st.set_page_config(page_title="Page Access Test", layout="wide")

st.title("Streamlit + Entra ID ページ権限制御テスト")


st.write("is_logged_in:", getattr(st.user, "is_logged_in", None))
st.write(
    "user dict:", st.user.to_dict() if hasattr(st.user, "to_dict") else dict(st.user)
)


if not st.user.is_logged_in:
    st.write("未ログインです。")
    if st.button("Microsoft Entra でログイン"):
        print("ログイン操作")
        st.login("microsoft")
    st.stop()

print(st.user.to_dict())
try:
    user_dict = st.user.to_dict()
except Exception:
    user_dict = dict(st.user)

roles = user_dict.get("roles", [])
if roles is None:
    roles = []
elif isinstance(roles, str):
    roles = [roles]
else:
    roles = list(roles)

st.success(f"ログイン中: {user_dict.get('email', 'unknown')}")
st.write("左のメニューから PageA / PageB / PageC を選択してください。")

st.write("### roles 確認")
st.write(roles)

if "AdminPage" in roles:
    st.success("AdminPage が付与されています。")
else:
    st.warning("AdminPage は付与されていません。")

with st.expander("現在のユーザー情報を確認"):
    st.json(user_dict)

if st.button("ログアウト"):
    st.logout()
