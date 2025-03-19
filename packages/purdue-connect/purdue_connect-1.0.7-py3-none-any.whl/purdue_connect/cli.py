import argparse
from purdue_connect.connection import connect_vpn, connect_ssh
from purdue_connect.otp import get_next_otp, set_hotp_secret_from_link, set_hotp_secret_from_qr
from purdue_connect.config import load_config, save_config
from purdue_connect.hotp_activation import decode_duo_qr


def set_credentials(username, password):
    config = load_config()
    config["username"] = username
    config["password"] = password
    save_config(config)
    print("Credentials have been set successfully.")

def main():
    parser = argparse.ArgumentParser(description="Purdue Connect CLI Tool")

    # Mutually exclusive group for primary actions
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--vpn", action="store_true", help="Connect to Purdue VPN")
    group.add_argument("--ssh", metavar="SERVER", help="Connect to Purdue SSH server (e.g., ececomp.ecn.purdue.edu)")
    group.add_argument("--otp", action="store_true", help="Print a new OTP")
    group.add_argument("--set-link", metavar="LINK", help="Set HOTP secret using an activation link")
    group.add_argument("--set-qr-link", metavar="QR_URI", help="Set HOTP secret using a QR activation URI")
    group.add_argument("--set-qr-img", metavar="IMAGE_PATH", help="Set HOTP secret using a Duo QR code image")
    group.add_argument("--set-credentials", nargs=2, metavar=("USERNAME", "PASSWORD"), help="Set permanent Purdue credentials")
    
    # Optional overrides for stored credentials
    parser.add_argument("--username", help="Purdue login username (overrides stored credential)")
    parser.add_argument("--password", help="Purdue base password (overrides stored credential)")
    
    args = parser.parse_args()

    if args.set_link:
        set_hotp_secret_from_link(args.set_link)
    elif args.set_qr_link:
        set_hotp_secret_from_qr(args.set_qr_link)
    elif args.set_qr_img:
        activation_url = decode_duo_qr(args.set_qr_img)
        if activation_url.startswith("Error:"):
            print(activation_url)
        else:
            set_hotp_secret_from_link(activation_url)
    elif args.set_credentials:
        username, password = args.set_credentials
        set_credentials(username, password)
    elif args.vpn:
        connect_vpn(username=args.username, password=args.password)
    elif args.ssh:
        connect_ssh(username=args.username, password=args.password, server=args.ssh)
    elif args.otp:
        try:
            otp = get_next_otp()
            print("Your OTP is:", otp)
        except Exception as e:
            print("Error generating OTP:", e)

if __name__ == "__main__":
    main()