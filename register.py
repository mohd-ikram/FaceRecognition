import cv2 as cv
import os


def capture_and_save_image(file_name):
    message = "File can not be saved"
    directory = "./resources/"
    """
    Captures an image from the webcam, allows the user to preview,
    and saves it to the specified directory with a timestamped filename.

    Args:
        directory (str): The directory path where the image will be saved.
    """

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)  # Safe directory creation

    # Initialize video capture
    cap = cv.VideoCapture(0)

    # Check if webcam is opened successfully
    if not cap.isOpened():
        message = "Error opening webcam!"
        print(message)
        return message

    # Capture frame-by-frame
    while True:
        # Capture frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv.imshow('Preview', frame)

        # Press 'q' to quit or 's' to save the image
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Generate a timestamped filename
            # timestamp = str(int(time.time()))  # Import time module if needed
            filename = os.path.join(directory, f"{file_name}.jpg")

            # Save the frame as an image
            cv.imwrite(filename, frame)
            print(f"Image saved to: {filename}")
            message = f"Image saved to: {filename}"
            break
    # Release the capture and close all windows
    cap.release()
    cv.destroyAllWindows()

    return message