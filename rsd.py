"""
rsd.py  —  Relational Symbolic Dynamics  (v1.0)
================================================
Core calculus: one pattern, one rule.

  Triple:       RSD(source, n, target)
  Composition:  a @ b   (source/target must share boundary)
  Identity:     RSD.identity(state)          → [X 0 X]
  Cycle:        RSD.cycle(state, n)          → [X n X]
  Chain:        RSD.chain([a, b, c, ...])    → composed triple
  Hierarchy:    RSD.enclose(outer_a, inner_chain, outer_b)

Exports
-------
  to_graph()   → dict  {nodes, edges}   (GraphML-compatible)
  to_matrix()  → dict  mapping (src,tgt) → n
  to_fol()     → str   first-order logic string
  to_graphml() → str   GraphML XML
  to_gexf()    → str   GEXF XML (Gephi-compatible)

Quick start
-----------
  from rsd import RSD, Chain

  q = RSD('psi', 1, 'psi_star')
  r = RSD('psi_star', 1, 'psi')
  cycle = q @ r                          # [psi 2 psi]

  ch = Chain([
      RSD('A_E', 'd',   'F_E'),
      RSD('F_E', 'W',   'A_L'),
      RSD('A_L', 'box', 'J'),
  ])
  print(ch.to_fol())
"""

from __future__ import annotations
import json, math, xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Any, List, Optional, Union

PHI = (1 + math.sqrt(5)) / 2          # golden ratio


# ── Core triple ──────────────────────────────────────────────────────────────

@dataclass
class RSD:
    """A single directed triple  [ source  n  target ]."""
    source: str
    n:      Any          # int, float, str (op name), or 'inf'
    target: str
    weight: complex = 1+0j   # AM/FM/PM extension: |w|=AM, arg(w)=PM
    frame:  int     = 0       # nesting depth k; effective n = n * phi^k
    inner:  Optional['Chain'] = field(default=None, repr=False)  # encapsulated chain

    # ── factories ──────────────────────────────────────────────────────────

    @classmethod
    def identity(cls, state: str, ref_scale: float = 1.0) -> 'RSD':
        """[X 0 X]  — zero-excursion identity. Cost = 1/ref_scale."""
        t = cls(state, 0, state)
        t._cost = 1.0 / ref_scale
        return t

    @classmethod
    def cycle(cls, state: str, n: Any) -> 'RSD':
        """[X n X]  — cyclic identity proven by orbit closure."""
        return cls(state, n, state)

    @classmethod
    def conservation(cls, left: str, right: str) -> 'RSD':
        """[left ≡ right]  — conservation / Gauss identity."""
        return cls(left, '≡', right)

    @classmethod
    def annihilate(cls, source: str, op: str = 'd') -> 'RSD':
        """[source op ⊥]  — Bianchi-style annihilation."""
        return cls(source, op, '⊥')

    @classmethod
    def phi_scaled(cls, source: str, n: float, target: str, frame: int) -> 'RSD':
        """[A  n@k  B]  — n scaled by phi^k."""
        return cls(source, n, target, frame=frame)

    # ── effective op count ─────────────────────────────────────────────────

    @property
    def effective_n(self) -> float:
        """n scaled by phi^frame. Returns float; 'inf' if n=='inf'."""
        if self.n == 'inf' or self.n == float('inf'):
            return float('inf')
        try:
            return float(self.n) * (PHI ** self.frame)
        except (TypeError, ValueError):
            return float('nan')   # symbolic op (e.g. 'd', 'W')

    # ── composition ───────────────────────────────────────────────────────

    def __matmul__(self, other: 'RSD') -> 'RSD':
        """
        Compose two triples by shared boundary.
        [A m B] @ [B n C] = [A m+n C]
        Raises ValueError if boundary states do not match.
        """
        if self.target != other.source:
            raise ValueError(
                f"Boundary mismatch: '{self.target}' != '{other.source}'"
            )
        # add op counts (symbolic ops concatenate with '+')
        try:
            new_n = float(self.n) + float(other.n)
            if new_n == int(new_n):
                new_n = int(new_n)
        except (TypeError, ValueError):
            new_n = f"{self.n}+{other.n}"
        new_w = self.weight * other.weight
        return RSD(self.source, new_n, other.target, weight=new_w, frame=self.frame)

    # ── encapsulation ─────────────────────────────────────────────────────

    @classmethod
    def enclose(cls, source: str, inner: 'Chain', target: str) -> 'RSD':
        """[source (inner chain) target] — hierarchical encapsulation."""
        outer_n = inner.total_n
        t = cls(source, outer_n, target)
        t.inner = inner
        return t

    # ── display ──────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        scope = f"@{self.frame}" if self.frame else ""
        inner_str = f" ({self.inner})" if self.inner else ""
        return f"[ {self.source}  {self.n}{scope}  {self.target}{inner_str} ]"

    # ── exports ──────────────────────────────────────────────────────────

    def to_fol(self) -> str:
        if self.n == '≡':
            return f"conservation({self.source}, {self.target})"
        if self.target == '⊥':
            return f"annihilates({self.source}, {self.n})"
        return f"transforms({self.source}, {self.n}, {self.target})"

    def to_dict(self) -> dict:
        return {
            'source': self.source, 'n': str(self.n), 'target': self.target,
            'weight_re': self.weight.real, 'weight_im': self.weight.imag,
            'frame': self.frame, 'effective_n': str(self.effective_n),
            'inner': self.inner.to_dict() if self.inner else None
        }


