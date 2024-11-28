from PIL import Image
import os
import numpy as np
import random

def calculate_median_size(image_paths):
    """Calcule la médiane des tailles (largeur, hauteur) des images."""
    dimensions = []
    for path in image_paths:
        with Image.open(path) as img:
            dimensions.append(img.size)  # (width, height)
    dimensions = np.array(dimensions)
    median_width = int(np.median(dimensions[:, 0]))
    median_height = int(np.median(dimensions[:, 1]))
    return median_width, median_height

def add_random_variation(size, variation_percent=0.2):
    """
    Ajoute une variation aléatoire à une taille donnée.
    """
    factor = 1 + random.uniform(-variation_percent, variation_percent)
    return int(size * factor)

def resize_image_with_aspect_ratio(img, target_width, target_height):
    """
    Redimensionne une image en conservant le ratio d'aspect, en s'adaptant à la taille cible.
    """
    original_width, original_height = img.size
    aspect_ratio = original_width / original_height

    # Ajuster la largeur et la hauteur pour conserver le ratio
    if target_width / target_height > aspect_ratio:
        # Ajuste par la hauteur
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    else:
        # Ajuste par la largeur
        new_width = target_width
        new_height = int(new_width / aspect_ratio)

    return img.resize((new_width, new_height), Image.ANTIALIAS)

def resize_images(source_dir, target_dir, median_size, variation_percent=0.2):
    """
    Redimensionne les images en conservant leur ratio d'aspect, avec des tailles légèrement différentes.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            file_path = os.path.join(source_dir, filename)
            with Image.open(file_path) as img:
                # Ajouter une variation aléatoire aux dimensions médianes
                target_width = add_random_variation(median_size[0], variation_percent)
                target_height = add_random_variation(median_size[1], variation_percent)

                # Redimensionner en conservant le ratio d'aspect
                resized_img = resize_image_with_aspect_ratio(img, target_width, target_height)

                # Sauvegarder l'image redimensionnée
                save_path = os.path.join(target_dir, filename)
                resized_img.save(save_path)
                print(f"Resized and saved: {save_path} -> {resized_img.size}")

# Répertoires
source_directory = "./Deep-Learning-Cpe-Project/AlgorithmePreProcess/source_images"  # Changez avec votre chemin
target_directory = "./Deep-Learning-Cpe-Project/AlgorithmePreProcess/resized_images"  # Répertoire cible

dimension_images = "./Deep-Learning-Cpe-Project/AlgorithmePreProcess/dimension_images"

# Images avec tailles définies
defined_images = [os.path.join(dimension_images, f) for f in os.listdir(dimension_images)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

# Calcul de la taille médiane
median_size = calculate_median_size(defined_images)

# Redimensionnement des images avec une variation aléatoire de ±20 %
resize_images(source_directory, target_directory, median_size, variation_percent=0.2)
