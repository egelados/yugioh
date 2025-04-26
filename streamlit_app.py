# Title: Yu-Gi-Oh! Card Draw Probabilities
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from math import comb

st.set_page_config(page_title="Yu-Gi-Oh! Card Draw Probabilities", layout="wide")

# Sidebar description
description = """
Calculate and visualize the probability of drawing specific cards in a Yu-Gi-Oh! duel!
"""
st.sidebar.image("resources/Yugi.png")
st.sidebar.markdown(description)

# Sidebar parameters
st.sidebar.header("Parameters")
deck_size = st.sidebar.slider("Deck Size", min_value=30, max_value=60, value=40, step=1)
num_target_cards = st.sidebar.slider("Number of Χ cards in Deck", min_value=1, max_value=5, value=1, step=1)
initial_hand_size = st.sidebar.slider("Initial Hand Size", min_value=1, max_value=10, value=5, step=1)
num_rounds = st.sidebar.slider("Number of Rounds to Simulate", min_value=1, max_value=10, value=3, step=1)

# Footer
footer = """
---
© 2025 _____. All rights reserved.
"""
st.sidebar.markdown(footer)

# Calculation function
def prob_at_least_one_X(N, k, drawn):
    if N - k < drawn:
        return 1.0
    return 1 - (comb(N - k, drawn) / comb(N, drawn))

# Determine line color based on probability
def get_dynamic_color(probability):
    if probability >= 75:
        return '#ff5733'  # intense red-orange
    elif probability >= 50:
        return '#ffc300'  # strong yellow
    elif probability >= 33:
        return '#70ad47'  # green
    else:
        return '#4f81bd'  # blue

# Layout
st.title("🎴 Yu-Gi-Oh! Card Draw Probabilities")

# Container for live updates
with st.container():
    # Calculate probabilities per round
    rounds = []
    probs = []
    hover_texts = []
    colors = []
    highlight_round = None
    for r in range(1, num_rounds + 1):
        drawn_cards = initial_hand_size + (r - 1)
        prob = prob_at_least_one_X(deck_size, num_target_cards, drawn_cards)
        prob_percent = round(prob * 100, 2)
        rounds.append(r)
        probs.append(prob_percent)
        colors.append(get_dynamic_color(prob_percent))

        if prob_percent >= 50:
            emoji = "🔥"
        elif prob_percent >= 33:
            emoji = "⚡"
        else:
            emoji = "✨"
        hover_texts.append(f"🔢 Round: {r}<br>🎯 Probability: {prob_percent}% {emoji}")

        if highlight_round is None and prob_percent >= 33.0:
            highlight_round = r
        if prob_percent >= 100.0:
            break

    # Displaying the data as a DataFrame
    df = pd.DataFrame({
        "Round": rounds,
        "Probability (%)": probs,
        "Hover Text": hover_texts,
        "Color": colors
    })

    # Plotting with Plotly for tooltips and animation
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Round"],
        y=df["Probability (%)"],
        mode="lines+markers",
        marker=dict(size=10, color=df["Color"], line=dict(width=2, color="DarkSlateGrey")),
        line=dict(color="#888", width=2),
        hovertext=df["Hover Text"],
        hoverinfo="text"
    ))

    fig.update_layout(
        title="Probability of Drawing at Least One Χ Card",
        xaxis_title="Round",
        yaxis_title="Probability (%)",
        yaxis_range=[0, max(probs) + 5],
        hovermode="closest",
        transition_duration=500,
        height=400,
    )

    # Highlight 33% point
    if highlight_round is not None and highlight_round in rounds:
        fig.add_vline(
            x=highlight_round,
            line_dash="dash",
            line_color="orange",
            annotation_text="33% Threshold",
            annotation_position="top",
        )

    with st.expander("📊 Probability Chart", expanded=True):
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Probability Table"):
        st.dataframe(df[["Round", "Probability (%)"]], use_container_width=True)

st.toast("Probabilities calculated successfully!", icon="✅")

