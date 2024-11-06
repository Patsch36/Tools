import sys
from PIL import Image

def resize_image(filename, factor):
    try:
        img = Image.open(filename)
        
        width, height = img.size
        
        new_width = int(width * factor)
        new_height = int(height * factor)
        
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        base_name, ext = filename.rsplit('.', 1)
        ext = ext.lower()
        
        new_filename = f"{base_name}_resized_{factor}.{ext}"
        
        resized_img.save(new_filename)
        print(f"Bild erfolgreich skaliert und gespeichert als {new_filename}")
    
    except Exception as e:
        print(f"Fehler beim Verarbeiten des Bildes: {e}")

# if __name__ == "__main__":
if len(sys.argv) != 3:
    print("Verwendung: python script.py <Dateiname> <Faktor>")
else:
    filename = sys.argv[1]
    try:
        factor = float(sys.argv[2])
        resize_image(filename, factor)
    except ValueError:
        print("Bitte geben Sie einen gültigen Skalierungsfaktor an.")
