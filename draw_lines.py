import cv2
import numpy as np

# Load the image
image = cv2.imread('Samples/107/O1.png')

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Sharpen lines
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
gray_image = cv2.filter2D(gray_image, -1, kernel)

# Apply edge detection
edges = cv2.Canny(gray_image, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
axis = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if (w < 10 and h > 40) or (h < 10 and w > 40):
        axis.append(contour)

# Step 4: Line Detection
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

# Create a list of colors
colors = [
    (255, 0, 0),   # Blue
    (0, 255, 0),   # Green
    (0, 0, 255),   # Red
    (255, 255, 0), # Cyan
    (255, 0, 255), # Magenta
    (0, 255, 255)  # Yellow
]

# Draw each contour with a different color
# print(len(axis))
# for i, axis in enumerate(axis):
#     cv2.drawContours(image, [axis], -1, colors[i%len(colors)], 2)

def is_equal(a, b):
    return abs(a - b) < np.pi / 100

selected_lines = []
selected_contours = []
for line in lines:
    rho, theta = line[0]
    if is_equal(theta, 0) or is_equal(theta, np.pi / 2) or is_equal(theta, np.pi) or is_equal(theta, 3 * np.pi / 2):
        for contour in axis:
            x, y, w, h = cv2.boundingRect(contour)
            if (abs(rho - x) < w and (is_equal(theta, 0) or is_equal(theta, np.pi))) or \
               (abs(rho - y) < h) and (is_equal(theta, np.pi / 2) or is_equal(theta, 3 * np.pi / 2)):
                flag = False
                for prev_line in selected_lines:
                    if abs(prev_line[0][0] - rho) < 5 and is_equal(prev_line[0][1], theta):
                        flag = True
                        break
                if not flag:
                    selected_contours.append(contour)
                    selected_lines.append(line)
                break

print(len(selected_lines))
for line in selected_lines:
    print("="*50)
    print(line)
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# for contour in selected_contours:
#     cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)

# Display the result
cv2.imwrite('contours.png', image)