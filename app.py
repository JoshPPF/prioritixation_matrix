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

# Function to plot the bug priorities
def plot_bug_priorities(bug_scores, bug_names):
    # Calculate total scores and corresponding colors and labels
    total_scores = [sum(scores) for scores in bug_scores]
    colors = []
    labels = []

    for score in total_scores:
        if 55 <= score <= 80:
            colors.append('#FF0000')  # Red
            labels.append('P2')
        elif 30 <= score <= 54:
            colors.append('#FFC107')  # Amber
            labels.append('P3')
        elif 0 <= score <= 29:
            colors.append('#0000FF')  # Blue
            labels.append('P4')

    # Define bar positions
    bar_positions = np.arange(len(bug_names))

    # Create the bar chart
    fig, ax = plt.subplots()

    # Plot each section of the stacked bars
    bottoms = np.zeros(len(bug_names))

    for i, score_type in enumerate(zip(*bug_scores)):
        ax.bar(bar_positions, score_type, bottom=bottoms, color=colors, edgecolor='black')
        bottoms += score_type

    # Add labels on top of bars
    for i, (score, label) in enumerate(zip(total_scores, labels)):
        ax.text(bar_positions[i], total_scores[i] + 1, f'{score} ({label})', ha='center', va='bottom')

    # Customize the chart
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("Bug Scoring System")
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bug_names)
    ax.set_ylim(0, 80)

    return fig

# Initialize session state for labels and temporary labels for projects
if 'labels' not in st.session_state:
    st.session_state['labels'] = [f'Project {i+1}' for i in range(10)]
if 'temp_labels' not in st.session_state:
    st.session_state['temp_labels'] = st.session_state['labels'][:]
if 'expanded' not in st.session_state:
    st.session_state['expanded'] = [True] * 10

# Initialize session state for bug inputs
if 'bug_scores' not in st.session_state:
    st.session_state['bug_scores'] = [[0, 0, 0, 0] for _ in range(10)]
if 'bug_names' not in st.session_state:
    st.session_state['bug_names'] = [f'Bug {i+1}' for i in range(10)]
if 'temp_bug_names' not in st.session_state:
    st.session_state['temp_bug_names'] = [f'Bug {i+1}' for i in range(10)]
if 'bug_expanded' not in st.session_state:
    st.session_state['bug_expanded'] = [False] * 10

# Streamlit app with pages
st.markdown("<h1 style='text-align: center;'>Prioritization App</h1>", unsafe_allow_html=True)

page = st.sidebar.radio("Select a page", ("Features Priority Matrix", "Bug Priorities"))

if page == "Features Priority Matrix":
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
            st.session_state['expanded'][i] = True * 10  # Keep expander open

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


elif page == "Bug Priorities":
    st.sidebar.header('Bug Scoring')
    num_bugs = st.sidebar.number_input('Number of bugs', min_value=1, max_value=10, value=1)

    for i in range(num_bugs):
        with st.sidebar.expander(st.session_state['bug_names'][i], expanded=st.session_state['bug_expanded'][i]):
            bug_name = st.text_input(f'Name', st.session_state['temp_bug_names'][i], key=f'bug_name_{i}')
            st.session_state['temp_bug_names'][i] = bug_name

            bug_type = st.number_input(
                f'Bug Type (0-20)', 
                min_value=0, 
                max_value=20, 
                key=f'bug_type_{i}',
                help="""
                **Bug Type /20**
                - No user issue. i.e. the user won’t even notice: **0**
                - Visual polish. It doesn’t affect navigation or branding: **4**
                - Minor Usability issue (or slightly affecting branding): **8**
                - Impairs usability in some non-key scenarios (or significantly affects branding): **12**
                - Impairs usability in key scenarios (or a major branding issue): **16**
                - Major usability issue: **20**
                """
            )
            impact = st.number_input(
                f'Impact (0-20)', 
                min_value=0, 
                max_value=20,  
                key=f'impact_{i}',
                help="""
                **Impact /20**
                - Trivial. Has no/low impact on the site/app. Does not affect user experience: **0**
                - Minor. Has low impact on the site/app. User will notice but won’t affect user experience: **4**
                - Starts to hurt. Has a decent impact on the site/app. User experience will be slightly affected: **8**
                - Major. Has a strong impact on the site/app. User experience is strongly affected: **12**
                - Direct loss of revenue: **16**
                - Critical! Blocks progress, a legal issue, crashes, 500 errors etc…: **20**
                """
            )
            likelihood = st.number_input(
                f'Likelihood (0-20)', 
                min_value=0, 
                max_value=20,  
                key=f'likelihood_{i}',
                help="""
                **Likelihood /20**
                - Most unlikely (0% users): **0**
                - Slightly unlikely (1–33% users): **5**
                - Likely (34–66% users): **10**
                - Strongly likely (67–99% users): **15**
                - Definitely (100% users): **20**
                """
            )
            workaround = st.number_input(
                f'Workaround (0-20)', 
                min_value=0, 
                max_value=20, 
                key=f'workaround_{i}',
                help="""
                **Is there a workaround? /20**
                - Quite easy to get around the issue (or a piece of config): **5**
                - Workaround exists, happy to put in front of users short term: **10**
                - Workaround exists, NOT happy to put in front of users: **15**
                - No Workaround: **20**
                """
            )

            st.session_state['bug_scores'][i] = [bug_type, impact, likelihood, workaround]
            st.session_state['bug_names'][i] = bug_name

            # Save expander state
            st.session_state['bug_expanded'][i] = True * 10 # Keep expander open

    if st.sidebar.button('Plot Bug Priorities'):
        # Update session state labels from temporary labels
        st.session_state['bug_names'] = st.session_state['temp_bug_names'][:]

        fig = plot_bug_priorities(st.session_state['bug_scores'][:num_bugs], st.session_state['bug_names'][:num_bugs])
        st.pyplot(fig)
