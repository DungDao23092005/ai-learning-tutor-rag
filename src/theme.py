import streamlit as st


def apply_custom_theme(is_dark_mode: bool) -> None:
    """
    Apply custom light/dark mode using CSS.

    This is a visual theme switch for Streamlit components.
    """
    if is_dark_mode:
        colors = {
            "app_bg": "#0F172A",
            "sidebar_bg": "#1E293B",
            "card_bg": "#111827",
            "input_bg": "#1E293B",
            "text": "#F8FAFC",
            "muted": "#CBD5E1",
            "border": "#334155",
            "primary": "#3B82F6",
            "primary_hover": "#2563EB",
            "success_bg": "#052E16",
            "success_text": "#BBF7D0",
            "warning_bg": "#422006",
            "warning_text": "#FEF3C7",
            "info_bg": "#082F49",
            "info_text": "#BAE6FD",
            "error_bg": "#450A0A",
            "error_text": "#FECACA",
        }
    else:
        colors = {
            "app_bg": "#FFFFFF",
            "sidebar_bg": "#F3F4F6",
            "card_bg": "#FFFFFF",
            "input_bg": "#FFFFFF",
            "text": "#111827",
            "muted": "#4B5563",
            "border": "#E5E7EB",
            "primary": "#2563EB",
            "primary_hover": "#1D4ED8",
            "success_bg": "#ECFDF5",
            "success_text": "#065F46",
            "warning_bg": "#FFFBEB",
            "warning_text": "#92400E",
            "info_bg": "#EFF6FF",
            "info_text": "#1E40AF",
            "error_bg": "#FEF2F2",
            "error_text": "#991B1B",
        }

    st.markdown(
        f"""
        <style>
        /* App background */
        .stApp {{
            background-color: {colors["app_bg"]};
            color: {colors["text"]};
        }}

        /* Top header */
        header[data-testid="stHeader"] {{
            background-color: {colors["app_bg"]};
            border-bottom: 1px solid {colors["border"]};
        }}

        /* Main container */
        .block-container {{
            color: {colors["text"]};
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {colors["sidebar_bg"]};
            border-right: 1px solid {colors["border"]};
        }}

        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {{
            color: {colors["text"]} !important;
        }}

        /* Headings and normal text */
        h1, h2, h3, h4, h5, h6 {{
            color: {colors["text"]} !important;
        }}

        p, label {{
            color: {colors["text"]} !important;
        }}

        div[data-testid="stMarkdownContainer"] {{
            color: {colors["text"]};
        }}

        div[data-testid="stCaptionContainer"] p {{
            color: {colors["muted"]} !important;
        }}

        /* File uploader */
        div[data-testid="stFileUploader"] section {{
            background-color: {colors["card_bg"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 12px !important;
        }}

        div[data-testid="stFileUploader"] small,
        div[data-testid="stFileUploader"] span,
        div[data-testid="stFileUploader"] p {{
            color: {colors["muted"]} !important;
        }}

        div[data-testid="stFileUploader"] button {{
            background-color: {colors["card_bg"]} !important;
            color: {colors["text"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 10px !important;
        }}

        div[data-testid="stFileUploader"] button:hover {{
            border-color: {colors["primary"]} !important;
            color: {colors["primary"]} !important;
        }}

        div[data-testid="stFileUploader"] button:disabled {{
            background-color: {colors["input_bg"]} !important;
            color: {colors["muted"]} !important;
            border: 1px solid {colors["border"]} !important;
        }}

        /* Text input and text area */
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {{
            background-color: {colors["input_bg"]} !important;
            color: {colors["text"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 10px !important;
        }}

        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stTextArea"] textarea::placeholder {{
            color: {colors["muted"]} !important;
            opacity: 1 !important;
        }}

        /* Chat input wrapper */
        div[data-testid="stChatInput"] {{
            background-color: transparent !important;
            border: none !important;
        }}

        div[data-testid="stChatInput"] > div {{
            background-color: {colors["input_bg"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 12px !important;
        }}

        div[data-testid="stChatInput"] textarea {{
            background-color: {colors["input_bg"]} !important;
            color: {colors["text"]} !important;
            border: none !important;
        }}

        div[data-testid="stChatInput"] textarea::placeholder {{
            color: {colors["muted"]} !important;
            opacity: 1 !important;
        }}

        div[data-testid="stChatInput"] button {{
            background-color: {colors["card_bg"]} !important;
            color: {colors["text"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 10px !important;
        }}

        div[data-testid="stBottom"],
        div[data-testid="stBottomBlockContainer"] {{
            background-color: {colors["app_bg"]} !important;
        }}

        /* Selectbox / radio / slider text */
        div[data-testid="stSelectbox"] *,
        div[data-testid="stRadio"] *,
        div[data-testid="stSlider"] * {{
            color: {colors["text"]} !important;
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            color: {colors["muted"]} !important;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {colors["primary"]} !important;
            border-bottom-color: {colors["primary"]} !important;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {colors["card_bg"]} !important;
            color: {colors["text"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 10px !important;
        }}

        .stButton > button:hover {{
            border-color: {colors["primary"]} !important;
            color: {colors["primary"]} !important;
        }}

        .stButton > button[kind="primary"] {{
            background-color: {colors["primary"]} !important;
            color: white !important;
            border: 1px solid {colors["primary"]} !important;
        }}

        .stButton > button[kind="primary"]:hover {{
            background-color: {colors["primary_hover"]} !important;
            color: white !important;
            border: 1px solid {colors["primary_hover"]} !important;
        }}

        /* Metrics */
        div[data-testid="stMetric"] {{
            background-color: {colors["card_bg"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 12px !important;
            padding: 14px !important;
        }}

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] div {{
            color: {colors["text"]} !important;
        }}

        /* Expanders */
        div[data-testid="stExpander"] {{
            background-color: {colors["card_bg"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 12px !important;
        }}

        div[data-testid="stExpander"] details summary p {{
            color: {colors["text"]} !important;
        }}

        /* Chat messages */
        div[data-testid="stChatMessage"] {{
            background-color: {colors["card_bg"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 14px !important;
            padding: 8px !important;
        }}

        /* Alerts */
        div[data-testid="stAlert"] {{
            border-radius: 12px !important;
            border: 1px solid {colors["border"]} !important;
        }}

        div[data-testid="stAlert"] p {{
            color: inherit !important;
        }}

        /* Code blocks */
        code, pre {{
            background-color: {colors["input_bg"]} !important;
            color: {colors["text"]} !important;
            border: 1px solid {colors["border"]} !important;
            border-radius: 8px !important;
        }}

        /* Horizontal divider */
        hr {{
            border-color: {colors["border"]} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )