import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # Supprime complètement la limite

# Chemins des dossiers
dossier_images = "./dataset_part_2/train/images"  # Chemin vers le dossier contenant les images
dossier_coordonnees = "./dataset_part_2/train/labelTxt"  # Chemin vers le dossier contenant les fichiers de coordonnées
dossier_crops = "./result"  # Dossier de sortie pour les images cropées

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(dossier_crops, exist_ok=True)

# Obtenir les listes triées des fichiers dans les dossiers
fichiers_images = sorted(os.listdir(dossier_images))
fichiers_coordonnees = sorted(os.listdir(dossier_coordonnees))

# Vérifier si les deux dossiers ont le même nombre de fichiers
if len(fichiers_images) != len(fichiers_coordonnees):
    print("Le nombre de fichiers dans les deux dossiers ne correspond pas.")
    exit()

# Parcours des images et fichiers de coordonnées
for index, image_file in enumerate(fichiers_images):
    if image_file.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(dossier_images, image_file)
        coord_file = os.path.join(dossier_coordonnees, fichiers_coordonnees[index])
        
        # Charger l'image
        with Image.open(image_path) as img:
            img_width, img_height = img.size  # Taille de l'image
            # Lire les coordonnées
            with open(coord_file, "r") as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    data = line.strip().split()
                    
                    # Vérifier la validité des données
                    if len(data) < 9:
                        print(f"Coordonnées invalides dans {coord_file}, ligne {i + 1}")
                        continue

                    # Calcul des coordonnées absolues du rectangle (x_min, y_min, x_max, y_max)
                    x_min = int(round(float(data[2])))
                    y_min = int(round(float(data[1])))
                    x_max = int(round(float(data[0])))
                    y_max = int(round(float(data[5])))

                    # Découper l'image
                    cropped_img = img.crop((x_min, y_min, x_max, y_max))
                    
                    # Sauvegarder l'image cropée
                    crop_file_name = f"crop_{index + 1}_{i + 1}.jpg"
                    crop_path = os.path.join(dossier_crops, crop_file_name)
                    cropped_img.save(crop_path, "JPEG")
                    print(f"Image cropée enregistrée : {crop_path}")
                    #Nom d'origine : {image_file}
