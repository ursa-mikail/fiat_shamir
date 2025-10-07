#from secp256k1 import curve, scalar_mult, point_add
import random, hashlib, sys

# Secret (passphrase → scalar)
secret = sys.argv[1] if len(sys.argv) > 1 else "Hello"
x = int(hashlib.md5(secret.encode()).hexdigest(), 16) % curve.n
xG = scalar_mult(x, curve.g)

print("=== Interactive Fiat–Shamir Proof (EC) ===")

# --- Step 1: Prover sends commitment ---
v = random.randint(1, curve.n - 1)
vG = scalar_mult(v, curve.g)
print(f"Alice → Bob: vG = {vG}")

# --- Step 2: Verifier issues random challenge ---
c = random.randint(1, curve.n - 1)      # 
print(f"Bob → Alice: challenge c = {c}")

# --- Step 3: Prover computes response ---
r = (v - c * x) % curve.n
print(f"Alice → Bob: response r = {r}")

# --- Step 4: Verifier checks proof ---
Vcheck = point_add(scalar_mult(r, curve.g), scalar_mult(c, xG))
print(f"Verifier computes: Vcheck = {Vcheck}")

print(f"\nCheck: vG == Vcheck → {vG == Vcheck}")

"""
=== Interactive Fiat–Shamir Proof (EC) ===
Alice → Bob: vG = (35847695394459542267720977970851067126787116502518797459034340416623140918475, 5552724347149700872584597790676774209498420542749832525712803058362895378156)
Bob → Alice: challenge c = 53923895167122559532887676275038403334913178806166097901025928856058891509595
Alice → Bob: response r = 96451692277067966985613609637827754236194030638310801524567067097407950323212
Verifier computes: Vcheck = (35847695394459542267720977970851067126787116502518797459034340416623140918475, 5552724347149700872584597790676774209498420542749832525712803058362895378156)

Check: vG == Vcheck → True
"""