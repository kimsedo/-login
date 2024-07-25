import streamlit as st
import sqlite3

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 회원가입 함수
def signup(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# 로그인 함수
def login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return True
    return False

# 데이터베이스 초기화
init_db()

# Streamlit 앱
st.title("Login and Signup Page")

# 페이지 선택
page = st.sidebar.selectbox("Choose a page", ["Login", "Signup"])

if page == "Signup":
    st.header("Signup")

    # 회원가입 입력 필드
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    # 회원가입 버튼
    if st.button("Signup"):
        if new_username and new_password:
            if signup(new_username, new_password):
                st.success("Signup successful. You can now log in.")
            else:
                st.error("Username already exists. Please choose a different username.")
        else:
            st.error("Please fill out both fields.")

elif page == "Login":
    st.header("Login")

    # 로그인 입력 필드
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # 로그인 버튼
    if st.button("Login"):
        if username and password:
            if login(username, password):
                st.success("Login successful")
                st.session_state['username'] = username
                st.session_state['password'] = password
            else:
                st.error("Invalid username or password")
        else:
            st.error("Please fill out both fields.")

    # 로그인 정보 표시
    if 'username' in st.session_state and 'password' in st.session_state:
        st.write("Logged in as:", st.session_state['username'])
        st.write("Server received the following login info:")
        st.write({"username": st.session_state['username'], "password": st.session_state['password']})

    # 서버에 로그인 정보 출력
    if st.button("Show Login Info on Server"):
        st.write("Username:", st.session_state.get('username'))
        st.write("Password:", st.session_state.get('password'))
