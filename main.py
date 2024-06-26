import struct

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]

H = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

def right_rotate(x, n):
    return (x >> n) | (x << (32 - n)) & 0xFFFFFFFF

def little_sigma_0(x):
    return right_rotate(x, 7) ^ right_rotate(x, 18) ^ (x >> 3)

def little_sigma_1(x):
    return right_rotate(x, 17) ^ right_rotate(x, 19) ^ (x >> 10)

def big_sigma_0(x):
    return right_rotate(x, 2) ^ right_rotate(x, 13) ^ right_rotate(x, 22)

def big_sigma_1(x):
    return right_rotate(x, 6) ^ right_rotate(x, 11) ^ right_rotate(x, 25)

def sha256(data):
    data = bytearray(data, 'ascii')
    original_length = len(data) * 8
    data.append(0x80)

    while len(data) % 64 != 56:
        data.append(0)

    data += struct.pack('>Q', original_length)

    def process_chunk(chunk):
        w = [0] * 64
        for i in range(16):
            w[i] = struct.unpack('>I', chunk[i * 4:i * 4 + 4])[0]

        for i in range(16, 64):
            w[i] = (little_sigma_1(w[i - 2]) + w[i - 7] + little_sigma_0(w[i - 15]) + w[i - 16]) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = H

        for i in range(64):
            t1 = (h + big_sigma_1(e) + ((e & f) ^ (~e & g)) + K[i] + w[i]) & 0xFFFFFFFF
            t2 = (big_sigma_0(a) + ((a & b) ^ (a & c) ^ (b & c))) & 0xFFFFFFFF
            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF

        H[0] = (H[0] + a) & 0xFFFFFFFF
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF

    for i in range(0, len(data), 64):
        process_chunk(data[i:i + 64])

    return ''.join(f'{value:08x}' for value in H)

# Utility functions for display
def uintArrToBinaryString(arr):
    return ''.join(f'{x:032b}' for x in arr)

def display_final_state_as_hex():
    print("\nFinal state (H) as hex = ", ' '.join(f'{x:08x}' for x in H))

def display_final_state_H_as_uint():
    print("\nFinal state (H) as uints = ", ' '.join(str(x) for x in H))

def display_final_state_H_as_bits():
    print("\nFinal state (H) as bits = ", uintArrToBinaryString(H))

# Main function to compute the hash
def main():
    s1 = (input("Enter Your Value: "))
    
    print("Sha256 result =", sha256(s1))

if __name__ == "__main__":
    main()