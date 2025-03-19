import qrcode
from io import BytesIO
import base64


def generateQR(upi_id: str, amount: float) -> str:
    """
    Generate UPI QR Code in base64 format

    Args:
        upi_id (str): UPI ID (format: xxxxx@xxx)
        amount (float): Transaction amount (0 < amount < 100000)

    Returns:
        str: Base64 encoded PNG image
    """
    # Validation
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number")
    if amount <= 0 or amount >= 100000:
        raise ValueError("Amount must be between 1 and 99,999")
    if not isinstance(upi_id, str) or '@' not in upi_id:
        raise ValueError("Invalid UPI ID format")

    # Create UPI URL
    upi_url = f"upi://pay?pa={upi_id}&am={amount:.2f}"

    # Generate QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)

    # Convert to base64
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
