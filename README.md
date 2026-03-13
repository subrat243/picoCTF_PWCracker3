# PicoCTF – PW Crack 3

## Challenge Description

From picoCTF:

> Can you crack the password to get the flag?
> Download the password checker here and you'll need the encrypted flag and the hash in the same directory too.
> There are 7 potential passwords with 1 being correct. You can find these by examining the password checker script.

This challenge focuses on analyzing a Python script that verifies a password using an **MD5 hash**. The goal is to determine the correct password and decrypt the flag.

---

# Files Provided

```
level3.py
level3.flag.txt.enc
level3.hash.bin
```

* **level3.py** – Python password verification script
* **level3.flag.txt.enc** – XOR encrypted flag
* **level3.hash.bin** – MD5 hash of the correct password

---

# Initial Analysis

Opening the script reveals how the password verification works.

The program:

1. Prompts the user for a password.
2. Computes the **MD5 hash** of the password.
3. Compares the generated hash with the stored hash from `level3.hash.bin`.
4. If the hashes match, the encrypted flag is decrypted using an XOR function.

Relevant section of the script:

```python
def hash_pw(pw_str):
    pw_bytes = bytearray()
    pw_bytes.extend(pw_str.encode())
    m = hashlib.md5()
    m.update(pw_bytes)
    return m.digest()
```

Later in the script:

```python
if( user_pw_hash == correct_pw_hash ):
```

This confirms that the script simply compares MD5 hashes.

At the bottom of the file, we also find a list of possible passwords:

```python
pos_pw_list = ["8799", "d3ab", "1ea2", "acaf", "2295", "a9de", "6f3d"]
```

Since only **7 candidates exist**, the easiest approach is to test each password and see which one produces the same MD5 hash as `level3.hash.bin`.

---

# Solution Method 1 – Manual Approach

## Step 1: Inspect the Stored Hash

First, view the contents of the stored hash file.

```bash
xxd level3.hash.bin
```

or

```bash
hexdump -C level3.hash.bin
```

This shows the raw MD5 digest stored in the file.

---

## Step 2: Generate MD5 Hashes for Each Candidate

We can compute the MD5 hash of each possible password using `md5sum`.

Important: use `-n` so a newline is not included.

Example:

```bash
echo -n "8799" | md5sum
```

Repeat for each candidate password:

```bash
echo -n "8799" | md5sum
echo -n "d3ab" | md5sum
echo -n "1ea2" | md5sum
echo -n "acaf" | md5sum
echo -n "2295" | md5sum
echo -n "a9de" | md5sum
echo -n "6f3d" | md5sum
```

Compare each generated hash with the value stored in `level3.hash.bin`.

When the hashes match, the corresponding password is the correct one.

---

## Step 3: Run the Program

Run the provided script:

```bash
python3 level3.py
```

Enter the correct password when prompted:

```
Please enter correct password for flag: <password>
```

The script will decrypt `level3.flag.txt.enc` and display the flag.

---

# Solution Method 2 – Automated Approach

Instead of checking each password manually, we can automate the process using Python.

The script simply:

1. Reads the correct hash from `level3.hash.bin`
2. Generates MD5 hashes for each candidate
3. Compares them

## Automated Brute Force Script

```python
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

```

Run the script:

```bash
python3 solve.py
```

Output:

```
Password found: <correct_password>
```

Then run the original program with that password.

#Note - Change passwoerd list in script

---

# Why This Works

The challenge relies on **hash verification rather than password storage**.

The workflow is:

```
User Input Password
        ↓
Generate MD5 Hash
        ↓
Compare With Stored Hash
        ↓
If Match → Decrypt Flag
```

Since the script reveals the **list of possible passwords**, the attack becomes a simple **dictionary brute-force attack**.

---

# Key Concepts Learned

* Reverse engineering simple Python authentication scripts
* Understanding **MD5 hashing**
* Working with **binary hash files**
* Dictionary brute-force attacks
* XOR-based encryption for flag protection

---

# Conclusion

By analyzing the password verification logic in the Python script, we discovered that the password is validated using an MD5 hash. Since the script also exposes a small list of possible passwords, we can either manually hash each candidate or automate the process with a short script.

Once the correct password is identified, running the program decrypts the XOR-encrypted flag and completes the challenge.
