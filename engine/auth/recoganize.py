import cv2
import numpy as np
from PIL import Image
import os
import json
import subprocess
import sys

class FaceAuthSystem:
    def __init__(self):
        self.base_path = 'engine/auth'
        self.samples_path = f'{self.base_path}/samples'
        self.trainer_path = f'{self.base_path}/trainer'
        self.cascade_file = f'{self.base_path}/haarcascade_frontalface_default.xml'
        self.users_file = f'{self.base_path}/users.json'
        self.model_file = f'{self.trainer_path}/trainer.yml'
        
        # Create directories
        os.makedirs(self.samples_path, exist_ok=True)
        os.makedirs(self.trainer_path, exist_ok=True)
        
        # Load users database
        self.users = self.load_users()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def get_next_id(self):
        """Get next available user ID"""
        if not self.users:
            return 1
        return max([int(k) for k in self.users.keys()]) + 1
    
    def collect_samples(self):
        """Collect face samples for a new user"""
        print("\n" + "="*60)
        print("COLLECT FACE SAMPLES")
        print("="*60)
        
        # Get user details
        name = input("Enter user name: ").strip()
        if not name:
            print("[ERROR] Name cannot be empty!")
            return
        
        # Check if user exists
        for uid, data in self.users.items():
            if data['name'].lower() == name.lower():
                print(f"[ERROR] User '{name}' already exists with ID {uid}")
                return
        
        user_id = self.get_next_id()
        print(f"[INFO] Assigned User ID: {user_id}")
        
        # Initialize camera
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)
        
        detector = cv2.CascadeClassifier(self.cascade_file)
        
        if detector.empty():
            print("[ERROR] Could not load Haar Cascade file!")
            cam.release()
            return
        
        print(f"\n[INFO] Collecting samples for: {name}")
        print("[INFO] Look at the camera...")
        print("[INFO] Press 'ESC' to stop early\n")
        
        count = 0
        min_face_size = (100, 100)
        
        while True:
            ret, img = cam.read()
            
            if not ret:
                print("[ERROR] Failed to grab frame")
                break
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=min_face_size,
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                padding = 10
                y1 = max(0, y - padding)
                y2 = min(img.shape[0], y + h + padding)
                x1 = max(0, x - padding)
                x2 = min(img.shape[1], x + w + padding)
                
                face_color = img[y1:y2, x1:x2]
                count += 1
                
                filename = f"{self.samples_path}/face.{user_id}.{count}.jpg"
                cv2.imwrite(filename, face_color)
                
                cv2.putText(img, f"Sample: {count}/100", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if len(faces) == 0:
                cv2.putText(img, "No face detected", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elif len(faces) > 1:
                cv2.putText(img, "Multiple faces detected!", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
            
            cv2.imshow('Face Sample Collection', img)
            
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                print("\n[INFO] Stopped by user")
                break
            elif count >= 100:
                print("\n[INFO] Sample collection complete!")
                break
        
        cam.release()
        cv2.destroyAllWindows()
        
        if count >= 50:
            self.users[str(user_id)] = {
                'name': name,
                'samples': count
            }
            self.save_users()
            print(f"[SUCCESS] User '{name}' registered with ID {user_id}")
            print(f"[INFO] {count} samples collected")
            print("[IMPORTANT] Run 'Train Model' to activate this user")
        else:
            print(f"[ERROR] Only {count} samples collected. Need at least 50.")
    
    def train_model(self):
        """Train the face recognition model"""
        print("\n" + "="*60)
        print("TRAIN FACE RECOGNITION MODEL")
        print("="*60)
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(self.cascade_file)
        
        path = self.samples_path
        image_paths = [os.path.join(path, f) for f in os.listdir(path) 
                      if f.endswith('.jpg')]
        
        if not image_paths:
            print("[ERROR] No training samples found!")
            print("[ERROR] Please collect samples first")
            return
        
        face_samples = []
        ids = []
        
        print(f"[INFO] Found {len(image_paths)} images")
        print("[INFO] Processing images...")
        
        for image_path in image_paths:
            try:
                img = Image.open(image_path).convert('L')
                img_numpy = np.array(img, 'uint8')
                
                id = int(os.path.split(image_path)[-1].split(".")[1])
                
                face_samples.append(img_numpy)
                ids.append(id)
                
            except Exception as e:
                print(f"[WARNING] Error processing {image_path}: {e}")
                continue
        
        if not face_samples:
            print("[ERROR] No valid training data found!")
            return
        
        unique_ids = list(set(ids))
        print(f"\n[INFO] Training for {len(unique_ids)} user(s)")
        print(f"[INFO] User IDs: {unique_ids}")
        print(f"[INFO] Total samples: {len(face_samples)}")
        
        print("\n[INFO] Training model (this may take a moment)...")
        recognizer.train(face_samples, np.array(ids))
        recognizer.write(self.model_file)
        
        print("[SUCCESS] Model trained successfully!")
        print(f"[INFO] Model saved to: {self.model_file}")
    
    def run_recognition(self):
        """Run face recognition system"""
        print("\n" + "="*60)
        print("FACE RECOGNITION SYSTEM")
        print("="*60)
        
        if not os.path.exists(self.model_file):
            print("[ERROR] No trained model found!")
            print("[ERROR] Please train the model first")
            return
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(self.model_file)
        
        face_cascade = cv2.CascadeClassifier(self.cascade_file)
        
        # Create names dictionary
        names = {int(uid): data['name'] for uid, data in self.users.items()}
        
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)
        
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        CONFIDENCE_THRESHOLD = 60
        
        print(f"\n[INFO] Registered Users: {list(names.values())}")
        print(f"[INFO] Confidence Threshold: {CONFIDENCE_THRESHOLD}%")
        print("\n[INFO] Press 'ESC' to exit")
        print("[INFO] Press 'S' to save screenshot\n")
        
        screenshot_count = 0
        
        while True:
            ret, img = cam.read()
            
            if not ret:
                break
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH))
            )
            
            for (x, y, w, h) in faces:
                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                
                if confidence < 100:
                    match_percentage = round(100 - confidence, 2)
                else:
                    match_percentage = 0
                
                if match_percentage >= CONFIDENCE_THRESHOLD:
                    name = names.get(id, f"Unknown_ID_{id}")
                    color = (0, 255, 0)
                    status = "AUTHENTICATED"
                else:
                    name = "Unknown"
                    color = (0, 0, 255)
                    status = "DENIED"
                
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                cv2.rectangle(img, (x, y-35), (x+w, y), color, cv2.FILLED)
                cv2.putText(img, name, (x+5, y-10), font, 0.7, (255, 255, 255), 2)
                cv2.putText(img, f"{match_percentage}% - {status}", (x+5, y+h+25),
                           font, 0.6, color, 2)
            
            cv2.putText(img, "ESC: Exit | S: Screenshot", (10, 25),
                       font, 0.5, (255, 255, 255), 1)
            cv2.putText(img, f"Faces: {len(faces)}", (10, img.shape[0]-10),
                       font, 0.5, (255, 255, 255), 1)
            
            cv2.imshow('Face Recognition', img)
            
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break
            elif k == ord('s') or k == ord('S'):
                screenshot_count += 1
                screenshot_path = f'screenshot_{screenshot_count}.jpg'
                cv2.imwrite(screenshot_path, img)
                print(f"[INFO] Screenshot saved: {screenshot_path}")
        
        cam.release()
        cv2.destroyAllWindows()
        print("\n[INFO] Recognition system stopped")
    
    def list_users(self):
        """List all registered users"""
        print("\n" + "="*60)
        print("REGISTERED USERS")
        print("="*60)
        
        if not self.users:
            print("No users registered yet.\n")
            return
        
        print(f"{'ID':<6} {'Name':<25} {'Samples':<10}")
        print("-" * 60)
        
        for uid in sorted(self.users.keys(), key=lambda x: int(x)):
            data = self.users[uid]
            print(f"{uid:<6} {data['name']:<25} {data['samples']:<10}")
        
        print()
    
    def delete_user(self):
        """Delete a user"""
        self.list_users()
        
        if not self.users:
            return
        
        user_id = input("Enter User ID to delete: ").strip()
        
        if user_id not in self.users:
            print(f"[ERROR] User ID {user_id} not found!")
            return
        
        name = self.users[user_id]['name']
        confirm = input(f"Delete '{name}' (ID: {user_id})? (yes/no): ").lower()
        
        if confirm == 'yes':
            # Delete sample files
            deleted = 0
            for f in os.listdir(self.samples_path):
                if f.startswith(f"face.{user_id}."):
                    os.remove(os.path.join(self.samples_path, f))
                    deleted += 1
            
            del self.users[user_id]
            self.save_users()
            
            print(f"[SUCCESS] User '{name}' deleted!")
            print(f"[INFO] Removed {deleted} sample images")
            print("[IMPORTANT] Run 'Train Model' to update the system")
        else:
            print("[INFO] Deletion cancelled")


