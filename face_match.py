import face_recognition
import os
import shutil
from PIL import Image

def match_faces(user_image_path, event_photos_dir, matched_dir, tolerance=0.35):
    # Load user's selfie
    user_img = face_recognition.load_image_file(user_image_path)
    user_encoding = face_recognition.face_encodings(user_img)
    
    if not user_encoding:
        return []

    user_encoding = user_encoding[0]

    matched_photos = []

    # Clear old matches
    if os.path.exists(matched_dir):
        shutil.rmtree(matched_dir)
    os.makedirs(matched_dir)

    # Loop through event photos
    for filename in os.listdir(event_photos_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue  # Skip non-image files like .DS_Store
        filepath = os.path.join(event_photos_dir, filename)
        event_img = face_recognition.load_image_file(filepath)


        # Find faces in event photo
        encodings = face_recognition.face_encodings(event_img)
        
        print(f"Comparing with: {filename}")

        for encoding in encodings:
            match = face_recognition.compare_faces([user_encoding], encoding, tolerance)[0]
            if match:
                # Save matched photo
                dest = os.path.join(matched_dir, filename)
                shutil.copyfile(filepath, dest)
                matched_photos.append(filename)
                print(f"✅ Match found in {filename}")
                break  # Move to next photo if match found

    return matched_photos
