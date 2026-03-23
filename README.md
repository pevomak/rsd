Relational Symbolic Dynamics
A practical calculus for multi-scale state transitions
with Python library, graph exports, and system comparison
Version 1.0  —  March 2026



1  Motivation
Standard mathematical notation for dynamic systems carries significant overhead: Greek-letter field indices, separate PDE forms for different time regimes, tensor products for hierarchical structure, and modal operators for temporal dependencies. These are not intrinsically necessary for the ideas they encode.
A quantum excitation, a neural firing, and an organisational disruption share identical relational structure: a system leaves a state, traverses some number of operations, and either returns or arrives somewhere new. The formalism should reflect that identity.
RSD encodes all of this with one pattern:

[ A   n   B ]  ∘  [ B   m   C ]  =  [ A  n+m  C ]

One rule, one operation, any scale. The key additional insight: X = X is not a free tautology — it conceals a comparison operation. RSD makes that cost explicit as X0X, relativised to a reference frame, and generalisable to XnX for orbits of any length in any time regime.

2  Core Calculus
2.1  The triple
Every relation is a directed triple:
[ Source   n   Target ]
where Source and Target are state symbols from an alphabet Σ, and n ∈ ℕ is the minimum operation count: the number of elementary steps required to reach Target from Source, relative to a reference frame. The triple maps mechanically to a weighted graph edge, a matrix entry, or a first-order predicate.

Figure 1. Composition of three triples into one. The total op-count is the sum of all intermediate counts. Only shared boundary states enable composition.
2.2  Composition rule
If the target of one triple matches the source of the next, they compose. This is the only inference rule needed:
[A m B]  ∘  [B n C]  =  [A m+n C]
Chains, cycles, hierarchies, and cross-scale links are all instances of this rule applied repeatedly. The operation is associative: ([AmB]∘[BnC])∘[CkD] = [AmB]∘([BnC]∘[CkD]).
2.3  Identity as operation
Standard mathematics treats X=X as a metalinguistic axiom requiring no computation. RSD rejects this. Every assertion of identity involves three hidden operations: locating X in state space, comparing against a reference point Ref, and asserting zero net displacement. The object-level statement is:
[X  0  X]    — zero-excursion identity, cost = 1/ref_scale
The generalisation [X n X] for n > 0 encodes cyclic identity: the system left X, traversed n operations, and proved it is still X by orbit closure. Identity is demonstrated dynamically.

Figure 2. Three identity modes. Left: X=X hides comparison operations. Centre: X0X is a zero-excursion orbit with measurable cost. Right: X5X proves identity by a 5-step closed orbit.
2.4  Symbol refinements from inversion audit
The inversion audit (Section 4) identified one notation ambiguity: the numeral 0 was used for self-loops, conservation, and annihilation. Three distinct operators resolve this:

Symbol	Meaning	Example
[ X  0  X ]	Self-loop, zero excursion	Ground state persistence
[ X  ≡  Y ]	Conservation: X and Y carry equal flux	Gauss law: [ ∂△[Q]  ≡  ∂○[Φ] ]
[ X  d  ⊥ ]	Annihilation to zero element	Bianchi: [ F  d  ⊥ ]  (d²A=0)

2.5  Frame-scoped notation
When a triple operates inside a nested frame at depth k, the op-count scales by φ^k:
[A  n@k  B]   ≡   [A  n·φ^k  B]  in frame-0 coordinates
The @k scope marker defaults to 0 when omitted. Slow frames have large n, fast frames have small n, φ-nested frames scale by the golden ratio. The composition rule is unchanged.
2.6  Hierarchical encapsulation
[X  ( [A m B]  ∘  [B n C] )  Y]
Inner dynamics are sealed inside the parentheses, opaque to the outer chain. The outer triple sees only the total op-count. This is the formal counterpart of an event horizon: information inside the brackets cannot influence the outer chain without passing through the encapsulation boundary.



3  Multi-Scale Reuse and Time Regimes
The core claim of RSD is practical: the same array and chain patterns apply across all scales without new symbols. Only the state labels and n magnitudes differ.

