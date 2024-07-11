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
    plt.text(-4, 4, 'P3', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))
    plt.text(4, 4, 'P2', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))
    plt.text(-4, -4, "Don't Do", fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))
    plt.text(4, -4, 'P4', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))

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

    return fig, ax

# Function to plot project points
def plot_project_points(ax, projects):
    # Plot points
    for value, effort, cbi, risk, label in projects:
        # Calculate x and y coordinates
        x = value - effort
        y = cbi - risk

         # Adjust (0,0) to (-0.5, 0.5)
        if x == 0 and y == 0:
            x = -0.5
            y = 0.5


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

    return ax

# Streamlit app
st.title('Prioritization Matrix App')

# Sidebar for project inputs and plot button
st.sidebar.header('Project Inputs')

num_projects = st.sidebar.number_input('Number of projects', min_value=1, max_value=10, value=1)

projects = []
for i in range(num_projects):
    st.sidebar.subheader(f'Project {i+1}')
    label = st.sidebar.text_input(f'Label (Project {i+1})', f'Project {i+1}')
    value = st.sidebar.number_input(f'Value (Project {i+1})', min_value=0, max_value=4, value=0)
    effort = st.sidebar.number_input(f'Effort (Project {i+1})', min_value=0, max_value=4, value=0)
    cbi = st.sidebar.number_input(f'CBI (Project {i+1})', min_value=0, max_value=4, value=0)
    risk = st.sidebar.number_input(f'Risk (Project {i+1})', min_value=0, max_value=4, value=0)
    projects.append((value, effort, cbi, risk, label))

# Button to plot priorities
if st.sidebar.button('Plot Priorities'):


    # Plot the prioritization matrix
    fig, ax = plot_prioritization_matrix(projects)
    
    # Plot project points on the same graph
    plot_project_points(ax, projects)

    # Display the plot
    st.pyplot(fig)
