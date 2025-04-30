import random

def luhn_checksum(card_number):
    """Calculate the Luhn checksum of a card number."""
    digits = [int(d) for d in card_number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10

def generate_credit_card(bin_format, quantity=10):
    """Generate full credit card info including expiry and CVV."""
    cards = []

    for _ in range(quantity):
        # Generate card number base
        card_number = bin_format + ''.join(str(random.randint(0, 9)) for _ in range(15 - len(bin_format)))
        checksum = (10 - luhn_checksum(card_number)) % 10
        card_number += str(checksum)

        # Generate random month and year
        mm = f"{random.randint(1, 12):02d}"
        yy = f"{random.randint(26, 29)}"  # e.g., valid till 2026–2029
        cvv = f"{random.randint(100, 999)}"

        # Final full CC format
        cards.append(f"{card_number}|{mm}|{yy}|{cvv}")

    result = "\n".join(cards)

    if quantity > 10:
        with open("gen.txt", "w") as file:
            file.write(result)
        return "gen.txt"
    
    return result
  # Return string output for direct reply

import requests  # If using an API

def get_bin_info(bin_number):
    try:
        url = f"https://lookup.binlist.net/{bin_number}"
        response = requests.get(url, headers={"Accept-Version": "3"})
        
        if response.status_code != 200:
            return None

        data = response.json()
        return {
            "bin": bin_number,
            "bank": data.get("bank", {}).get("name", "Unknown"),
            "country": data.get("country", {}).get("name", "Unknown"),
            "country_code": data.get("country", {}).get("alpha2", "N/A"),
            "type": data.get("type", "N/A"),
            "level": data.get("brand", "N/A"),
            "brand": data.get("scheme", "N/A"),
        }
    except Exception:
        return None