def recoganize():
    print("""
╔══════════════════════════════════════════════════════════╗
║        FACE AUTHENTICATION MANAGEMENT SYSTEM             ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    system = FaceAuthSystem()
    
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Collect Face Samples (Register New User)")
        print("2. Train Recognition Model")
        print("3. Start Face Recognition")
        print("4. List All Users")
        print("5. Delete User")
        print("6. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            system.collect_samples()
        elif choice == '2':
            system.train_model()
        elif choice == '3':
            system.run_recognition()
        elif choice == '4':
            system.list_users()
        elif choice == '5':
            system.delete_user()
        elif choice == '6':
            print("\n[INFO] Thank you for using Face Authentication System!")
            print("[INFO] Goodbye!\n")
            break
        else:
            print("[ERROR] Invalid choice! Please enter 1-6")
def AuthenticateFace():
    """
    Automatic face authentication.
    - Returns True if a known user is recognized.
    - Returns False if not recognized after several attempts.
    - Automatically stops without manual intervention.
    """
    system = FaceAuthSystem()
    
    if not os.path.exists(system.model_file):
        print("[ERROR] No trained model found!")
        return False

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(system.model_file)
    face_cascade = cv2.CascadeClassifier(system.cascade_file)
    names = {int(uid): data['name'] for uid, data in system.users.items()}

    cam = cv2.VideoCapture(0)
    CONFIDENCE_THRESHOLD = 60
    max_attempts = 20  # stop if too many failed recognitions
    attempt_count = 0
    recognized = False

    while attempt_count < max_attempts:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        if len(faces) == 0:
            attempt_count += 1
            continue  # no face detected, try again

        for (x, y, w, h) in faces:
            id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            match_percent = max(0, round(100 - confidence, 2))

            if match_percent >= CONFIDENCE_THRESHOLD:
                recognized = True
                user_name = names.get(id_, f"Unknown_ID_{id_}")
                print(f"[ACCESS GRANTED] {user_name} ({match_percent}%)")
                break
            else:
                attempt_count += 1
                print(f"[ACCESS DENIED] Unknown ({match_percent}%)")

        if recognized:
            break

    cam.release()
    cv2.destroyAllWindows()

    if not recognized:
        print("[ACCESS FAILED] No registered user recognized.")

    # Save result to auth_result.json
    with open(f"{system.base_path}/auth_result.json", "w") as f:
        json.dump({"authenticated": recognized}, f)

    return recognized


if __name__ == "__main__":
    # recoganize()
    def AuthenticateFace():
   
     system = FaceAuthSystem()
     system.run_recognition()
     return True
