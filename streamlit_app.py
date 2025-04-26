# Title: Yu-Gi-Oh! Card Draw Probabilities
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import comb

st.set_page_config(page_title="Yu-Gi-Oh! Card Draw Probabilities", layout="wide")

# Sidebar description
description = """
Calculate and visualize the probability of drawing specific cards in a Yu-Gi-Oh! duel!
"""
st.sidebar.markdown(description)

# Sidebar parameters
st.sidebar.header("Parameters")
deck_size = st.sidebar.slider("Deck Size", min_value=30, max_value=60, value=40, step=1)
num_target_cards = st.sidebar.slider("Number of Χ cards in Deck", min_value=1, max_value=5, value=1, step=1)
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

# Calculate probabilities per round
rounds = list(range(1, num_rounds + 1))
probs = []
for r in rounds:
    drawn_cards = 5 + (r - 1)
    prob = prob_at_least_one_X(deck_size, num_target_cards, drawn_cards)
    probs.append(round(prob * 100, 2))

# Displaying the data as a DataFrame
df = pd.DataFrame({
    "Round": rounds,
    "Probability (%)": probs
})

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(rounds, probs, marker='o', color='#1f77b4')
for x, y in zip(rounds, probs):
    ax.text(x, y + 1.5, f"{y:.1f}%", ha='center', va='bottom', fontsize=8)

ax.set_title("Probability of Drawing at Least One Χ Card")
ax.set_xlabel("Round")
ax.set_ylabel("Probability (%)")
ax.set_xticks(rounds)
ax.set_ylim(0, max(probs) + 5)
ax.grid(True, linestyle='--', alpha=0.6)

# Layout
st.title("🎴 Yu-Gi-Oh! Card Draw Probabilities")
with st.expander("📊 Probability Chart", expanded=True):
    st.pyplot(fig)

with st.expander("📋 Probability Table"):
    st.dataframe(df, use_container_width=True)

st.toast("Probabilities calculated successfully!", icon="✅")
