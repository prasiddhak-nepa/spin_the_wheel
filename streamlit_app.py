import streamlit as st
import plotly.graph_objects as go
import random
import time
import math

# Animation settings
SPIN_DURATION = 5  # Total duration of the spin in seconds
FPS = 60  # Frames per second for smooth animation

# Sidebar input for wheel data
st.sidebar.header("Add Data to the Wheel")
data_input = st.sidebar.text_area("Enter data (one per line)", height=150)
# Button to apply the data input
apply_data = st.sidebar.button("Enter Data")

# Parse the input data into a list
data = [item.strip() for item in data_input.splitlines() if item.strip()]

if not data:
    st.warning("Please add data to the wheel in the sidebar.")
else:
    # Initialize the wheel chart
    fig = go.Figure(
        data=[go.Pie(
            labels=data,
            values=[1] * len(data),  # Equal values for equal-sized slices
            hole=0.3,
            textinfo='label',
            textfont_size=12,
            textposition='inside',  # Force text inside the pie slices to avoid cut-off
        )]
    )

    # Adjust layout to prevent label cut-off
    fig.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20, l=50, r=50),  # Increased margins
        height=700,  # Increased height to accommodate more labels
        width=700,   # Increased width to maintain aspect ratio
        annotations=[{
            "text": "▲", 
            "xref": "paper", "yref": "paper",
            "showarrow": False, "font": {"size": 136}, "x": 0.5, "y": 0.55
        }]
    )

    # Create a placeholder for the wheel chart
    chart_placeholder = st.empty()

    def rotate_wheel(angle, frame_id):
        """Update the wheel rotation with a given angle."""
        fig.update_traces(rotation=angle)
        chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"frame-{frame_id}")

    # Button to trigger the spin
    if st.button("Spin the Wheel"):
        with st.spinner("Spinning the wheel... 🎉"):
            total_frames = FPS * SPIN_DURATION
            max_rotations = 8  # Number of full rotations
            max_angle = 360 * max_rotations

            # Randomly determine the winner
            winner = random.choice(data)
            winner_index = data.index(winner)

            # Calculate the target angle for the winner
            slice_angle = 360 / len(data)
            target_angle = (winner_index * slice_angle) + (slice_angle / 2) - slice_angle

            # Calculate the final rotation angle (multiple full rotations + target angle)
            final_angle = max_angle + target_angle

            # Spin with gradual deceleration
            for frame in range(total_frames):
                t = frame / total_frames  # Normalized time (0 to 1)
                eased_t = math.sin(t * math.pi / 2)  # Smooth easing function

                # Calculate the current angle for this frame
                current_angle = eased_t * final_angle
                rotate_wheel(current_angle % 360, frame)
                time.sleep(1 / FPS)  # Control the frame rate

            # Ensure the wheel lands exactly on the winning segment
            rotate_wheel(target_angle, "final")

        # Display the result
        st.success(f"🎊 The wheel landed on: **{winner}**")
