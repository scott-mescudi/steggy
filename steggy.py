import os
import modules.password_generator as password_generator
from colorama import Fore, Style
import modules.geotagger as geotagger
import modules.aes256 as aes256
import modules.stego as stego
import zipfile


def validate_file_path(prompt, create=False):
    while True:
        file_path = input(prompt)
        if not os.path.exists(file_path):
            if create:
                create_file = input("File does not exist. Do you want to create it? (yes/no): ").lower()
                if create_file == "yes":
                    with open(file_path, "w"):
                        pass
                    print(Fore.GREEN + f"File '{file_path}' created." + Style.RESET_ALL)
                    return file_path
                else:
                    print(Fore.RED + "Operation aborted." + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Error: File '{file_path}' not found." + Style.RESET_ALL)
        else:
            return file_path


def validate_image_path(prompt):
    while True:
        image_path = input(prompt)
        if not os.path.exists(image_path):
            print(Fore.RED + f"Error: file '{image_path}' not found." + Style.RESET_ALL)
        elif not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.wav')):
            print(Fore.RED + "Error: Invalid image format. Supported formats are PNG, JPG, JPEG, BMP, and GIF." + Style.RESET_ALL)
        else:
            return image_path


def geotag(image):
    """Print geotag information of an image."""
    try:
        latitude, longitude, datetime_obj, device = geotagger.get_geotag_info(image)
        print("Latitude:", latitude)
        print("Longitude:", longitude)
        print("Datetime:", datetime_obj)
        print("Device:", device)
    except Exception as e:
        print(Fore.RED + "An error occurred while fetching geotag information:", e + Style.RESET_ALL)


def embed(file, password, input_image, output):
    """Embed encrypted data into an image."""
    try:
        encrypted_data = aes256.encrypt_AES256(file, password)
        stego.encode_binary_image(
            image_path=input_image,
            data=encrypted_data,
            new_image_path=output
        )
        print(Fore.GREEN + "Embedding successful." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "An error occurred while embedding data:", e + Style.RESET_ALL)


def compress_directory(directory_path, zip_file_path):
    """Compress directory into a zip file."""
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory_path))


def embed_zip(directory_path, input_image_path, output_image_path, password):
    try:
        zip_file_path = "compressed_dir.zip"
        compress_directory(directory_path, zip_file_path)
        encrypted_data = aes256.encrypt_AES256(zip_file_path, password)
        stego.encode_binary_image(
            image_path=input_image_path,
            data=encrypted_data,
            new_image_path=output_image_path
        )

        print(Fore.GREEN + "Embedding successful." + Style.RESET_ALL)
        os.remove(zip_file_path)
    except:
        print(Fore.RED + "Error: An error occurred while compressing data." + Style.RESET_ALL)


def extract_zip(input_image_path, output_directory, password):
    try:
        encrypted_data = stego.decode_binary_image(input_image_path)
        decrypted_data = aes256.decrypt_AES256(encrypted_data, password)
        zip_file_path = "extracted_dir.zip"
        with open(zip_file_path, "wb") as file:
            file.write(decrypted_data)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_directory)
        os.remove(zip_file_path)
        print(Fore.GREEN + "Extraction successful." + Style.RESET_ALL)
    except:
        print(Fore.RED + "Error: An error occurred while extracting data." + Style.RESET_ALL)


