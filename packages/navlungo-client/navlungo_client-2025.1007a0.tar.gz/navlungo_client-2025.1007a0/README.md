# Navlungo Domestic API Client

A quick and dirty API client for the Navlungo Domestic API.

## Usage

```python
from navlungo_client.client import NavlungoClient
from navlungo_client.models import CreatePostRequest, Address, PostDetails, PostItem, CreateTokenRequest, SenderAddress, CreateAddressRequest, GetBarcodeRequest, CarrierId, BarcodeType

# Replace with your actual credentials

USERNAME = "__USERNAME__"  # Replace with your username
PASSWORD = "__PASSWORD__"  # Replace with your password

def main():
    client = NavlungoClient(base_url=NavlungoClient.PROD_BASE_URL)

    # 1. Create Token
    try:
        token_data = {"username": USERNAME, "password": PASSWORD}
        token_response = client.create_token(data=token_data)
        print("Token created successfully:", token_response)
    except Exception as e:
        print(f"Error creating token: {e}")
        return

    # 2. Create Post
    try:
        sender_address = SenderAddress(
            addressId="2526"
        )

        recipient_address = Address(
            name="Carrtell",
            phone="0532 123 45 67",
            email="carrtell@test.com",
            address="Zümrütevler, Ural Sk. No:38, 34852",
            country="tr",
            city="İstanbul",
            district="Maltepe"
        )

        post_details = PostDetails(
            desi=2,
            package_count=1
        )

        post_item = PostItem(
            reference_id="REF123",
            carrier_id=CarrierId.SURAT_KARGO,
            post_type=2,
            sender=sender_address,
            recipient=recipient_address,
            post=post_details,
            barcode_format="pdf-A5"
        )

        post_data = {
            "platform": "Integration Company",
            "posts": [post_item.model_dump()]
        }

        post_response = client.create_post(data=post_data)
        print("Post created successfully:", post_response)

    except Exception as e:
        print(f"Error creating post: {e}")

    # 3. Create Address
    try:
        address_data = {
            "address_type": "recipient",
            "address_name": "John Doe",
            "address_phone": "+90531234567",
            "address_line": "Deneme Mahallesi Ural Sokak No:999",
            "address_country": "tr",
            "address_city": "İstanbul",
            "address_district": "Kadıköy"
        }
        address_response = client.create_address(data=address_data)
        print("Address created successfully:", address_response)
    except Exception as e:
        print(f"Error creating address: {e}")

    # 4. Get All Carriers
    try:
        carriers_response = client.get_all_carriers()
        print("Carriers retrieved successfully:", carriers_response)
    except Exception as e:
        print(f"Error getting carriers: {e}")

    # 5. Get Barcode
    try:
        barcode_data = {
            "post_number": "XXX123",
            "barcode_type": BarcodeType.PDF
        }
        barcode_response = client.get_barcode(data=barcode_data)
        print("Barcode retrieved successfully:", barcode_response)
    except Exception as e:
        print(f"Error getting barcode: {e}")

if __name__ == "__main__":
    main()