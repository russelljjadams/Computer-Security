import urllib.parse
import sys

def custom_encode(payload):
    """
    Applies custom double URL encoding, handling '.' and '%'.
    """

    encoded_payload = ""
    for char in payload:
        if char == '.':
            encoded_char = "%252E"  # Explicitly encode '.' as %252E
        elif char == '-':
            encoded_char = '%252D'
        elif char in '%/':
            encoded_char = urllib.parse.quote_plus(char)    # Encode '%' once (it will be double-encoded later)
        else:
            encoded_char = urllib.parse.quote(char)  # Standard URL encoding for other characters
        encoded_payload += encoded_char

    # Double-encode all '%' symbols
    double_encoded_payload = ""
    for char in encoded_payload:
        if char == '%':
            double_encoded_payload += urllib.parse.quote(char) 
        else:
            double_encoded_payload += char

    return double_encoded_payload

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 encoder.py <payload>")
        sys.exit(1)

    payload = sys.argv[1]
    encoded_payload = custom_encode(payload)
    print(f"Encoded payload: {encoded_payload}")

if __name__ == "__main__":
    main()
