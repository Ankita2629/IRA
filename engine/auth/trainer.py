# import cv2
# import numpy as np
# from PIL import Image #pillow package
# import os

# path = 'engine\\auth\\samples' # Path for samples already taken

# recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
# detector = cv2.CascadeClassifier("engine\\auth\\haarcascade_frontalface_default.xml")
# #Haar Cascade classifier is an effective object detection approach


# def Images_And_Labels(path): # function to fetch the images and labels

#     imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
#     faceSamples=[]
#     ids = []

#     for imagePath in imagePaths: # to iterate particular image path

#         gray_img = Image.open(imagePath).convert('L') # convert it to grayscale
#         img_arr = np.array(gray_img,'uint8') #creating an array

#         id = int(os.path.split(imagePath)[-1].split(".")[1])
#         faces = detector.detectMultiScale(img_arr)

#         for (x,y,w,h) in faces:
#             faceSamples.append(img_arr[y:y+h,x:x+w])
#             ids.append(id)

#     return faceSamples,ids

# print ("Training faces. It will take a few seconds. Wait ...")

# faces,ids = Images_And_Labels(path)
# recognizer.train(faces, np.array(ids))

# recognizer.write('engine\\auth\\trainer\\trainer.yml')  # Save the trained model as trainer.yml

# print("Model trained, Now we can recognize your face.")


import cv2
import numpy as np
from PIL import Image
import os

# Create trainer directory if it doesn't exist
os.makedirs('engine/auth/trainer', exist_ok=True)

# Initialize face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Path to sample images
path = 'engine/auth/samples'

def get_images_and_labels(path):
    """
    Get all face images and their labels from the samples directory
    """
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    
    face_samples = []
    ids = []
    
    print(f"[INFO] Found {len(image_paths)} images")
    
    for image_path in image_paths:
        try:
            # Load image and convert to grayscale
            img = Image.open(image_path).convert('L')
            img_numpy = np.array(img, 'uint8')
            
            # Extract ID from filename (face.ID.number.jpg)
            id = int(os.path.split(image_path)[-1].split(".")[1])
            
            face_samples.append(img_numpy)
            ids.append(id)
            
        except Exception as e:
            print(f"[WARNING] Error processing {image_path}: {e}")
            continue
    
    return face_samples, ids

print("[INFO] Training faces. This may take a few moments...")

# Get all face samples and IDs
faces, ids = get_images_and_labels(path)

if len(faces) == 0:
    print("[ERROR] No training samples found!")
    print("[ERROR] Please run the sample collection script first")
    exit()

# Get unique IDs
unique_ids = list(set(ids))
print(f"[INFO] Training for {len(unique_ids)} person(s): {unique_ids}")
print(f"[INFO] Total training samples: {len(faces)}")

# Train the recognizer
recognizer.train(faces, np.array(ids))

# Save the trained model
model_path = 'engine/auth/trainer/trainer.yml'
recognizer.write(model_path)

print(f"[INFO] Model trained successfully!")
print(f"[INFO] Model saved to: {model_path}")
print(f"[INFO] You can now use the recognition script")