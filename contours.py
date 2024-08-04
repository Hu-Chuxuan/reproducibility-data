import cv2
import numpy as np
from tqdm import tqdm

colors = [
    (0, 0, 0),     # Black
    (128, 128, 128), # Gray
    (255, 0, 0),   # Blue
    (0, 255, 255),  # Yellow
    (0, 0, 255),   # Red
    (255, 255, 0), # Cyan
    (255, 0, 255), # Magenta
    (0, 255, 0),   # Green
]

def manhattan_distance(p, contour):
    dist = 999999999
    for point in contour:
        dist = min(dist, abs(p[0] - point[0][0]) + abs(p[1] - point[0][1]))
    return dist

def is_inside(cornors, contours, w, h):
    for contour in contours:
        for cornor in cornors:
            if cv2.pointPolygonTest(contour, cornor, False) >= 0:
                return True
    return False

def get_potential_position(point, contours, text, w, h):
    res = []
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    offset = 1
    positions = [
        (point[0] + offset, point[1] + text_height // 2),  # Right
        (point[0] - text_width - offset, point[1] + text_height // 2),  # Left
        (point[0] - text_width // 2, point[1] - offset),  # Above
        (point[0] - text_width // 2, point[1] + text_height + offset)  # Below
    ]

    # Check if the text box intersects with the contour for each position
    for pos in positions:
        text_box = [
            (pos[0], pos[1]),
            (pos[0] + text_width, pos[1]),
            (pos[0] + text_width, pos[1] - text_height),
            (pos[0], pos[1] - text_height)
        ]
        x_min, x_max = pos[0], pos[0] + text_width
        y_min, y_max = pos[1] - text_height, pos[1]
        if x_max >= w - offset or x_min <= offset or y_max >= h - offset or y_min <= offset:
            continue
        if not is_inside(text_box, contours, w, h):
            res.append(pos)
    return res

def get_label_positions(contours, w, h):
    label_positions = []
    for i, contour in tqdm(enumerate(contours)):
        max_dist_sum = 0
        max_dist_min = 0
        label_position = contour[0][0]
        for point in contour:
            positions = get_potential_position(point[0], contours, str(i), w, h)
            for p in positions:
                dist_sum = 0
                min_dist = 99999999
                for j, contour in enumerate(contours):
                    if i == j:
                        continue
                    dist = manhattan_distance(p, contour)
                    dist_sum += dist
                    min_dist = min(min_dist, dist)
                if dist_sum > max_dist_sum or (dist_sum == max_dist_sum and min_dist > max_dist_min):
                    max_dist_sum = dist_sum
                    max_dist_min = min_dist
                    label_position = p
        label_positions.append(tuple(label_position))

    return label_positions

repeat = 3
kernel_sz = 5
max_scale = 2
min_area = 100

def is_contour_closed(contour):
    return cv2.contourArea(contour) > cv2.arcLength(contour, True)

def find_lines(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

    vertical_lines = []
    horizontal_lines = []
    for line in lines:
        rho, theta = line[0]
        if abs(theta - np.pi / 2) < np.pi / 6:
            horizontal_lines.append((rho, theta))
        elif abs(theta) < np.pi / 10:
            vertical_lines.append((rho, theta))
    cv2.imwrite("lines.png", image)
    return horizontal_lines, vertical_lines

def is_black(color):
    # cast to float
    color = color.astype(np.float)
    min_color = min(color)
    max_color = max(color)
    if min_color == 0 and max_color != 0:
        return False
    return  (max_color - min_color) / (min_color + 1e-8) < 0.35 and min_color < 150

def clear_color(image):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if is_black(image[i, j]):
                image[i, j] = [0, 0, 0]
            else:
                image[i, j] = [255, 255, 255]
    return image

def draw_contours(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    for i in range(repeat):
        gray_image = cv2.GaussianBlur(gray_image, (kernel_sz, kernel_sz), 0)
        edges = cv2.Canny(gray_image, 50, 150)
        if i < repeat-1:
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for j, contour in enumerate(iterable=contours):
                cv2.drawContours(gray_image, [contour], -1, (0, 0, 0), max_scale)
            cv2.imwrite(f"test/grey_{i}.png", gray_image)
        else:
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            final_contours = []
            for contour in contours:
                if cv2.contourArea(contour) < min_area or contour_to_points(contour, "vertical") is None or contour_to_points(contour, "horizontal") is None:
                    continue
                final_contours.append(contour)
            
            # Mask every outside contours and leave every black points in the last grey image
            # mask = np.all(gray_image != 0) # Set all non-black points to 255
            # gray_image[mask] = 255
            # gray_image = cv2.bitwise_not(gray_image) # Reserve the black points
            # cv2.drawContours(gray_image, final_contours, -1, 255, -1) # Fill the edge of contours with white
            # image = cv2.bitwise_and(image, image, mask=gray_image)
            # cv2.imwrite("contours_mask.png", image)

            # label_positions = get_label_positions(final_contours, image.shape[1], image.shape[0])
            colors = [np.random.randint(0, 256, 3).tolist() for _ in range(len(final_contours))]
            for j, contour in enumerate(final_contours):
                cv2.drawContours(image, [contour], -1, colors[j], 1)
                # cv2.putText(image, str(j), label_positions[j], cv2.FONT_HERSHEY_SIMPLEX, 1, colors[j], 2)

            return final_contours, image, colors

def contour_to_points(contour, direction):
    w, h = max(contour[:, 0, 0]), max(contour[:, 0, 1])
    image = np.zeros((h+5, w+5, 3), np.uint8)
    cv2.drawContours(image, [contour], -1, (255, 255, 255), 1)
    x_min, y_min = min(contour[:, 0, 0]), min(contour[:, 0, 1])
    x_max, y_max = w, h
    
    # Unify the direction
    ind_values = {}
    if direction == "vertical":
        for x in range(x_min, x_max):
            y_values = np.where(image[y_min:y_max+1, x] == 255)[0] + y_min
            if len(y_values) <= 1:
                return None
            ind_values[x] = y_values
    else:
        for y in range(y_min, y_max):
            x_values = np.where(image[y, x_min:x_max] == 255)[0] + x_min
            if len(x_values) <= 1:
                return None
            ind_values[y] = x_values
    
    return ind_values

def estimate_dots(contour, direction):
    ind_values = contour_to_points(contour, direction)

    # Calculate the average height of the contour
    avg = 0
    for _, deps in ind_values.items():
        avg += max(deps) - min(deps)
    avg /= len(ind_values)

    # Filter the points with smaller height
    points = []
    for ind, deps in ind_values.items():
        if max(deps) - min(deps) > avg * 1.2:
            points.append((ind, (max(deps) + min(deps)) // 2))
    
    # Merge the points
    res = []
    i = 0
    while i < len(points):
        # Search for the points of the same dot
        j = i + 1
        dep = points[i][1]
        while j < len(points) and points[j][0] - points[j-1][0] < 3:
            dep += points[j][1]
            j += 1
        # Estimate the position as the average of the points
        dep //= j - i
        ind = (points[j-1][0] + points[i][0]) // 2
        if direction == "horizontal":
            res.append((dep, ind))
        else:
            res.append((ind, dep))
        i = j
    return res

def find_axis_line(contour, axis, cv_lines):
    same_dir_values = contour_to_points(contour, axis)
    
    # Find the axis as the longest line
    lines = []
    lines_len_sum = 0
    max_length = 0
    total_sum = 0
    for i, values in same_dir_values.items():
        if len(values) < 2:
            continue
        length = max(values) - min(values)
        total_sum += length
        if max_length < length * 0.95:
            lines = [i]
            max_length = length
            lines_len_sum = length
        elif length > max_length * 0.95:
            lines.append(i)
            max_length = max(max_length, length)
            lines_len_sum += length
    avg = (total_sum - lines_len_sum) // (len(same_dir_values) - len(lines))

    if avg * 2 < max_length:
        line_lo, line_hi = min(lines), max(lines)
        # Find straight line among the longest lines
        for ind in lines:
            len_inline = len(same_dir_values[ind])
            if ind-1 in same_dir_values:
                len_inline += len(same_dir_values[ind-1])
            if ind+1 in same_dir_values:
                len_inline += len(same_dir_values[ind+1])
            if max_length <= len_inline:
                axis_coor = (line_lo + line_hi) // 2
                for l in cv_lines:
                    if abs(l[0] - axis_coor) < 5:
                        return same_dir_values, axis_coor, line_hi - line_lo
        return same_dir_values, None, None
    else:
        return same_dir_values, None, None

# TODO: Handle when other_axis_coor is None
def find_ticks(contours, hori_line, vert_line):
    for i, contour in enumerate(contours):
        hori_values, hori_coor, hori_height = find_axis_line(contour, "horizontal", hori_line)
        vert_values, vert_coor, vert_height = find_axis_line(contour, "vertical", vert_line)
        if hori_coor is None or vert_coor is None:
            continue
        hori_ticks = estimate_ticks(vert_coor, hori_coor, vert_values, hori_height, "x")
        vert_ticks = estimate_ticks(hori_coor, vert_coor, hori_values, vert_height, "y")
        return hori_ticks, vert_ticks
    return None, None

def estimate_ticks(other_axis_coor, axis_coor, ind_values, line_height, axis):
    # Filter data points taller than line
    # MARK: Assuming y-axis is at the left end of x-axis and x-axis is at the bottom of y-axis
    tick_pts = [[other_axis_coor]]
    for ind in sorted(ind_values.keys(), reverse=axis == "y"):
        deps = ind_values[ind]
        if line_height * 1.5 < max(deps) - min(deps):
            # print(ind, max(deps) - min(deps), line_height * 1.1)
            if (axis == "x" and ind > other_axis_coor) or (axis == "y" and ind < other_axis_coor):
                if abs(ind - tick_pts[-1][-1]) > 2:
                    tick_pts.append([ind])
                else:
                    tick_pts[-1].append(ind)
    tick_pts[0] = tick_pts[0][:1]
    ticks = []
    for tick in tick_pts:
        if axis == "x":
            ticks.append(((max(tick) + min(tick)) // 2, axis_coor))
        else:
            ticks.append((axis_coor, (max(tick) + min(tick)) // 2))
    return ticks

def estimate_bars(contour):
    pass

if __name__ == "__main__":
    image = cv2.imread("Samples/107/O1.png")
    contours, image = draw_contours(image)
    dots = estimate_dots(contours[5], "vertical")
    for dot in dots:
        cv2.circle(image, dot, 3, (255, 255, 0), -1)
    dots = estimate_dots(contours[6], "vertical")
    for dot in dots:
        cv2.circle(image, dot, 3, (255, 255, 0), -1)
    dots = estimate_axis(contours[7], "x")
    for dot in dots:
        cv2.circle(image, dot, 5, (0, 0, 255), -1)
    dots = estimate_axis(contours[7], "y")
    for dot in dots:
        cv2.circle(image, dot, 5, (0, 0, 255), -1)
    cv2.imwrite("dots.png", image)
    print(dots)