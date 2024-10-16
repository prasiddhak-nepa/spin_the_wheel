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
num_pointers = st.sidebar.slider("Number of Pointers", min_value=1, max_value=100, value=3)
apply_data = st.sidebar.button("Enter Data")

# Parse the input data into a list
data = [item.strip() for item in data_input.splitlines() if item.strip()]
random.shuffle(data)
if not data:
    st.warning("Please add data to the wheel in the sidebar.")
else:
    # Initialize the wheel chart
    fig = go.Figure(
        data=[go.Pie(
            labels=data,
            values=[1] * len(data),  # Equal-sized slices
            hole=0.3,
            textinfo='label',  # Keep labels inside the pie chart
            textfont_size=12,
            textposition='inside',
        )]
    )

    # Add multiple markers (pointers) at equal intervals
    annotations = []
    divisions_angle = 360/len(data)
    div_per_pointer = len(data)//num_pointers
    pointer_angle = div_per_pointer * divisions_angle

    for i in range(num_pointers):
        angle = i * pointer_angle  # Calculate each pointer's angle
        # Pointer coordinates
        x = 0.5 + 0.53 * math.cos(math.radians(angle + 90))
        y = 0.5 + 0.53 * math.sin(math.radians(angle + 90))

        # Number label coordinates (slightly above the pointer)
        label_x = 0.5 + 0.56 * math.cos(math.radians(angle + 90))
        label_y = 0.5 + 0.56 * math.sin(math.radians(angle + 90))

        # Add pointer annotation
        annotations.append({
            "text": "🔵", "xref": "paper", "yref": "paper",
            "showarrow": False, "font": {"size": 8, "color": "white"},
            "x": x, "y": y
        })

        # Add number label annotation
        annotations.append({
            "text": str(i + 1), "xref": "paper", "yref": "paper",
            "showarrow": False, "font": {"size": 12, "color": "#0080e6"},
            "x": label_x, "y": label_y
        })
    fig.update_layout(annotations=annotations)

    # Ensure the wheel retains a larger size and remove legends
    fig.update_layout(
        showlegend=False,  # Remove legends
        margin=dict(t=34, b=34, l=34, r=34),  # Remove margins for full view
        height=700,
        width=700,
    )

    # Placeholder for the wheel chart
    chart_placeholder = st.empty()

    def rotate_wheel(angle, frame_id):
        """Update the wheel rotation with a given angle."""
        fig.update_traces(rotation=angle)
        chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"frame-{frame_id}")

    if st.button("Spin the Wheel"):
        with st.spinner("Spinning the wheel... 🎉"):
            total_frames = FPS * SPIN_DURATION
            max_rotations = 8  # Number of full rotations
            max_angle = 360 * max_rotations

            # Select a single initial winner randomly
            initial_winner = random.choice(data)
            initial_index = data.index(initial_winner)

            # Calculate slice angle
            slice_angle = 360 / len(data)

            # Determine other winners based on equal intervals
            winners = [data[(initial_index + i * (len(data) // num_pointers)) % len(data)] 
                       for i in range(num_pointers)]

            # Calculate the target angle for the first winner
            target_angle = (initial_index * slice_angle) + (slice_angle / 2) - slice_angle

            # Final angle = max rotations + target angle
            final_angle = max_angle + target_angle

            # Smooth spinning animation with gradual deceleration
            for frame in range(total_frames):
                t = frame / total_frames  # Normalized time (0 to 1)
                eased_t = (1 - math.cos(t * math.pi)) / 2  # Smooth ease-out

                # Calculate the current angle for this frame
                current_angle = eased_t * final_angle
                rotate_wheel(current_angle % 360, frame)
                time.sleep(1 / FPS)

            # Ensure the wheel lands exactly on the winning segment
            rotate_wheel(target_angle, "final")

        # Display the results
        st.success(f"🎊 1st Winner: **{winners[0]}**")
        st.info(f"2nd Winner: **{winners[1]}**")
        st.info(f"3rd Winner: **{winners[2]}**")
        for i, winner in enumerate(winners[3:], start=4):
            st.info(f"{i}th Winner: **{winner}**")
