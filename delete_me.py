from pathlib import Path
from vapory import Camera, LightSource, Sphere, Texture, Pigment, Finish, Scene, ImageMap

# Définir le chemin du dossier des images
image_folder = Path(__file__).parents[2].joinpath('resources/images/')
print(image_folder)
# Définition de la caméra
camera = Camera('location', [0, 0, -10], 'look_at', [0, 0, 0], 'angle', 30)

# Source de lumière
light = LightSource([10, 10, -10], 'color', [1, 1, 1])

# Rayon de la Terre
earth_radius = 1.0

# Texture pour la Terre avec image_map
earth_texture = Texture(
    Pigment(
            ImageMap(
                "tiff", f"\"{str('/resources/images/earth_color_21K.tif')}\"",
                'map_type', 1, 'interpolate', 2),
            ),
    Finish('diffuse', 0.8, 'ambient', 0, 'specular', 0.2, 'roughness', 0.05)
)

# Sphère représentant la Terre
earth = Sphere([0, 0, 0], earth_radius, earth_texture)

# Scène
scene = Scene(camera, objects=[light, earth], included=['colors.inc'])

output_folder = Path.home()

# Rendu
scene.render(str(output_folder.joinpath("earth_render.png")), width=80, height=60, tempfile='temp.pov', docker=True, resources_folder="/home/arnaud/workspace/5a/P2I_5A/P2i_POV_Ray/resources/")

print('Yey')