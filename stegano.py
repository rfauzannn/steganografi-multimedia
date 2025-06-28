import numpy as np
import cv2

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)

def encode_spread_spectrum(image_path, message):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Image not found or unreadable")

    h, w = image.shape
    flat_image = image.flatten().astype(np.float32)
    bits = text_to_bits(message)
    n_bits = len(bits)

    # Generate pseudo-random code
    np.random.seed(42)
    pn_sequence = np.random.choice([-1, 1], size=(n_bits, flat_image.shape[0]))

    # Embed message
    encoded = flat_image.copy()
    for i in range(n_bits):
        if bits[i] == '1':
            encoded += pn_sequence[i]
        else:
            encoded -= pn_sequence[i]

    encoded_image = encoded.reshape((h, w)).clip(0, 255).astype(np.uint8)
    return encoded_image

def decode_spread_spectrum(original_image_path, stego_image_path, message_length):
    original = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE).flatten().astype(np.float32)
    stego = cv2.imread(stego_image_path, cv2.IMREAD_GRAYSCALE).flatten().astype(np.float32)

    # Generate pseudo-random code
    np.random.seed(42)
    pn_sequence = np.random.choice([-1, 1], size=(message_length * 8, original.shape[0]))

    diff = stego - original
    bits = ''
    for i in range(message_length * 8):
        correlation = np.dot(diff, pn_sequence[i])
        bits += '1' if correlation > 0 else '0'

    return bits_to_text(bits)
