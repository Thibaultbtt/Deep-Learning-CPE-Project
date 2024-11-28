from PIL import Image
import os
import numpy as np

def calculate_median_size(image_paths):
    """Calcule la médiane des tailles (largeur, hauteur) des images."""
    dimensions = []
    for path in image_paths:
        with Image.open(path) as img:
            dimensions.append(img.size)  # (width, height)
    # Convertir en array numpy pour un calcul facile
    dimensions = np.array(dimensions)
    median_width = int(np.median(dimensions[:, 0]))
    median_height = int(np.median(dimensions[:, 1]))
    return median_width, median_height

def resize_images(source_dir, target_dir, median_size, tolerance=0.1):
    """
    Redimensionne les images vers une taille proche de la médiane avec une tolérance.
    Les enregistre dans un répertoire cible.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    median_width, median_height = median_size
    tol_width = int(median_width * tolerance)
    tol_height = int(median_height * tolerance)

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            file_path = os.path.join(source_dir, filename)
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Vérifier si la taille est dans la plage
                if not (median_width - tol_width <= width <= median_width + tol_width and
                        median_height - tol_height <= height <= median_height + tol_height):
                    # Redimensionner vers la taille médiane
                    img_resized = img.resize((median_width, median_height), Image.ANTIALIAS)
                    save_path = os.path.join(target_dir, filename)
                    img_resized.save(save_path)
                    print(f"Resized and saved: {save_path}")
                else:
                    # Si la taille est acceptable, copier l'image
                    save_path = os.path.join(target_dir, filename)
                    img.save(save_path)
                    print(f"Copied without resizing: {save_path}")

# Répertoire des images
source_directory = "./Deep-Learning-Cpe-Project/AlgorithmePreProcess/source_images"  # Changez avec votre chemin
target_directory = "./Deep-Learning-Cpe-Project/AlgorithmePreProcess/resize_images"  # Répertoire cible

dimension_images = "./Deep-Learning-Cpe-Project/AlgorithmePreProcess/dimension_images"

# Images avec tailles définies (entraînement)
defined_images = [os.path.join(dimension_images, f) for f in os.listdir(dimension_images)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

# Calcul de la taille médiane
median_size = calculate_median_size(defined_images)

# Redimensionnement des images avec une tolérance de 10 %
resize_images(source_directory, target_directory, median_size, tolerance=0.1)