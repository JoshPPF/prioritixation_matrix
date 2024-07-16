# Sample data including an example of P4
bug_names = ["Bug 1", "Bug 2", "Bug 3", "Bug 4", "Bug 5"]
bug_scores = [
    [16, 12, 10, 5],  # Bug 1
    [20, 8, 5, 15],   # Bug 2
    [12, 16, 15, 10], # Bug 3
    [8, 20, 20, 20],  # Bug 4
    [4, 8, 5, 10],    # Bug 5 (P4 example)
]

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
for i, score in enumerate(total_scores):
    ax.text(bar_positions[i], total_scores[i] + 1, labels[i], ha='center', va='bottom')

# Customize the chart
ax.set_xlabel("Bugs")
ax.set_ylabel("Scores")
ax.set_title("Bug Scoring System")
ax.set_xticks(bar_positions)
ax.set_xticklabels(bug_names)
ax.set_ylim(0, 80)

# Show the chart
plt.show()