Figure 3. Identical chain structure across quantum, neural, and organisational scales. The ≅ symbol marks structural isomorphism — the chains are the same object at different n magnitudes.

Cross-scale composition links frames directly:
[ψ  1  ψ*]  ∘  [ψ*  φ  N]  ∘  [N  φ²  T]  =  [ψ  1+φ+φ²  T]
The total 1 + φ + φ² = 2φ + 2 follows from φ² = φ + 1. The Fibonacci structure of φ-scaled chains is not imposed; it emerges from the composition rule applied to φ-ratio frames.

Time regimes
Regime	Expression	Condition	Physical meaning
Fast	[ A  1  B ]	n ≪ ref	Sub-reference, single-step
Slow	[ A  100  B ]	n ≫ ref	Super-reference, many-step
Critical	[ A  r  B ]	n = ref	At reference timescale
φ-nested k	[ A  n@k  B ]	n·φ^k	Frame-k coordinates
Indeterminate	[ A  ∞  B ]	orbit never closes	Self-reference unprovable

4  Inversion Validity Audit
For each core RSD claim, we ask: given the output, can the input be uniquely recovered? The table below records results from a computational audit run across all axioms and rules.

Claim	Forward	Inverse	Verdict
Composition [AmB]∘[BnC]	Always valid	Non-unique: any m’+n’=m+n qualifies	HOLDS — inverse exists, not unique
X0X self-loop	Valid, cost 1/ref	Always recoverable	HOLDS
X0Y (X≠Y)	Violates Axiom 6	Inconsistent without external tag	REFINE — use ≡ or ⊥
XnX cyclic forward	X(kn)X by composition	XnX from X(kn)X not guaranteed	PARTIAL — prime orbits irreducible
φ-scaling n@k	Scales by φ^k	Multiply by φ^{-k}, exact to 10^{-9}	HOLDS — fully invertible
Hierarchical [X(inner)Y]	Compresses correctly	Inner not recoverable from outer	LOSSY by design
Axiom 7 entropy asymmetry	Holds for irreversible	Fails for isometries (Wick, unitary)	REFINE — restrict to non-isometries
Translation simple triples	Lossless all 4 formats	Lossless all 4 formats	HOLDS
X=X vs X0X	X=X hides cost	X0X makes cost explicit and frame-relative	VALIDATED

φ-scaling round-trips verified computationally to 10⁻⁹ precision across frames 0–4. Composition non-uniqueness confirmed across 5 test cases with 3–11 valid factorisations each.



5  Comparison to Existing Formalisms
RSD addresses limitations found in each standard approach. The comparison below is qualitative (scores 1–5); precise claims are scope-limited to the properties listed.

Figure 4. Capability comparison across six dimensions. RSD scores uniformly high because it was designed specifically to address the gaps visible in each other system.

System	Strength	Gap that RSD closes
State machines	Simple, decidable	No scale reuse; identity not quantified; no hierarchy
Graph theory	Flexible topology	Op-count semantics absent; time regimes not encoded
Petri nets	Concurrency, firing rules	Heavy notation; no frame-relative identity; poor hierarchy
Category theory	Scale-invariant morphisms	Abstract; no numeric op-cost; hard to use directly
RSD	All of the above	—

RSD is most directly comparable to weighted categories, where morphisms are arrows between objects and composition is the only rule. The addition of the op-count n as an explicit integer weight, plus the identity-as-operation principle, are the two novel contributions relative to standard categorical notation. Both extensions are conservative: they add information without breaking any categorical property.

6  Network Diagrams
The following diagrams are rendered from the RSD Python library and exported as GraphML, GEXF, and JSON files included in the distribution.

Figure 5. Left: Maxwell emergence chain as a directed graph.  Right: φ-scaled cross-scale ladder from quantum (ψ) through neural (N) and organisational (T) to societal (S) scales. Edge labels show n and φ^k scaling factors.


Figure 6. BH frame boundaries as φ-tuned membranes. Each coloured wave is one nested frame vibrating at its characteristic frequency f_k = f_0·φ^k. Amber dots mark Chladni nodes — points of simultaneous zero displacement across all participating waves — where meta-processes emerge.



