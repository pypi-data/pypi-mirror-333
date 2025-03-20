from werkzeug.datastructures.file_storage import FileStorage
from typing import Optional

def guardarImagen(imagen : FileStorage,nombre_archivo : str, directorio : str,*, subdirectorio : Optional[str] = '') -> str:
    from PIL import Image as Imagen
    import os 

    imagen_base : Imagen = Imagen.open(imagen)
    nombre_archivo_imagen : str = f"{nombre_archivo}.webp".encode('ascii','ignore').decode('ascii')
 
    imagen_maxi = imagen_base
    imagen_maxi.save(os.path.join(directorio,subdirectorio,f"max_{nombre_archivo_imagen}"), lossless = True, quality=30)
    
    imagen_2000px = imagen_base.copy()
    imagen_2000px.thumbnail((2000,2000))
    imagen_2000px.save(os.path.join(directorio,subdirectorio,f"2000_{nombre_archivo_imagen}"), quality= 75)

    imagen_1000px = imagen_base.copy()
    imagen_1000px.thumbnail((1000,1000))
    imagen_1000px.save(os.path.join(directorio,subdirectorio,f"1000_{nombre_archivo_imagen}"), quality= 70)
    
    imagen_750px = imagen_base.copy()
    imagen_750px.thumbnail((750,750))
    imagen_750px.save(os.path.join(directorio,subdirectorio,f"750_{nombre_archivo_imagen}"), quality= 60)

    imagen_500px = imagen_base.copy()
    imagen_500px.thumbnail((500,500))
    imagen_500px.save(os.path.join(directorio,subdirectorio,f"500_{nombre_archivo_imagen}"), quality= 50)

    imagen_200px = imagen_base.copy()
    imagen_200px.thumbnail((200,200))
    imagen_200px.save(os.path.join(directorio,subdirectorio,f"200_{nombre_archivo_imagen}"), quality= 40)
    
    imagen_100px = imagen_base.copy()
    imagen_100px.thumbnail((100,100))
    imagen_100px.save(os.path.join(directorio,subdirectorio,f"100_{nombre_archivo_imagen}"), quality=35 )

    imagen_50px = imagen_base.copy()
    imagen_50px.thumbnail((50,50))
    imagen_50px.save(os.path.join(directorio,subdirectorio,f"50_{nombre_archivo_imagen}"), quality=30 )

    return nombre_archivo_imagen
