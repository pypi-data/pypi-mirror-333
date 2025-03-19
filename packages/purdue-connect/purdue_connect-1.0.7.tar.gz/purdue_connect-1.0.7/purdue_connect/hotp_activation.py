import base64
from urllib.parse import urlparse, unquote
import requests
from Crypto.PublicKey import RSA
import cv2

def decode_duo_qr(image_path):
    """
    Scans a Duo QR code image and extracts the activation URL using OpenCV's QRCodeDetector.
    
    :param image_path: Path to the QR code image file.
    :return: Extracted Duo activation link or an error message.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Unable to load image. Check the file path."
    
    # Use OpenCV's QRCodeDetector
    detector = cv2.QRCodeDetector()
    qr_data, points, _ = detector.detectAndDecode(image)
    
    if not qr_data:
        return "Error: No QR code detected in the image."
    
    # Split activation key and Base64 hostname
    if '-' not in qr_data:
        return "Error: Unexpected QR code format."
    
    activation_key, base64_host = qr_data.split('-', 1)
    
    # Decode Base64 Duo API host
    try:
        padding_needed = len(base64_host) % 4
        if padding_needed:
            base64_host += "=" * (4 - padding_needed)
        duo_host = base64.b64decode(base64_host).decode('utf-8')
    except Exception as e:
        return f"Error: Base64 decoding failed ({str(e)})."
    
    # Construct the activation URL
    activation_url = f"https://{duo_host}/activate/{activation_key}"
    return activation_url

def qr_url_to_activation_url(qr_url):
    """
    Convert a Duo QR activation URL to a standard activation URL.
    Extracts the activation code and Base64-encoded hostname and returns a formatted URL.
    """
    # Extract the URL parameter value after ?value=
    data = unquote(qr_url.split("?value=")[1])
    # The first part is the activation code (remove the 'duo://' prefix)
    code = data.split("-")[0].replace("duo://", "")
    # The second part is the hostname in base64
    hostb64 = data.split("-")[1]
    # Decode the hostname (add padding if needed)
    host = base64.b64decode(hostb64 + "=" * (-len(hostb64) % 4))
    activation_url = f"https://{host.decode('utf-8')}/push/v2/activation/{code}"
    print(activation_url)
    return activation_url

def get_secret(activation_uri):
    """
    Extracts the HOTP secret from an activation URI.
    If the URI is a QR activation URL (contains "frame/qr"), it is converted to a standard activation URL first.
    Returns the HOTP secret as a Base32-encoded string.
    """
    if "frame/qr" in activation_uri:
        activation_uri = qr_url_to_activation_url(activation_uri)
    parsed = urlparse(activation_uri)
    subdomain = parsed.netloc.split(".")[0]
    host_id = subdomain.split("-")[-1]
    # Remove any trailing slash so that slug is correctly extracted.
    slug = parsed.path.rstrip("/").split("/")[-1]

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": f"api-{host_id}.duosecurity.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.0.0",
    }
    params = {"customer_protocol": "1"}
    data = {
        "touchid_status": "not_supported",
        "jailbroken": False,
        "architecture": "arch64",
        "region": "US",
        "app_id": "com.duosecurity.duomobile",
        "full_disk_encryption": True,
        "passcode_status": True,
        "platform": "Android",
        "pkpush": "rsa-sha512",
        "pubkey": RSA.generate(2048).publickey().export_key().decode(),
        "app_version": "3.28.1",
        "app_build_number": 328104,
        "version": "9.0.0",
        "manufacturer": "Samsung",
        "language": "en",
        "model": "Samsung Smart Fridge",
        "security_patch_level": "2019-07-05",
    }

    address = f"https://{parsed.netloc}/push/v2/activation/{slug}"
    response = requests.post(address, headers=headers, params=params, data=data)
    response.raise_for_status()
    hotp_secret = response.json()["response"]["hotp_secret"]
    # Convert the raw secret (likely hexadecimal or another format) to Base32.
    # This ensures the secret works with pyotp.
    encoded_secret = base64.b32encode(hotp_secret.encode()).decode()
    return encoded_secret