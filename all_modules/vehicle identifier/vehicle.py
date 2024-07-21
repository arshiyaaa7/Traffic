import cv2
import numpy as np

# Open the video file
cap = cv2.VideoCapture("intersection_1.mp4")

min_width_react = 80
min_height_react = 80
# Initialize background subtractor
algo = cv2.bgsegm.createBackgroundSubtractorMOG()


# function of count
def center_handle(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


detect = []

offset = 6
counter = 0

# Define the count line position
count_line_position = 550  # You can set this to the desired position

# Read video
while True:
    ret, frame1 = cap.read()
    if not ret:
        break

    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)

    # Apply the background subtraction algorithm
    img_sub = algo.apply(blur)

    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contourShape, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the count line
    cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (255, 127, 0), 3)

    for (i, c) in enumerate(contourShape):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_counter = (w >= min_width_react) and (h >= min_height_react)

        if not validate_counter:
            continue

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # giving circle so that we count the no of car pointed by circle
        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)

        # counting
        for (x, y) in detect:
            if y < (count_line_position + offset) and y > (count_line_position - offset):
                counter += 1
            cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (0, 127, 255), 3)
            detect.remove((x, y))
            print("car count:" + str(counter))

    cv2.putText(frame1, "car counter:" + str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    # Display the processed frame
    # cv2.imshow('Detector', dilatada)

    # Display the original frame
    cv2.imshow('Video original', frame1)

    # Increase the wait time (e.g., 100 milliseconds)
    if cv2.waitKey(100) == 13:  # 100 ms delay
        break

# Release resources
cv2.destroyAllWindows()
cap.release()