import pygame

import math
from collections import Counter
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
NODE_COLOR = (0, 0, 255)
NODE_RADIUS = 20
FONT_COLOR = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Real-Time Decision Trees in Pygame AI')
font = pygame.font.SysFont(None, 24)

# Decision Tree settings
tree_depth = 3

# Load and split the Iris dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.5, random_state=42)

# Build the Decision Tree
clf = DecisionTreeClassifier(max_depth=tree_depth)
clf.fit(X_train, y_train)

# Function to recursively draw the decision tree
def draw_tree(surface, tree, x, y, width, level=0):
    if tree.tree_.children_left[level] == tree.tree_.children_right[level]:  # Check if it is a leaf
        label = Counter(y_train[tree.apply(X_train) == level]).most_common(1)[0][0]
        text = font.render(iris.target_names[label], True, FONT_COLOR)
    else:
        feature = iris.feature_names[tree.tree_.feature[level]]
        threshold = round(tree.tree_.threshold[level], 2)
        text = font.render(f'{feature} <= {threshold}', True, FONT_COLOR)
    surface.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    pygame.draw.circle(surface, NODE_COLOR, (x, y), NODE_RADIUS)
    
    left = tree.tree_.children_left[level]
    right = tree.tree_.children_right[level]

    if left != -1:  # draw left branch
        next_x = x - width // 2
        next_y = y + 100
        pygame.draw.line(surface, NODE_COLOR, (x, y), (next_x, next_y))
        draw_tree(surface, tree, next_x, next_y, width // 2, left)
    
    if right != -1:  # draw right branch
        next_x = x + width // 2
        next_y = y + 100
        pygame.draw.line(surface, NODE_COLOR, (x, y), (next_x, next_y))
        draw_tree(surface, tree, next_x, next_y, width // 2, right)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the decision tree
    draw_tree(screen, clf, SCREEN_WIDTH // 2, 100, SCREEN_WIDTH // 2)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()