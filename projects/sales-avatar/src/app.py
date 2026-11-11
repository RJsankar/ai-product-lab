"""Streamlit UI for the Sales Avatar V0.1 MVP."""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from prompts import (
    EVALUATION_SCHEMA,
    PERSONAS,
    customer_input,
    evaluation_input,
    evaluation_instructions,
    parse_evaluation,
    persona_instructions,
)


load_dotenv()

DEFAULT_SCENARIO = (
    "A 20-minute discovery call. The sales rep is introducing an AI coaching product "
    "and must understand the customer's needs before proposing a next step."
)


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Add OPENAI_API_KEY to a local .env file before starting a simulation.")
    return OpenAI(api_key=api_key)


def model_name() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def generate_customer_reply() -> str:
    response = get_client().responses.create(
        model=model_name(),
        instructions=persona_instructions(st.session_state.persona, st.session_state.scenario),
        input=customer_input(st.session_state.messages),
    )
    return response.output_text.strip()


def generate_evaluation() -> dict:
    response = get_client().responses.create(
        model=model_name(),
        instructions=evaluation_instructions(st.session_state.persona, st.session_state.scenario),
        input=evaluation_input(st.session_state.messages),
        text={
            "format": {
                "type": "json_schema",
                "name": "sales_coaching_feedback",
                "schema": EVALUATION_SCHEMA,
                "strict": True,
            }
        },
    )
    return parse_evaluation(response.output_text)


def reset_simulation() -> None:
    for key in ("messages", "evaluation", "active", "persona", "scenario"):
        st.session_state.pop(key, None)


def render_feedback(feedback: dict) -> None:
    st.subheader("Coaching feedback")
    st.metric("Overall score", f"{feedback['overall_score']} / 5")
    st.write(feedback["summary"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Strengths**")
        for item in feedback["strengths"]:
            st.markdown(f"- {item}")
    with col2:
        st.markdown("**Misses**")
        for item in feedback["misses"]:
            st.markdown(f"- {item}")

    st.markdown("**Try next**")
    for item in feedback["next_steps"]:
        st.markdown(f"- {item}")

    labels = {
        "discovery": "Discovery",
        "listening": "Listening & relevance",
        "value_articulation": "Value articulation",
        "objection_handling": "Objection handling",
        "next_step": "Clear next step",
    }
    st.markdown("**Rubric**")
    for key, label in labels.items():
        st.write(f"{label}: {feedback['rubric'][key]} / 5")


st.set_page_config(page_title="Sales Avatar", page_icon="🎯", layout="centered")
st.title("Sales Avatar")
st.caption("Practice a customer conversation. Get evidence-based coaching.")

if "active" not in st.session_state:
    st.session_state.active = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "evaluation" not in st.session_state:
    st.session_state.evaluation = None

with st.sidebar:
    st.header("Simulation setup")
    selected_persona = st.selectbox("Customer persona", list(PERSONAS), disabled=st.session_state.active)
    selected_scenario = st.text_area(
        "Scenario",
        value=DEFAULT_SCENARIO,
        height=150,
        disabled=st.session_state.active,
    )
    if not st.session_state.active:
        if st.button("Start simulation", type="primary", use_container_width=True):
            st.session_state.persona = selected_persona
            st.session_state.scenario = selected_scenario.strip() or DEFAULT_SCENARIO
            st.session_state.active = True
            try:
                opening = generate_customer_reply()
                st.session_state.messages.append({"role": "assistant", "content": opening})
                st.rerun()
            except Exception as exc:
                st.session_state.active = False
                st.error(str(exc))
    else:
        st.info(f"Playing: {st.session_state.persona}")
        if st.button("Reset", use_container_width=True):
            reset_simulation()
            st.rerun()

if not st.session_state.active:
    st.markdown(
        "Choose a persona and scenario, then start the simulation. The AI will stay in character "
        "until you end the session."
    )
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if not st.session_state.evaluation:
        user_message = st.chat_input("Respond as the sales rep")
        if user_message:
            st.session_state.messages.append({"role": "user", "content": user_message})
            with st.chat_message("user"):
                st.write(user_message)
            with st.chat_message("assistant"):
                with st.spinner("Customer is responding..."):
                    try:
                        reply = generate_customer_reply()
                        st.write(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    except Exception as exc:
                        st.error(str(exc))

        if st.button("End simulation and get feedback", type="primary", use_container_width=True):
            if not any(item["role"] == "user" for item in st.session_state.messages):
                st.warning("Add at least one sales-rep response before requesting feedback.")
            else:
                with st.spinner("Evaluating the conversation..."):
                    try:
                        st.session_state.evaluation = generate_evaluation()
                        st.rerun()
                    except Exception as exc:
                        st.error(str(exc))
    else:
        render_feedback(st.session_state.evaluation)
        if st.button("Practice again", type="primary", use_container_width=True):
            reset_simulation()
            st.rerun()