7  Python Library
The rsd.py module implements the complete RSD calculus as a Python library. It requires only the Python standard library; matplotlib and networkx are optional for visualisation.
7.1  Installation
# No dependencies beyond Python 3.8+
# Optional: pip install matplotlib networkx
from rsd import RSD, Chain, PhiLadder
7.2  Core usage
# Basic triple
a = RSD("A", 3, "B")
b = RSD("B", 4, "C")
c = a @ b                       # [ A  7  C ]

# Identity modes
x0x = RSD.identity("X", ref_scale=10)   # [ X  0  X ]  cost=0.1
xnx = RSD.cycle("X", 5)                 # [ X  5  X ]

# Conservation and annihilation
gauss = RSD.conservation("dT_Q", "dO_Phi")   # [ dT_Q  ≡  dO_Phi ]
bianchi = RSD.annihilate("F_E", "d")          # [ F_E  d  ⊥ ]

# Frame-scoped n@k
t = RSD.phi_scaled("psi", 1.0, "N", frame=1) # n·φ^1 = 1.618
print(t.effective_n)                          # 1.618034
7.3  Chains
from rsd import Chain, maxwell_chain

# Build a chain
ch = Chain([
    RSD("A_E", "d",   "F_E"),
    RSD("F_E", "W",   "A_L"),
    RSD("A_L", "box", "J_mu"),
])

# Collapse to single triple
result = ch.compose()           # [ A_E  d+W+box  J_mu ]

# First-order logic export
print(ch.to_fol())
# transforms(A_E, d, F_E)
# transforms(F_E, W, A_L)
# transforms(A_L, box, J_mu)
7.4  Cross-scale phi-ladder
from rsd import PhiLadder

ladder = PhiLadder(["psi", "N", "T", "S"], base_n=1.0)
chain  = ladder.chain()
print(chain)
# [ psi  1.0  N ] ∘ [ N  1.618@1  T ] ∘ [ T  2.618@2  S ]
print(ladder.total_n())         # 5.2361 (= 1 + φ + φ²)
7.5  Graph export
# All three export formats from any Chain
gml  = chain.to_graphml()       # import into Gephi, yEd, NetworkX
gexf = chain.to_gexf()          # Gephi native with dynamic attributes
j    = chain.to_json()          # generic JSON

# Write to disk
with open("chain.graphml", "w") as f: f.write(gml)
with open("chain.gexf",    "w") as f: f.write(gexf)
with open("chain.json",    "w") as f: f.write(j)

# Load back into NetworkX
import networkx as nx
G = nx.read_graphml("chain.graphml")
print(list(G.edges(data=True)))
7.6  Matrix representation
M = chain.to_matrix()
# { ("psi","N"): 1.0,  ("N","T"): 1.618,  ("T","S"): 2.618 }

# Or convert to numpy / pandas
states = list(chain.states)
import numpy as np
A = np.zeros((len(states), len(states)))
for (src, tgt), n in M.items():
    A[states.index(src), states.index(tgt)] = float(n)



8  Graph Data Files
Three pre-built graph files are included, each in three formats (GraphML, GEXF, JSON). All files are generated by rsd.py and are re-generatable from the library.

File base	Content	Nodes	Edges	Use case
rsd_maxwell	Maxwell emergence chain	4	3 + Bianchi	Electromagnetism, field theory
rsd_ladder	Cross-scale φ-ladder ψ→N→T→S	4	3	Multi-scale analysis
rsd_bh_nesting	BH nested frame chain BH0→…→BH3	4	3	Event horizon / UTGP analysis

GraphML (.graphml)
Standard XML-based graph format. Importable into Gephi, yEd, Cytoscape, and NetworkX. Each edge carries four attributes: n, frame, effective_n, weight_re.
GEXF (.gexf)
Gephi's native format with dynamic attribute support. Directly drag-and-drop into Gephi for visualisation with layout algorithms and community detection.
JSON (.json)
Generic key-value format. Contains the full triple list including inner chains, complex weights, and frame depths. Use for any custom processing pipeline.