def extract(password, image, output="extracted_data.txt"):
    """Extract encrypted data from an image."""
    try:
        encoded_data = stego.decode_binary_image(image)
        decrypted_data = aes256.decrypt_AES256(encoded_data, password)
        if decrypted_data:
            with open(output, "wb") as f:
                f.write(decrypted_data)
            print(Fore.GREEN + "Extraction successful." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Decryption failed." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "An error occurred while extracting data:", e + Style.RESET_ALL)

    try:
        data = aes256.decrypt_AES256(input, password)
        with open(output, "wb") as f:
            f.write(data)
    except Exception:
        print(Fore.RED + "An error occurred while decrypting data:" + Style.RESET_ALL)


def display_help():
    print(Fore.YELLOW + "Help:")
    print("1. Embed file in cover file")
    print("2. Extract file from cover file")
    print("3. Embed directory in cover file")
    print("4. Extract directory from cover file")
    print("5. Extract exif data from image")
    print("6. Generate password" + Style.RESET_ALL)
    print("exit: Close the utility")


def start():
    print(Fore.YELLOW + Style.BRIGHT + '''
    :'######::'########:'########::'######::::'######:::'##:::'##:
    '##... ##:... ##..:: ##.....::'##... ##::'##... ##::. ##:'##::
    :##:::..::::: ##:::: ##::::::: ##:::..::: ##:::..::::. ####:::
    . ######::::: ##:::: ######::: ##::'####: ##::'####:::. ##::::
    :..... ##:::: ##:::: ##...:::: ##::: ##:: ##::: ##::::: ##::::
    '##::: ##:::: ##:::: ##::::::: ##::: ##:: ##::: ##::::: ##::::
    . ######::::: ##:::: ########:. ######:::. ######:::::: ##::::
    :......::::::..:::::........:::......:::::......:::::::..:::::
    ''')
    print(Style.RESET_ALL)
    print(Fore.WHITE + Style.BRIGHT + "Available Options:")
    print("1. Embed file in cover file")
    print("2. Extract file from cover file")
    print("3. Embed directory in cover file")
    print("4. Extract directory from cover file")
    print("5. Extract exif data from image")
    print("6. Generate password" + Style.RESET_ALL)
    print("exit: Close the utility")

    option = input(Fore.WHITE + Style.BRIGHT + "\n> " + Style.RESET_ALL)

    if option == "Help":
        display_help()
        start()

    elif option == "1":
        print(Fore.CYAN + Style.BRIGHT + "Embed file in cover image" + Style.RESET_ALL)
        file = validate_file_path("Enter embed file: ", create=False)
        input_image = validate_image_path("Enter cover file: ")
        password = input("Enter password: ")
        file_name, file_ext = os.path.splitext(input_image)
        output = f"{file_name}_embed.png"
        print(f"Embedding {file} in {input_image} and saving as {output}...")
        embed(file, password, input_image, output)
        start()

    elif option == "2":
        print(Fore.CYAN + Style.BRIGHT + "Extract file from cover image" + Style.RESET_ALL)
        image = validate_image_path("Enter cover file: ")
        password = input("Enter password: ")
        output = input("Enter output file: ")
        print(f"Extracting data from {image} and saving as {output}...")
        extract(password, image, output)
        start()

    elif option == "3":
        print(Fore.CYAN + Style.BRIGHT + "Embed directory in cover image" + Style.RESET_ALL)
        directory_path = input("Enter directory: ")
        input_image = validate_image_path("Enter cover image: ")
        password = input("Enter password: ")
        file_name, file_ext = os.path.splitext(input_image)
        output_image = f"{file_name}_embed.png"
        print(f"Embedding {directory_path} in {input_image} and saving as {output_image}...")
        embed_zip(directory_path, input_image, output_image, password)
        start()

    elif option == "4":
        print(Fore.CYAN + Style.BRIGHT + "Extract directory from cover file" + Style.RESET_ALL)
        input_image = validate_image_path("Enter cover file: ")
        password = input("Enter password: ")
        output_directory = input("Enter output directory: ")
        print(f"Extracting directory from {input_image} to {output_directory}...")
        extract_zip(input_image, output_directory, password)
        start()

    elif option == "5":
        print(Fore.CYAN + Style.BRIGHT + "Extract exif data from image" + Style.RESET_ALL)
        image = validate_image_path("Enter image: ")
        print(f"Extracting geotag information from {image}...")
        geotag(image)
        start()

    elif option == "6":
        print(Fore.CYAN + Style.BRIGHT + "Generate password" + Style.RESET_ALL)
        password_generator.password_gen()

    elif option == "exit":
        print(Fore.RED + Style.BRIGHT + "Exiting..." + Style.RESET_ALL)

    else:
        print(Fore.RED + "Invalid option. Please choose a valid option." + Style.RESET_ALL)
        start()



if __name__ == "__main__":
    start()
