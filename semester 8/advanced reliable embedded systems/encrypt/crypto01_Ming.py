"""
Based on this work: https://github.com/bbc/kamaelia/blob/master/Sketches/AM/xtea/xtea.py

Modified to support flexible length messages and terminal support by A. Ming.
"""

import argparse
import struct

def xtea_encrypt(key, block, n=32):
    """
        Encrypt 64-bit data block using XTEA block cipher
        * key = 128-bit (16 bytes) / block = 64-bit (8 bytes)
    """
    v0, v1 = struct.unpack("!2L", block)
    k = struct.unpack("!4L", key)
    sum, delta, mask = 0, 0x9e3779b9, 0xffffffff # mask for only using 8 bytes
    for round in range(n):
        v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum + k[sum & 3]))) & mask
        sum = (sum + delta) & mask
        v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum + k[sum >> 11 & 3]))) & mask
    return struct.pack("!2L", v0, v1)

def xtea_decrypt(key, block, n=32):
    """
        Decrypt 64-bit data block using XTEA block cipher
        * key = 128-bit (16 bytes) / block = 64-bit (8 bytes)
    """
    v0, v1 = struct.unpack("!2L", block)
    k = struct.unpack("!4L", key)
    delta, mask = 0x9e3779b9, 0xffffffff # mask for only using 8 bytes
    sum = (delta * n) & mask
    for round in range(n):
        v1 = (v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum + k[sum >> 11 & 3]))) & mask
        sum = (sum - delta) & mask
        v0 = (v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum + k[sum & 3]))) & mask
    return struct.pack("!2L", v0, v1)

def pad_block(block):
    """Pad the block to make its length a multiple of 8 bytes."""
    padding_length = 8 - (len(block) % 8)
    return block + b'\x00' * padding_length

def xtea_encrypt_arbit(key, block):
   # Pad the input block to ensure its length is a multiple of 8 bytes
   padded_block = pad_block(block)
   times = len(padded_block) // 8
   index = 0
   enc_list = []
   
   while times != 0:
      slice = padded_block[index:index+8]
      index += 8
      times -= 1
      enc_list.append(xtea_encrypt(key, slice))

   return b''.join(enc_list)

def xtea_decrypt_arbit(key, block):
   # Ensure input block is properly sized for decryption
   times = len(block) // 8
   index = 0
   dec_list = []
   
   while times != 0:
      slice = block[index:index+8]
      index += 8
      times -= 1
      dec_list.append(xtea_decrypt(key, slice))

   return b''.join(dec_list).rstrip(b'\x00')


def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files using XTEA.")
    parser.add_argument("key_file", type=str, help="Path to the key file (.txt)")
    parser.add_argument("input_file", type=str, help="Path to the input file (.txt for plaintext or .cip for encrypted text)")
    parser.add_argument("output_file", type=str, help="Path to the output file (.cip for encrypted text or .txt for decrypted text)")
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the input file")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the input file")
    
    args = parser.parse_args()

    # Ensure either encryption or decryption is specified, but not both
    if args.encrypt == args.decrypt:
        print("Error: You must specify either --encrypt or --decrypt.")
        return

    # Read the key from the key file
    with open(args.key_file, 'rb') as kf:
        key = kf.read().strip()

    # Read the input file
    with open(args.input_file, 'rb') as inf:
        data = inf.read().strip()

    if args.encrypt:
        # Encrypt the data and write to the output file
        encrypted_data = xtea_encrypt_arbit(key, data)
        with open(args.output_file, 'wb') as outf:
            outf.write(encrypted_data)
        print(f"Encrypted data written to {args.output_file}")

    elif args.decrypt:
        # Decrypt the data and write to the output file
        decrypted_data = xtea_decrypt_arbit(key, data)
        with open(args.output_file, 'wb') as outf:
            outf.write(decrypted_data)
        print(f"Decrypted data written to {args.output_file}")


if __name__ == '__main__':
    main()
