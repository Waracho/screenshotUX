import json
from selenium import webdriver
from PIL import Image, ImageDraw, ImageFont
import io
import time
from urllib.parse import urlparse

# Configuración inicial
url = "https://www.usm.cl"  # Cambiar a la URL de tu navegador
screenshot_path = "screenshots/"  # Carpeta donde se guardarán los pantallazos
log_file = "visited_pages.json"  # Archivo de registro en formato JSON

# Inicializar el navegador (en este caso, Chrome)
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)

# Variables para el control del tiempo y registro de páginas
start_time = time.time()  # Tiempo de inicio de la visita a la página inicial
last_url = url  # URL inicial
page_visits = []  # Lista para almacenar las visitas a las páginas
last_screenshot = None  # Inicializamos la variable para el último pantallazo

# Función para capturar y guardar el pantallazo con el nombre de la URL
def capture_screenshot(file_name):
    screenshot = driver.get_screenshot_as_png()
    with open(file_name, "wb") as f:
        f.write(screenshot)

# Función para agregar texto a la imagen
def add_text_to_image(image, text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # Puedes ajustar el tamaño y la fuente según tus necesidades
    draw.text((100, 100), text, fill="black", font=font)

# Función para escribir en el archivo JSON
def write_to_json(url, elapsed_time):
    data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "url": url,
        "elapsed_time": elapsed_time
    }
    page_visits.append(data)

    with open(log_file, "w") as f:
        json.dump(page_visits, f, indent=4)

try:
    while True:
        # Comparar la nueva URL con la anterior
        current_url = driver.current_url
        if current_url != last_url:
            # Capturar un nuevo pantallazo si hay un cambio en la URL
            parsed_url = urlparse(current_url)
            domain_name = parsed_url.netloc.replace(".", "_")  # Reemplazar puntos por guiones bajos
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_name = f"{screenshot_path}{domain_name}_{timestamp}.png"
            capture_screenshot(file_name)
            current_screenshot = Image.open(file_name)
            
            print(f"Se detectó un cambio en la URL. Guardando: {file_name}")
            text = "Cambio detectado"
            add_text_to_image(current_screenshot, text)
            current_screenshot.save(file_name)
            last_screenshot = current_screenshot
            
            # Calcular el tiempo que se estuvo en la página anterior
            elapsed_time = time.time() - start_time
            write_to_json(last_url, elapsed_time)
            
            # Actualizar las variables para la nueva página
            start_time = time.time()
            last_url = current_url
        
        else:
            pass
        
        # Esperar un breve periodo antes de revisar nuevamente la URL
        time.sleep(0.5)  # Puedes ajustar el tiempo de espera según sea necesario
        
except KeyboardInterrupt:
    print("Detención del programa por el usuario.")
finally:
    # Escribir la última página visitada al detener el programa
    if last_url != url:
        elapsed_time = time.time() - start_time
        write_to_json(last_url, elapsed_time)
    
    driver.quit()
