import os, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "screenshots")
k = [2,3,4,5,6,7,8,9]; nodes = [148,445,1336,4009,12028,36085,108256,324769]
plt.figure(figsize=(6.4,3.8)); plt.semilogy(k, nodes, "o-", color="#c0392b", label="measured nodes (Version 1)")
plt.semilogy(k, [3**x for x in k], "s--", color="#2c3e50", label="3^k"); plt.xlabel("free vertices k placed before K4 (m=3)")
plt.ylabel("search nodes (log scale)"); plt.title("B2: search effort grows ~3^k for same-structure graphs"); plt.grid(alpha=.3); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(OUT, "chart_b2_growth.png"), dpi=140)
m = [8,12,16,20,24,28,32,34]; ex = [113,2582,1214,62781,55730,130130,148418,1541367]; gr = [32,84,64,140,144,168,160,238]
plt.figure(figsize=(6.4,3.8)); plt.semilogy(m, ex, "o-", color="#c0392b", label="Exact: combinations tested")
plt.semilogy(m, gr, "s-", color="#27ae60", label="Greedy: evaluations"); plt.xlabel("candidate centres m"); plt.ylabel("operations (log scale)")
plt.title("B3: exact vs greedy effort"); plt.grid(alpha=.3); plt.legend(); plt.tight_layout(); plt.savefig(os.path.join(OUT, "chart_b3_effort.png"), dpi=140)
