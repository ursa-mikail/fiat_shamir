#from secp256k1 import curve, scalar_mult, point_add
import random, hashlib, sys

# Secret (passphrase → scalar)
secret = sys.argv[1] if len(sys.argv) > 1 else "Hello"
x = int(hashlib.md5(secret.encode()).hexdigest(), 16) % curve.n

# Prover (Alice) commits
xG = scalar_mult(x, curve.g)
print("=== Non-Interactive Fiat–Shamir Proof (EC) ===")

# Generate random nonce and commitment
v = random.randint(1, curve.n - 1)
vG = scalar_mult(v, curve.g)

# Fiat–Shamir heuristic: challenge derived as hash of transcript
chal_data = str(curve.g) + str(xG) + str(vG)
c = int(hashlib.md5(chal_data.encode()).hexdigest(), 16) % curve.n    # 

# Response
r = (v - c * x) % curve.n

# Verifier independently reconstructs Vcheck
Vcheck = point_add(scalar_mult(r, curve.g), scalar_mult(c, xG))

print(f"xG   = {xG}")
print(f"vG   = {vG}")
print(f"r    = {r}")
print(f"c    = {c}")
print(f"Check: vG == Vcheck → {vG == Vcheck}")

"""
=== Non-Interactive Fiat–Shamir Proof (EC) ===
xG   = (109136146525607546220032307408645454120926653774236118390999877987510575231837, 102799055635747742540494351136650526442928416618537601684262987618300031910476)
vG   = (87247226759421715861100292583172861405342481033651805103337098646412910584222, 104118246656241911782843309387547027934553865429172294753697100495273588192371)
r    = 109359456758115288415930258940412025790595049479515565568110509396886874821285
c    = 64464214473628448331494940835256403267
Check: vG == Vcheck → True
"""