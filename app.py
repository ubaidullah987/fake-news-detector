from __future__ import annotations
import streamlit as st
from src.highlighting import render_highlighted_html
from src.modeling import DetectionError, predict_from_text, predict_from_url
from src.ui import inject_app_styles, render_assistant_bubble, render_user_bubble


st.set_page_config(
    page_title="Fake News & Scam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_result_card(result) -> None:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-header">
                <span class="result-label">{result.label}</span>
                <span class="confidence-pill">{result.confidence_percent:.1f}% confidence</span>
            </div>
            <div class="result-meta">
                <span><strong>Risk level:</strong> {result.risk_level}</span>
                <span><strong>Source:</strong> {result.source_mode}</span>
            </div>
            <div class="explanation-box">
                <strong>Why this was flagged</strong>
                <p>{result.explanation}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Highlighted indicators")
    st.markdown(render_highlighted_html(result.highlighted_segments), unsafe_allow_html=True)

    if result.triggers:
        trigger_lines = [
            f"<li><strong>{trigger.category}</strong>: {trigger.term} ({trigger.severity})</li>"
            for trigger in result.triggers
        ]
        st.markdown(
            f"""
            <div class="trigger-box">
                <strong>Detected patterns</strong>
                <ul>{''.join(trigger_lines)}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    inject_app_styles()

    st.markdown(
        """
        <div class="hero-shell">
            <div class="hero-copy">
                <div class="eyebrow">AI + NLP Verification</div>
                <h1>Fake News & Scam Detector</h1>
                <p>
                    Drop in a message, article, or URL and get a fast verdict, confidence score,
                    highlighted warning signals, and a plain-English explanation.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Choose input mode",
        options=["Text", "URL"],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

    if mode == "Text":
        user_text = st.text_area(
            "Paste text to analyze",
            height=220,
            placeholder="Paste a news article, social post, email, or suspicious message here...",
        )
        render_user_bubble(user_text or "Paste or type a suspicious message to begin the analysis.")

        if st.button("Analyze Text", type="primary", use_container_width=True):
            if not user_text.strip():
                st.error("Please paste some text before running the detector.")
            else:
                with st.spinner("Analyzing text with the detector, so please wait......"):
                    try:
                        result = predict_from_text(user_text)
                    except DetectionError as exc:
                        st.error(str(exc))
                    else:
                        render_assistant_bubble("Analysis complete. Here is the model verdict and explanation.")
                        render_result_card(result)
    else:
        target_url = st.text_input(
            "Paste a URL to analyze",
            placeholder="https://example.com/article-or-message",
        )
        render_user_bubble(target_url or "Paste an article link and I will fetch the page content for analysis.")

        if st.button("Analyze URL", type="primary", use_container_width=True):
            if not target_url.strip():
                st.error("Please enter a URL before running the detector.")
            else:
                with st.spinner("Fetching article content and running the detector, so please wait"):
                    try:
                        result = predict_from_url(target_url)

                        # Extra safety: handle empty/invalid result
                        if result is None:
                            st.error("Could not extract content from this URL. Try another link or paste text instead.")
                        else:
                            render_assistant_bubble("The page content has been extracted and scored.")
                            render_result_card(result)

                    except DetectionError as exc:
                        st.error(str(exc))

                    except Exception:
                        st.error(
                            "This website blocks automated access. Please paste the article text instead"
                        )

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
