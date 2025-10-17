import streamlit as st

def show():
    # -------------------------
    # Page Title with Color
    # -------------------------
    st.markdown("<h1 style='color: #1E90FF;'>🏏 Cricbuzz LiveStats</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # -------------------------
    # Project Overview
    # -------------------------
    with st.container():
        st.subheader("📌 Project Overview")
        st.markdown("""
        Cricbuzz LiveStats is a **cricket analytics platform** that provides:
        - 📡 **Live match updates**
        - 📊 **Player performance analytics**
        - 🗂 **SQL-driven analytics & queries**
        - ✍️ **CRUD operations for player and match data**
        """)
        st.info("ℹ️ Explore different sections from the sidebar!")

    st.markdown("---")

    # -------------------------
    # Tools & Technologies
    # -------------------------
    with st.expander("🛠 Tools & Technologies", expanded=True):
        st.markdown("""
        - **Frontend**: Streamlit  
        - **Backend**: Python, SQLAlchemy  
        - **Database**: PostgreSQL / MySQL (configure via `.env`)  
        - **Deployment**: Streamlit Cloud / Local Server  
        """)
    
    st.markdown("---")

    # -------------------------
    # Instructions
    # -------------------------
    with st.expander("📖 Instructions", expanded=True):
        st.markdown("""
        1. Configure your **`.env`** file with `DATABASE_URL`.  
        2. Use the **sidebar** to navigate between pages.  
        3. Explore **LiveStats**, **Player Analytics**, and **Database CRUD**.  
        """)
        st.success("✅ Follow these steps to run the app smoothly.")

    st.markdown("---")

    # -------------------------
    # Project Resources
    # -------------------------
    with st.expander("📂 Project Resources"):
        st.markdown("""
        - [📘 Project Documentation](https://github.com/your-username/your-repo/blob/main/README.md)  
        - [📁 Folder Structure Info](https://your-github-repo-link.com)  
        """)

    st.markdown("---")

    # -------------------------
    # Add Cricket Image / Logo
    # -------------------------
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/36/Cricket_ball.png", width=150)

    # -------------------------
    # Sidebar Mini-Intro
    # -------------------------
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/36/Cricket_ball.png", width=100)
    st.sidebar.markdown("🏏 **Cricbuzz LiveStats**\n\nYour cricket analytics companion!")
