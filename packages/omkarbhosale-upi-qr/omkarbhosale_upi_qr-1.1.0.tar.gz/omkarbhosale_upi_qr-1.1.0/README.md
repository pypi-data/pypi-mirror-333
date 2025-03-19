# UPI QR Generator

Python package to generate UPI payment QR codes with specified amounts.

## Installation

```bash
pip install omkarbhosale-upi-qr
```

### Usage

```python
from upi_qr import omkarbhosale_upi_qr

# Basic usage
qr_image = omkarbhosale_upi_qr(
    upi_id="omkarb@example",
    amount=500.75
)

# With error handling
try:
    qr_data = omkarbhosale_upi_qr("test@upi", 50)
    print(f"QR Code: {qr_data[:50]}...")  # Show partial output
except ValueError as e:
    print(f"Error: {e}")
```