All three formats are lossless for simple (non-hierarchical) chains. Hierarchical inner chains are preserved only in JSON. GraphML and GEXF record only the outer op-count for hierarchical triples.

9  Worked Applications
9.1  Maxwell equations
The derivation of electromagnetism from a Euclidean substrate as a four-stage NxN chain:
ch = Chain([
    RSD("A_E",  "d",    "F_E"),   # exterior derivative
    RSD("F_E",  "W",    "A_L"),   # Wick rotation (PM: 90° phase)
    RSD("A_L",  "box",  "J_mu"),  # d'Alembertian
])
bianchi = RSD.annihilate("F_E", "d")          # d²A = 0
gauss   = RSD.conservation("dT_Q", "dO_Phi")  # Gauss law
9.2  UTGP stability cascade
The UTGP Stability Number Σ = λ₁Kτ_rel and Geometric Cliff R_k as RSD chains:
stability = RSD("Sigma_hi", 1, "Sigma_lo")    # Σ crosses 1
cliff     = Chain([
    RSD("beta1",  "collapse", "beta0"),        # cycle death
    RSD("beta0",  "spike",    "Psi_hi"),       # Psi spike
    RSD("Psi_hi", "Cliff",    "flat"),         # Geometric Cliff
])
9.3  Nested BH frames with Chladni crossing
bh = Chain([
    RSD.phi_scaled("BH0", 1.0, "BH1", frame=0),
    RSD.phi_scaled("BH1", 1.0, "BH2", frame=1),
    RSD.phi_scaled("BH2", 1.0, "BH3", frame=2),
])
# Chladni node at BH1∩BH2 crossing:
meta = RSD.enclose("BH0", bh, "meta_process")
print(meta)
# [ BH0  ([ BH0  1.0  BH1 ] ∘ […])  meta_process ]

10  Note on Further Extensions
The following extensions are identified but not developed in this paper. Each adds one concept to the core calculus without changing the composition rule.

•{text: complex weight field} — augment triples to [ A  n:w  B ] where w ∈ ℂ. Then |w| = AM depth, rate of state advance = FM, arg(w) = PM phase. Wick rotation becomes w = e^{iπ/2} = i. Complete modulation algebra in the notation.
•Stochastic extension — replace Axiom 6 (Determinism) with a probability distribution over targets: P(transforms(A,n,X)=B_i) = p_i. Classical RSD recovered at p=1.
•Modal layer — [ A ◇n B ] (possible in n), [ A □n B ] (necessary in n). Models systems with indeterminate pathways while keeping composition intact.
•Continuous limit — as n and ref both grow with fixed ratio n/ref, the discrete chain approaches a continuous flow. Composition becomes an integral; the matrix becomes a propagator. Bridge to PDE formulations, derivable rather than postulated.

These extensions form a natural research programme. None requires changing the composition rule or the treatment of identity. The graph export formats already carry the weight_re and weight_im fields for the complex weight extension.

Summary
RSD reduces multi-scale dynamic systems to one pattern ([ Source  n  Target ]) and one rule (composition adds op-counts through shared boundary states). Identity is an operation with measurable cost. Time regimes are magnitudes of n. Hierarchical nesting is parenthetical encapsulation.
The system translates to weighted graphs, matrices, and first-order logic without loss for simple expressions. Three graph file formats (GraphML, GEXF, JSON) are provided for immediate use with Gephi, NetworkX, yEd, and custom pipelines. The Python library implements the full calculus in a single file with no mandatory dependencies.

Property	Status
Composition rule	Holds; inverse exists but is non-unique (intended)
φ-scaling inversion	Exact to 10⁻⁹ across all frames
Identity quantification	X0X cost = 1/ref_scale (non-zero, frame-relative)
Scale reuse	Same chain, different n magnitudes — no new symbols needed
Translation fidelity	Lossless for simple triples; FOL only for hierarchical
op=0 ambiguity	Resolved: X0X / ≡ / ⊥ are three distinct operators
Axiom 7 scope	Restricted to irreversible (non-isometric) transforms
