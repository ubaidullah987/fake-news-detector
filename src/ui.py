from __future__ import annotations

import html

import streamlit as st


def inject_app_styles() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&family=Source+Sans+3:wght@400;600;700&display=swap');

            :root {
                --bg: #f7f1e8;
                --surface: rgba(255, 252, 247, 0.92);
                --surface-strong: #fffdf9;
                --ink: #18212f;
                --muted: #556070;
                --accent: #0f8b8d;
                --accent-deep: #136f73;
                --user: #dff3ea;
                --assistant: #ffffff;
                --danger: #cc3d3d;
                --warning: #f0b429;
                --shadow: 0 24px 60px rgba(24, 33, 47, 0.10);
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(15, 139, 141, 0.16), transparent 28%),
                    radial-gradient(circle at top right, rgba(240, 180, 41, 0.14), transparent 24%),
                    linear-gradient(180deg, #f8f2e8 0%, #efe7da 100%);
                color: var(--ink);
            }

            .block-container {
                max-width: 980px;
                padding-top: 2rem;
                padding-bottom: 2rem;
            }

            h1, h2, h3 {
                font-family: 'Manrope', sans-serif;
                color: var(--ink);
            }

            p, label, div, span {
                font-family: 'Source Sans 3', sans-serif;
            }

            .hero-shell {
                background: linear-gradient(135deg, rgba(255,255,255,0.94), rgba(255,247,233,0.9));
                border: 1px solid rgba(24, 33, 47, 0.08);
                border-radius: 28px;
                padding: 2rem;
                box-shadow: var(--shadow);
                margin-bottom: 1.25rem;
            }

            .hero-shell h1 {
                font-size: clamp(2rem, 5vw, 3.4rem);
                line-height: 1.05;
                margin: 0.2rem 0 0.6rem;
            }

            .hero-shell p {
                font-size: 1.08rem;
                max-width: 700px;
                color: var(--muted);
                margin: 0;
            }

            .eyebrow {
                display: inline-block;
                font-size: 0.82rem;
                text-transform: uppercase;
                letter-spacing: 0.16em;
                color: var(--accent-deep);
                font-weight: 700;
                background: rgba(15, 139, 141, 0.1);
                padding: 0.45rem 0.75rem;
                border-radius: 999px;
            }

            .chat-shell {
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }

            .chat-bubble {
                max-width: 82%;
                padding: 1rem 1.15rem;
                border-radius: 22px;
                box-shadow: 0 12px 30px rgba(24, 33, 47, 0.08);
                border: 1px solid rgba(24, 33, 47, 0.06);
                animation: rise-in 240ms ease-out;
            }

            .chat-bubble.user {
                margin-left: auto;
                background: var(--user);
                border-bottom-right-radius: 8px;
            }

            .chat-bubble.assistant {
                margin-right: auto;
                background: var(--assistant);
                border-bottom-left-radius: 8px;
            }

            .bubble-title {
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--muted);
                margin-bottom: 0.25rem;
            }

            .bubble-body {
                font-size: 1rem;
                color: var(--ink);
                white-space: pre-wrap;
            }

            .result-card {
                background: var(--surface-strong);
                border-radius: 24px;
                border: 1px solid rgba(24, 33, 47, 0.08);
                padding: 1.25rem;
                margin: 1rem 0 1.25rem;
                box-shadow: var(--shadow);
            }

            .result-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 1rem;
                flex-wrap: wrap;
                margin-bottom: 0.8rem;
            }

            .result-label {
                font-family: 'Manrope', sans-serif;
                font-size: 1.5rem;
                font-weight: 800;
            }

            .confidence-pill {
                background: rgba(15, 139, 141, 0.12);
                color: var(--accent-deep);
                padding: 0.5rem 0.8rem;
                border-radius: 999px;
                font-weight: 700;
            }

            .result-meta {
                display: flex;
                gap: 1.25rem;
                flex-wrap: wrap;
                color: var(--muted);
                margin-bottom: 1rem;
            }

            .explanation-box, .trigger-box, .highlight-box {
                background: rgba(247, 241, 232, 0.72);
                border-radius: 18px;
                padding: 1rem;
                border: 1px solid rgba(24, 33, 47, 0.06);
            }

            .highlight-box {
                line-height: 1.8;
                font-size: 1rem;
            }

            .highlight {
                padding: 0.18rem 0.28rem;
                border-radius: 8px;
                font-weight: 700;
            }

            .high-risk {
                background: rgba(204, 61, 61, 0.18);
                color: #8b1e1e;
            }

            .moderate-risk {
                background: rgba(240, 180, 41, 0.28);
                color: #7a5a00;
            }

            @keyframes rise-in {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @media (max-width: 768px) {
                .chat-bubble {
                    max-width: 100%;
                }

                .hero-shell {
                    padding: 1.4rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_user_bubble(message: str) -> None:
    safe_message = html.escape(message)
    st.markdown(
        f"""
        <div class="chat-bubble user">
            <div class="bubble-title">You</div>
            <div class="bubble-body">{safe_message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_assistant_bubble(message: str) -> None:
    safe_message = html.escape(message)
    st.markdown(
        f"""
        <div class="chat-bubble assistant">
            <div class="bubble-title">Detector AI</div>
            <div class="bubble-body">{safe_message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
