import hashlib

# Load correct hash
with open("level3.hash.bin", "rb") as f:
    correct_hash = f.read()

# Candidate passwords
pos_pw_list = ["8799", "d3ab", "1ea2", "acaf", "2295", "a9de", "6f3d"]

for pw in pos_pw_list:
    # Generate MD5 hash
    pw_hash = hashlib.md5(pw.encode()).digest()

    # Compare hashes
    if pw_hash == correct_hash:
        print(f"[+] Password Found: {pw}")
        break
    else:
        print(f"[-] Tried: {pw}")
