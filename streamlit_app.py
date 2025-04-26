# Title: Yu-Gi-Oh! Card Draw Probabilities
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from math import comb

st.set_page_config(page_title="Yu-Gi-Oh! Card Draw Probabilities", layout="wide")

# Sidebar description
description = """
Calculate and visualize the probability of drawing specific cards (Χ, Υ, Ζ) in a Yu-Gi-Oh! duel!
"""
st.sidebar.image("resources/Yugi.png")
st.sidebar.markdown(description)

# Sidebar parameters
st.sidebar.header("Parameters")
deck_size = st.sidebar.slider("Deck Size", min_value=30, max_value=60, value=40, step=1)
num_x_cards = st.sidebar.slider("Number of Χ cards in Deck", min_value=0, max_value=5, value=1, step=1)
num_y_cards = st.sidebar.slider("Number of Υ cards in Deck", min_value=0, max_value=5, value=1, step=1)
num_z_cards = st.sidebar.slider("Number of Ζ cards in Deck", min_value=0, max_value=5, value=1, step=1)
initial_hand_size = st.sidebar.slider("Initial Hand Size", min_value=1, max_value=10, value=5, step=1)
num_rounds = st.sidebar.slider("Number of Rounds to Simulate", min_value=1, max_value=10, value=3, step=1)

# Footer
footer = """
---
© 2025 _____. All rights reserved.
"""
st.sidebar.markdown(footer)

# Calculation function
def prob_at_least_one(N, k, drawn):
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
    probs_x = []
    probs_y = []
    probs_z = []
    for r in range(1, num_rounds + 1):
        drawn_cards = initial_hand_size + (r - 1)
        prob_x = prob_at_least_one(deck_size, num_x_cards, drawn_cards)
        prob_y = prob_at_least_one(deck_size, num_y_cards, drawn_cards)
        prob_z = prob_at_least_one(deck_size, num_z_cards, drawn_cards)
        probs_x.append(round(prob_x * 100, 2))
        probs_y.append(round(prob_y * 100, 2))
        probs_z.append(round(prob_z * 100, 2))
        rounds.append(r)

    # Displaying the data as a DataFrame
    df = pd.DataFrame({
        "Round": rounds,
        "Χ Probability (%)": probs_x,
        "Υ Probability (%)": probs_y,
        "Ζ Probability (%)": probs_z
    })

    # Plotting with Plotly for tooltips and animation
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Round"],
        y=df["Χ Probability (%)"],
        mode="lines+markers",
        name="Χ Card",
        line=dict(color="#4f81bd", width=2),
        hoverinfo="x+y"
    ))
    fig.add_trace(go.Scatter(
        x=df["Round"],
        y=df["Υ Probability (%)"],
        mode="lines+markers",
        name="Υ Card",
        line=dict(color="#70ad47", width=2),
        hoverinfo="x+y"
    ))
    fig.add_trace(go.Scatter(
        x=df["Round"],
        y=df["Ζ Probability (%)"],
        mode="lines+markers",
        name="Ζ Card",
        line=dict(color="#ff5733", width=2),
        hoverinfo="x+y"
    ))

    fig.update_layout(
        title="Probability of Drawing at Least One Χ, Υ, Ζ Card",
        xaxis_title="Round",
        yaxis_title="Probability (%)",
        yaxis_range=[0, 105],
        hovermode="closest",
        transition_duration=500,
        height=500,
    )

    with st.expander("📊 Probability Chart", expanded=True):
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Probability Table"):
        st.dataframe(df, use_container_width=True)

st.toast("Probabilities calculated successfully!", icon="✅")
