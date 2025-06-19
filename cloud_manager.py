import os
import sys
import io
from icloudpy import ICloudPyService
from getpass import getpass
import argparse

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


# === VERWENDUNG ===
def main():
    parser = argparse.ArgumentParser(
        description="iCloud Datei-Upload/Download Tool"
    )
    parser.add_argument(
        "--apple-id", required=True, help="Ihre Apple ID"
    )
    parser.add_argument(
        "--upload", metavar="LOCAL_PATH", help="Lokaler Pfad der Datei zum Hochladen"
    )
    parser.add_argument(
        "--upload-name", metavar="ICLOUD_FILENAME", help="Dateiname in iCloud Drive (optional, Standard: wie lokal)"
    )
    parser.add_argument(
        "--folder", required=True, help="Zielordner in iCloud Drive"
    )
    parser.add_argument(
        "--download", metavar="ICLOUD_FILENAME", help="Dateiname in iCloud Drive zum Herunterladen"
    )
    parser.add_argument(
        "--download-to", metavar="LOCAL_PATH", help="Lokaler Pfad für den Download"
    )

    args = parser.parse_args()

    apple_password = getpass("Geben Sie Ihr Apple-Passwort ein: ")

    try:
        icloud_client = ICloudUploaderDownloader(args.apple_id, apple_password)

        if args.upload:
            icloud_filename = args.upload_name if args.upload_name else os.path.basename(args.upload)
            icloud_client.upload_file(
                local_path=args.upload,
                icloud_filename=icloud_filename,
                icloud_folder=args.folder
            )

        if args.download and args.download_to:
            icloud_client.download_file(
                icloud_filename=args.download,
                icloud_folder=args.folder,
                target_local_path=args.download_to
            )
        elif args.download or args.download_to:
            print("Für den Download müssen sowohl --download als auch --download-to angegeben werden.")

        if not args.upload and not args.download:
            print("Nichts zu tun. Bitte --upload oder --download angeben.")

    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()