# ── Chain ────────────────────────────────────────────────────────────────────

class Chain:
    """An ordered list of RSD triples that compose sequentially."""

    def __init__(self, triples: List[RSD]):
        self.triples = list(triples)
        self._validate()

    def _validate(self):
        for i in range(len(self.triples) - 1):
            a, b = self.triples[i], self.triples[i+1]
            if a.target != b.source:
                raise ValueError(
                    f"Chain break at position {i}: "
                    f"'{a.target}' != '{b.source}'"
                )

    def compose(self) -> RSD:
        """Collapse the entire chain to a single RSD triple."""
        result = self.triples[0]
        for t in self.triples[1:]:
            result = result @ t
        return result

    @property
    def total_n(self) -> Any:
        try:
            s = sum(float(t.n) for t in self.triples)
            return int(s) if s == int(s) else s
        except (TypeError, ValueError):
            return '+'.join(str(t.n) for t in self.triples)

    @property
    def states(self) -> List[str]:
        s = [self.triples[0].source]
        for t in self.triples:
            s.append(t.target)
        return s

    def __repr__(self) -> str:
        return ' ∘ '.join(repr(t) for t in self.triples)

    def to_fol(self) -> str:
        return '\n'.join(t.to_fol() for t in self.triples)

    def to_dict(self) -> dict:
        return {'triples': [t.to_dict() for t in self.triples],
                'total_n': str(self.total_n)}

    # ── graph exports ────────────────────────────────────────────────────

    def to_graph(self) -> dict:
        """Return {nodes: [...], edges: [...]} dict."""
        nodes, edges = set(), []
        for t in self.triples:
            nodes.add(t.source)
            nodes.add(t.target)
            edges.append({
                'source': t.source, 'target': t.target,
                'n': str(t.n), 'frame': t.frame,
                'effective_n': str(t.effective_n),
                'weight_re': t.weight.real,
                'weight_im': t.weight.imag,
            })
        return {'nodes': [{'id': n} for n in sorted(nodes)], 'edges': edges}

    def to_matrix(self) -> dict:
        """Return (source, target) → n mapping."""
        return {(t.source, t.target): t.n for t in self.triples}

    def to_graphml(self) -> str:
        """GraphML XML string — import into Gephi, yEd, NetworkX."""
        root = ET.Element('graphml',
            xmlns='http://graphml.graphdrawing.org/graphml',
            attrib={'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        # attribute keys
        for kid, name, typ in [
            ('d0', 'n', 'string'), ('d1', 'frame', 'int'),
            ('d2', 'effective_n', 'double'), ('d3', 'weight_re', 'double'),
        ]:
            k = ET.SubElement(root, 'key', id=kid,
                attrib={'for': 'edge', 'attr.name': name, 'attr.type': typ})
        g = ET.SubElement(root, 'graph', id='RSD', edgedefault='directed')
        nodes = set()
        for t in self.triples:
            for s in (t.source, t.target):
                if s not in nodes:
                    ET.SubElement(g, 'node', id=s)
                    nodes.add(s)
            e = ET.SubElement(g, 'edge',
                source=t.source, target=t.target)
            for kid, val in [('d0', str(t.n)), ('d1', str(t.frame)),
                              ('d2', str(t.effective_n)), ('d3', str(t.weight.real))]:
                d = ET.SubElement(e, 'data', key=kid)
                d.text = val
        return ET.tostring(root, encoding='unicode',
                           xml_declaration=False)

    def to_gexf(self) -> str:
        """GEXF XML — Gephi native format with dynamic attributes."""
        root = ET.Element('gexf',
            xmlns='http://gexf.net/1.3',
            attrib={'xmlns:viz': 'http://gexf.net/1.3/viz', 'version': '1.3'})
        meta = ET.SubElement(root, 'meta')
        ET.SubElement(meta, 'description').text = 'RSD chain export'
        graph = ET.SubElement(root, 'graph', defaultedgetype='directed')

        attrs = ET.SubElement(graph, 'attributes',
            attrib={'class': 'edge', 'mode': 'static'})
        for aid, name, typ in [('0','n','string'), ('1','frame','integer'),
                                ('2','effective_n','float')]:
            ET.SubElement(attrs, 'attribute', id=aid, title=name, type=typ)

        nodes_el = ET.SubElement(graph, 'nodes')
        edges_el = ET.SubElement(graph, 'edges')

        seen = set()
        for idx, t in enumerate(self.triples):
            for s in (t.source, t.target):
                if s not in seen:
                    ET.SubElement(nodes_el, 'node', id=s, label=s)
                    seen.add(s)
            e = ET.SubElement(edges_el, 'edge',
                id=str(idx), source=t.source, target=t.target)
            attvals = ET.SubElement(e, 'attvalues')
            for aid, val in [('0', str(t.n)), ('1', str(t.frame)),
                              ('2', str(t.effective_n))]:
                ET.SubElement(attvals, 'attvalue', **{'for': aid, 'value': val})
        return ET.tostring(root, encoding='unicode')

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# ── PhiLadder — multi-scale chain with phi-scaling ───────────────────────────

class PhiLadder:
    """
    Build a cross-scale chain where each inter-frame link is scaled by phi^k.
    Usage:
        ladder = PhiLadder(['psi', 'N', 'T'], base_n=1)
        chain  = ladder.chain()
    """
    def __init__(self, states: List[str], base_n: float = 1.0):
        self.states  = states
        self.base_n  = base_n

    def chain(self) -> Chain:
        triples = []
        for k, (s, t) in enumerate(zip(self.states, self.states[1:])):
            n = self.base_n * (PHI ** k)
            triples.append(RSD(s, round(n, 6), t, frame=k))
        return Chain(triples)

    def total_n(self) -> float:
        return sum(self.base_n * (PHI**k) for k in range(len(self.states)-1))


# ── Convenience: Maxwell chain ───────────────────────────────────────────────

def maxwell_chain() -> Chain:
    """Return the 4-stage Maxwell emergence chain."""
    return Chain([
        RSD('A_E',  'd',   'F_E'),
        RSD('F_E',  'W',   'A_L'),
        RSD('A_L',  'box', 'J_mu'),
    ])

def maxwell_bianchi() -> RSD:
    return RSD.annihilate('F_E', 'd')

def gauss_identity() -> RSD:
    return RSD.conservation('dT_Q', 'dO_Phi')


# ── CLI / script entry point ─────────────────────────────────────────────────

if __name__ == '__main__':
    import sys, os

    print("=" * 60)
    print("RSD v1.0  —  Quick demo")
    print("=" * 60)

    # 1. Basic composition
    a = RSD('A', 3, 'B')
    b = RSD('B', 4, 'C')
    c = a @ b
    print(f"\nComposition:  {a}  @  {b}  =  {c}")

    # 2. Identity
    x0x = RSD.identity('X', ref_scale=10)
    print(f"Identity:     {x0x}  (cost={x0x._cost})")

    # 3. Cyclic orbit
    cyc = RSD.cycle('X', 5)
    print(f"Cycle:        {cyc}")

    # 4. Maxwell chain
    mch = maxwell_chain()
    print(f"\nMaxwell chain:\n  {mch}")
    print(f"  FOL:\n    " + mch.to_fol().replace('\n', '\n    '))

    # 5. Cross-scale phi ladder
    ladder = PhiLadder(['psi', 'N', 'T', 'S'])
    lch = ladder.chain()
    print(f"\nPhi ladder (psi→N→T→S):\n  {lch}")
    print(f"  total n = {ladder.total_n():.4f}")

    # 6. Export
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    gml = lch.to_graphml()
    gexf = lch.to_gexf()
    j = lch.to_json()

    with open(os.path.join(out, 'rsd_ladder.graphml'), 'w') as f: f.write(gml)
    with open(os.path.join(out, 'rsd_ladder.gexf'),    'w') as f: f.write(gexf)
    with open(os.path.join(out, 'rsd_ladder.json'),    'w') as f: f.write(j)
    print(f"\nExported: rsd_ladder.graphml / .gexf / .json  →  {out}/")
    print("=" * 60)
