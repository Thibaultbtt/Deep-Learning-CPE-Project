import cv2
import numpy as np
from PIL import Image, ImageFilter
import os
import random

def apply_gaussian_blur(img, kernel_size=5):
    """
    Applique un flou gaussien à une image.
    """
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def add_gaussian_noise(img, mean=0, std=25):
    """
    Ajoute un bruit gaussien à une image.
    """
    # Convertir l'image en tableau numpy
    img_array = np.array(img, dtype=np.float32)

    # Générer du bruit gaussien
    std = 10
    noise = np.random.normal(mean, std, img_array.shape)
    noisy_img = img_array + noise

    # Limiter les valeurs entre 0 et 255
    noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)
    return noisy_img

def process_images_with_effects(source_dir, target_dir, apply_blur=True, apply_noise=True):
    """
    Applique flou et bruit aux images redimensionnées.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            file_path = os.path.join(source_dir, filename)
            save_path = os.path.join(target_dir, filename)

            # Charger l'image
            with Image.open(file_path) as img:
                # Convertir en BGR pour OpenCV
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                # Appliquer flou gaussien
                # if apply_blur and random.random() < 0.3:  # 50% de chances d'ajouter un flou
                #     kernel_size = random.choice([3, 5, 7])  # Taille du noyau aléatoire
                #     kernel_size = 3  # Taille du noyau fixe
                #     img_cv = apply_gaussian_blur(img_cv, kernel_size=kernel_size)

                # Appliquer bruit gaussien
                if apply_noise and random.random() > 0.3:  # 50% de chances d'ajouter du bruit
                    img_cv = add_gaussian_noise(img_cv, mean=0, std=random.randint(15, 40))

                # Convertir en RGB et sauvegarder
                final_img = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
                final_img.save(save_path)
                print(f"Processed and saved: {save_path}")

# Répertoires
source_directory = "./Deep-Learning-Cpe-Project/AlgorithmePreProcess/resized_images"  # Changez avec votre chemin
target_directory = "./Deep-Learning-Cpe-Project/AlgorithmePreProcess/final_images"  # Répertoire cible

# Appliquer flou et bruit
process_images_with_effects(source_directory, target_directory, apply_blur=True, apply_noise=True)
