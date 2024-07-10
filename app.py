import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Function to plot the prioritization matrix
def plot_prioritization_matrix(projects):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)

    # Remove grid lines and set up the plot
    ax.grid(False)

    # Remove the zero label from the axis
    ax.set_xticks(range(-4, 5))
    ax.set_xticklabels(['4', '3', '2', '1', '', '1', '2', '3', '4'])
    ax.set_yticks(range(-4, 5))
    ax.set_yticklabels(['4', '3', '2', '1', '', '1', '2', '3', '4'])

    # Move the axes to the center
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Add quadrant labels at the corners outside the graph
    plt.text(-4.5, 4.5, 'P3', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))
    plt.text(4.5, 4.5, 'P2', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))
    plt.text(-4.5, -4.5, "Don't Do", fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))
    plt.text(4.5, -4.5, 'P4', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))

    # Set axis titles just inside the graph
    plt.text(3.5, 0.3, 'Value', fontsize=12, ha='center', va='center')
    plt.text(-3.5, 0.3, 'Effort', fontsize=12, ha='center', va='center')
    plt.text(0.3, 3.5, 'CBI', fontsize=12, ha='center', va='center', rotation=90)
    plt.text(0.3, -3.5, 'Risk', fontsize=12, ha='center', va='center', rotation=90)

    # Fill the quadrants with colors using hex codes
    ax.fill_betweenx(np.arange(0, 4.1, 0.1), 0, 4, color='#a8e6a3', alpha=0.5)  # Green for P2
    ax.fill_betweenx(np.arange(0, 4.1, 0.1), -4, 0, color='#ffcc80', alpha=0.5)  # Amber for P3
    ax.fill_betweenx(np.arange(-4, 0.1, 0.1), 0, 4, color='#8ecae6', alpha=0.5)  # Blue for P4
    ax.fill_betweenx(np.arange(-4, 0.1, 0.1), -4, 0, color='#ff9aa2', alpha=0.5)  # Red for Don't Do

    # Plot points
    for value, effort, cbi, risk, label in projects:
        # Calculate x and y coordinates
        x = value - effort
        y = cbi - risk

        # Ensure points are within quadrants
        if x > 4:
            x = 4
        elif x < -4:
            x = -4
        if y > 4:
            y = 4
        elif y < -4:
            y = -4

        # Plot adjusted points
        ax.plot(x, y, 'o', label=label)
        ax.text(x, y, label, fontsize=9, ha='right')

    plt.title('Prioritization Matrix')
    st.pyplot(fig)

st.title('Prioritization Matrix App')

st.sidebar.header('Project Inputs')

num_projects = st.sidebar.number_input('Number of projects', min_value=1, max_value=10, value=1)

projects = []
for i in range(num_projects):
    st.sidebar.subheader(f'Project {i+1}')
    label = st.sidebar.text_input(f'Label (Project {i+1})', f'Project {i+1}')
    value = st.sidebar.slider(f'Value (Project {i+1})', 0, 4, 0)
    effort = st.sidebar.slider(f'Effort (Project {i+1})', 0, 4, 0)
    cbi = st.sidebar.slider(f'CBI (Project {i+1})', 0, 4, 0)
    risk = st.sidebar.slider(f'Risk (Project {i+1})', 0, 4, 0)
    projects.append((value, effort, cbi, risk, label))

plot_prioritization_matrix(projects)