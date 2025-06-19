import os
import sys
import io
from icloudpy import ICloudPyService


class ICloudUploaderDownloader:
    def __init__(self, apple_id: str, password: str):
        self.apple_id = apple_id
        self.password = password
        self.api = self.authenticate()

    def authenticate(self) -> ICloudPyService:
        """Handles iCloud authentication, including optional 2FA."""
        api = ICloudPyService(self.apple_id, self.password)

        if api.requires_2fa:
            print("Zwei-Faktor-Authentifizierung erforderlich.")
            code = input("Geben Sie den 2FA-Code ein: ")
            if not api.validate_2fa_code(code):
                sys.exit("Fehler: Ungültiger 2FA-Code.")

            if not api.is_trusted_session:
                print("Vertrauensstellung wird hergestellt...")
                if not api.trust_session():
                    print("Warnung: Sitzung ist nicht vertrauenswürdig.")

        print("Erfolgreich bei iCloud angemeldet.")
        return api

    def get_or_create_folder(self, folder_path: str):
        """Navigiert zum Ordner in iCloud Drive oder erstellt ihn."""
        drive = self.api.drive
        folder = drive

        for part in folder_path.strip("/").split("/"):
            dir_list = folder.dir() or []
            if part not in dir_list:
                print(f"Ordner '{part}' wird erstellt...")
                folder.mkdir(part)

            folder = folder[part]
            if folder is None:
                sys.exit(f"Fehler: Ordner '{part}' konnte nicht erstellt werden.")

        return folder

    def upload_file(self, local_path: str, icloud_filename: str, icloud_folder: str):
        """Lädt eine lokale Datei in iCloud hoch."""
        if not os.path.exists(local_path):
            sys.exit(f"Fehler: Datei '{local_path}' wurde nicht gefunden.")

        folder = self.get_or_create_folder(icloud_folder)

        with open(local_path, 'rb') as file_in:
            mem_file = io.BytesIO(file_in.read())
            mem_file.name = icloud_filename
            folder.upload(mem_file)

        print(f"Datei '{icloud_filename}' erfolgreich nach iCloud Drive/'{icloud_folder}' hochgeladen.")

    def download_file(self, icloud_filename: str, icloud_folder: str, target_local_path: str):
        """Lädt eine Datei aus iCloud herunter und speichert sie lokal."""
        folder = self.get_or_create_folder(icloud_folder)
        
        if folder is None:
            sys.exit(f"Fehler: Ordner '{icloud_folder}' konnte nicht gefunden oder erstellt werden.")

        dir_list = folder.dir() or []
        file_node = next(
            (item for item in dir_list if item == icloud_filename),
            None
        )

        if not file_node:
            sys.exit(f"Fehler: Datei '{icloud_filename}' wurde in Ordner '{icloud_folder}' nicht gefunden.")

        print(f"Lade '{icloud_filename}' aus iCloud Drive herunter...")
        
        file = folder.get(icloud_filename)
        
        if file is None:
            sys.exit(f"Fehler: Datei '{icloud_filename}' konnte nicht abgerufen werden.")

        with open(target_local_path, 'w') as out_file:
            out_file.write(file.open().text)

        print(f"Datei '{icloud_filename}' erfolgreich nach '{target_local_path}' heruntergeladen.")





# === KONFIGURATION ===
APPLE_ID = "scheichpatrick@gmail.com"
APPLE_PASSWORD = "Juergen**3600"
LOKALER_DATEIPFAD = os.path.expanduser("~/.acronymes.txt")
ZIEL_DATEINAME = "acronyms.txt"
ZIEL_ORDNER = "botuments"
ZIEL_DOWNLOAD_PFAD = os.path.expanduser("~/Downloads/acronyms_downloaded.txt")


# === VERWENDUNG ===
if __name__ == "__main__":
    try:
        icloud_client = ICloudUploaderDownloader(APPLE_ID, APPLE_PASSWORD)

        # Upload der Datei
        icloud_client.upload_file(
            local_path=LOKALER_DATEIPFAD,
            icloud_filename=ZIEL_DATEINAME,
            icloud_folder=ZIEL_ORDNER
        )

        # Download der Datei
        icloud_client.download_file(
            icloud_filename=ZIEL_DATEINAME,
            icloud_folder=ZIEL_ORDNER,
            target_local_path=ZIEL_DOWNLOAD_PFAD
        )

    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
