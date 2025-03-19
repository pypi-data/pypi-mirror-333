from upi_qr import generate_upi_qr

qr_image = generate_upi_qr(
    upi_id="yourname@upi",  # Replace with valid UPI ID
    amount=150.75           # Amount between 1 and 99,999.99
)

print(qr_image)
