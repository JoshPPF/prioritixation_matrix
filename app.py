import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Function to plot the prioritization matrix
def plot_prioritization_matrix():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)

    ax.grid(False)
    ax.set_xticks(range(-4, 5))
    ax.set_xticklabels(['', '', '', '', '', '', '', '', ''])
    ax.set_yticks(range(-4, 5))
    ax.set_yticklabels(['', '', '', '', '', '', '', '', ''])

    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    plt.text(-2, 2, 'P3', fontsize=20, ha='center', va='center', color='#ffb74d')
    plt.text(2, 2, 'P2', fontsize=20, ha='center', va='center', color='#8bc34a')
    plt.text(-2, -2, "Re-think", fontsize=20, ha='center', va='center', color='#e57373')
    plt.text(2, -2, 'P4', fontsize=20, ha='center', va='center', color='#64b5f6')

    plt.text(3.5, 0.3, 'Value', fontsize=12, ha='center', va='center')
    plt.text(-3.5, 0.3, 'Effort', fontsize=12, ha='center', va='center')
    plt.text(0.3, 3.5, 'CBI', fontsize=12, ha='center', va='center', rotation=90)
    plt.text(0.3, -3.5, 'Risk', fontsize=12, ha='center', va='center', rotation=90)

    ax.fill_betweenx(np.arange(0, 4.1, 0.1), 0, 4, color='#a8e6a3', alpha=0.5)
    ax.fill_betweenx(np.arange(0, 4.1, 0.1), -4, 0, color='#ffcc80', alpha=0.5)
    ax.fill_betweenx(np.arange(-4, 0.1, 0.1), 0, 4, color='#8ecae6', alpha=0.5)
    ax.fill_betweenx(np.arange(-4, 0.1, 0.1), -4, 0, color='#ff9aa2', alpha=0.5)

    return fig, ax

# Function to plot project points
def plot_project_points(ax, projects):
    for value, effort, cbi, risk, label in projects:
        x = value - effort
        y = cbi - risk

        if x == 0:
            x = -0.5
        if y == 0:
            y = 0.5

        x = max(min(x, 4), -4)
        y = max(min(y, 4), -4)

        ax.plot(x, y, 'o', label=label)
        ax.text(x, y - 0.1, label, fontsize=9, ha='center', va='top')

    return ax

# Initialize session state for labels and temporary labels
if 'labels' not in st.session_state:
    st.session_state['labels'] = [f'Project {i+1}' for i in range(10)]
if 'temp_labels' not in st.session_state:
    st.session_state['temp_labels'] = st.session_state['labels'][:]
if 'expanded' not in st.session_state:
    st.session_state['expanded'] = [True] * 20

# Streamlit app
st.markdown("<h1 style='text-align: center;'>Prioritization Matrix App</h1>", unsafe_allow_html=True)

# Sidebar for project inputs and plot button
st.sidebar.header('Projects')

num_projects = st.sidebar.number_input('Number of projects', min_value=1, max_value=10, value=1)

projects = []
for i in range(num_projects):
    with st.sidebar.expander(st.session_state['temp_labels'][i], expanded=st.session_state['expanded'][i]):
        label = st.text_input(f'Name (Project {i+1})', st.session_state['temp_labels'][i], key=f'label_{i}')
        
        # Temporary labels updated without session state change
        st.session_state['temp_labels'][i] = label
        
        value = st.number_input(f'Value (Project {i+1})', min_value=0, max_value=4, value=0, key=f'value_{i}')
        effort = st.number_input(f'Effort (Project {i+1})', min_value=0, max_value=4, value=0, key=f'effort_{i}')
        cbi = st.number_input(f'CBI (Project {i+1})', min_value=0, max_value=4, value=0, key=f'cbi_{i}')
        risk = st.number_input(f'Risk (Project {i+1})', min_value=0, max_value=4, value=0, key=f'risk_{i}')
        projects.append((value, effort, cbi, risk, st.session_state['temp_labels'][i]))

        # Save expander state
        st.session_state['expanded'][i] = True  # Keep expander open

# Button to plot priorities
if st.sidebar.button('Plot Priorities'):
    # Update session state labels from temporary labels
    st.session_state['labels'] = st.session_state['temp_labels'][:]
    
    # Plot the prioritization matrix
    fig, ax = plot_prioritization_matrix()
    
    # Plot project points on the same graph
    plot_project_points(ax, projects)

    # Display the plot
    st.pyplot(fig)
