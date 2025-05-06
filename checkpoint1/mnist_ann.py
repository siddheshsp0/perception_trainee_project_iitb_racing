
from keras import Sequential
from keras.layers import Flatten, Dense, BatchNormalization
from keras.datasets.mnist import load_data
import numpy as np
import cv2

(x_train, y_train), (x_test, y_test) = load_data()

x_train, x_test = x_train/255.0, x_test/255.0


model = Sequential([
    Flatten(input_shape = (28, 28)),
    Dense(128, activation='relu'),
    BatchNormalization(axis=1),
    Dense(64, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=20, verbose=2, shuffle=True, batch_size=100)

# test_loss, test_acc = model.evaluate(x_test, y_test)

# Copied from chatgpt
import numpy as np
import cv2

# Initialize a black canvas (28x28 pixels)
canvas = np.zeros((280, 280), dtype=np.uint8)  # Scaled up 10x for better drawing
drawing = False  # True when mouse is pressed

# Mouse callback function
def draw(event, x, y, flags, param):
    global drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(canvas, (x, y), 10, (255, 255, 255), -1)  # Draw white
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

# Create a window and bind the function
cv2.namedWindow("Draw (Press 's' to save)")
cv2.setMouseCallback("Draw (Press 's' to save)", draw)

while True:
    cv2.imshow("Draw (Press 's' to save)", canvas)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # Press 's' to save
        break

cv2.destroyAllWindows()

# Resize to 28x28 and normalize
digit = cv2.resize(canvas, (28, 28), interpolation=cv2.INTER_AREA)
digit = digit / 255.0  # Normalize (0 to 1)

# Convert to NumPy array
digit_array = np.array(digit)


print('\n\n\n\n')
print(f'digitarray shape {digit_array.shape} xtrain shape: {x_train.shape}')
# model.predict(digit_array)



