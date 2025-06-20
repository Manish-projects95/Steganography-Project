from PIL import Image

def encode_image(img_path, message, output_path):
    """Hides a message in an image"""
    img = Image.open(img_path)
    binary_msg = ''.join([format(ord(i), "08b") for i in message])
    length = len(binary_msg)
    
    # Check if message can fit in image
    if length > img.size[0] * img.size[1] * 3:
        raise ValueError("Message too large for image")
    
    pixels = img.load()
    index = 0
    
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = list(pixels[i, j])
            
            for n in range(3):  # For each RGB component
                if index < length:
                    # Modify least significant bit
                    pixel[n] = pixel[n] & ~1 | int(binary_msg[index])
                    index += 1
            
            pixels[i, j] = tuple(pixel)
            
            if index >= length:
                img.save(output_path)
                return True
    return False

def decode_image(img_path):
    """Extracts a hidden message from an image"""
    img = Image.open(img_path)
    pixels = img.load()
    binary_msg = ""
    
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = pixels[i, j]
            
            for n in range(3):  # For each RGB component
                binary_msg += str(pixel[n] & 1)
    
    # Split into 8-bit chunks and convert to characters
    message = ""
    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i+8]
        message += chr(int(byte, 2))
        if message.endswith("\x00"):  # Null terminator
            return message[:-1]
    
    return message

# Example usage
if __name__ == "__main__":
    # Encode a message
    encode_image("original.png", "Secret message!", "encoded.png")
    
    # Decode the message
    secret = decode_image("encoded.png")
    print(f"Decoded message: {secret}")
