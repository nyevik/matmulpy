import React, { useMemo, useState } from "react";

// Helper to create a matrix with given rows/cols and a filler function
function makeMatrix(r, c, fillFn = () => 0) {
  return Array.from({ length: r }, (_, i) =>
    Array.from({ length: c }, (_, j) => fillFn(i, j))
  );
}

// Random small integers for easy mental math
function randInt(min = -5, max = 5) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

export default function MatrixMultiplyVisualizer() {
  // Dimensions: A is m x n, B is n x p
  const [m, setM] = useState(2);
  const [n, setN] = useState(2);
  const [p, setP] = useState(2);

  // Matrices
  const [A, setA] = useState(() => makeMatrix(2, 2, (i, j) => (i === j ? 1 : i === 0 && j === 1 ? 2 : 0)));
  const [B, setB] = useState(() => makeMatrix(2, 2, (i, j) => (i === 0 ? [5, 6][j] ?? 0 : [7, 8][j] ?? 0)));

  // Hovered output cell (i, j)
  const [hover, setHover] = useState({ i: null, j: null });
  // Step-through index for dot product term visualization
  const [kIndex, setKIndex] = useState(null); // null = show all terms

  // Ensure matrices sizes align when dims change
  React.useEffect(() => {
    setA((prev) => {
      const next = makeMatrix(m, n);
      for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) next[i][j] = (prev[i]?.[j] ?? 0);
      }
      return next;
    });
    setB((prev) => {
      const next = makeMatrix(n, p);
      for (let i = 0; i < n; i++) {
        for (let j = 0; j < p; j++) next[i][j] = (prev[i]?.[j] ?? 0);
      }
      return next;
    });
    setHover({ i: null, j: null });
    setKIndex(null);
  }, [m, n, p]);

  // Compute C = A * B
  const C = useMemo(() => {
    const out = makeMatrix(m, p, () => 0);
    for (let i = 0; i < m; i++) {
      for (let j = 0; j < p; j++) {
        let sum = 0;
        for (let k = 0; k < n; k++) sum += (A[i]?.[k] ?? 0) * (B[k]?.[j] ?? 0);
        out[i][j] = sum;
      }
    }
    return out;
  }, [A, B, m, n, p]);

  // UI helpers
  const numberCell = (value, onChange, isHighlighted = false) => (
    <input
      type="number"
      className={`w-16 px-2 py-1 text-right border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 ${
        isHighlighted ? "bg-yellow-100 border-yellow-400" : "border-gray-300"
      }`}
      value={value}
      onChange={(e) => onChange(parseFloat(e.target.value || "0"))}
    />
  );

  const buildGrid = (rows, cols, getCell, className = "") => (
    <div
      className={`inline-grid gap-1 ${className}`}
      style={{ gridTemplateColumns: `repeat(${cols}, minmax(4rem, auto))` }}
    >
      {Array.from({ length: rows * cols }, (_, idx) => {
        const i = Math.floor(idx / cols);
        const j = idx % cols;
        return <div key={`${i}-${j}`}>{getCell(i, j)}</div>;
      })}
    </div>
  );

  const highlightRow = hover.i;
  const highlightCol = hover.j;

  // Expression builder for the hovered C[i,j]
  const terms = useMemo(() => {
    if (highlightRow == null || highlightCol == null) return [];
    return Array.from({ length: n }, (_, k) => ({
      k,
      a: A[highlightRow][k] ?? 0,
      b: B[k][highlightCol] ?? 0,
    }));
  }, [highlightRow, highlightCol, n, A, B]);

  const highlightedValue = useMemo(() => {
    if (!terms.length) return null;
    if (kIndex == null) {
      return terms.reduce((s, t) => s + t.a * t.b, 0);
    } else {
      return terms.slice(0, kIndex + 1).reduce((s, t) => s + t.a * t.b, 0);
    }
  }, [terms, kIndex]);

  return (
    <div className="p-6 max-w-[1200px] mx-auto text-gray-900">
      <h1 className="text-2xl font-semibold mb-2">Interactive Matrix Multiplication</h1>
      <p className="text-sm mb-4">A visual guide for multiplying A (m×n) by B (n×p) to get C (m×p). Hover a cell of C to highlight the contributing row and column. Optionally step through each term of the dot product.</p>

      {/* Dimension controls */}
      <div className="flex items-center gap-4 mb-6">
        <DimPicker label="m (rows of A)" value={m} setValue={setM} />
        <DimPicker label="n (cols of A = rows of B)" value={n} setValue={setN} />
        <DimPicker label="p (cols of B)" value={p} setValue={setP} />
        <div className="flex items-center gap-2 ml-auto">
          <button
            className="px-3 py-1.5 rounded-lg border bg-white hover:bg-gray-50"
            onClick={() => {
              setA(makeMatrix(m, n, () => randInt(-5, 5)));
              setB(makeMatrix(n, p, () => randInt(-5, 5)));
              setKIndex(null);
            }}
          >Randomize</button>
          <button
            className="px-3 py-1.5 rounded-lg border bg-white hover:bg-gray-50"
            onClick={() => {
              setA(makeMatrix(m, n, () => 0));
              setB(makeMatrix(n, p, () => 0));
              setKIndex(null);
            }}
          >Clear</button>
          <button
            className="px-3 py-1.5 rounded-lg border bg-white hover:bg-gray-50"
            onClick={() => {
              // If square shapes allow identity shortcuts
              const size = Math.min(m, n);
              setA(makeMatrix(m, n, (i, j) => (i === j && j < size ? 1 : 0)));
              setB(makeMatrix(n, p, (i, j) => (i === j && j < Math.min(n, p) ? 1 : 0)));
              setKIndex(null);
            }}
          >Identity (where possible)</button>
        </div>
      </div>

      {/* Grids: A, B, C */}
      <div className="flex items-start gap-6">
        <div className="space-y-2">
          <div className="text-center font-medium">Matrix A ({m}×{n})</div>
          {buildGrid(m, n, (i, j) =>
            numberCell(A[i][j], (val) => setA((M) => {
              const copy = M.map((row) => row.slice());
              copy[i][j] = val;
              return copy;
            }), highlightRow === i)
          )}
        </div>

        <div className="text-3xl font-semibold mt-10">×</div>

        <div className="space-y-2">
          <div className="text-center font-medium">Matrix B ({n}×{p})</div>
          {buildGrid(n, p, (i, j) =>
            numberCell(B[i][j], (val) => setB((M) => {
              const copy = M.map((row) => row.slice());
              copy[i][j] = val;
              return copy;
            }), highlightCol === j)
          )}
        </div>

        <div className="text-3xl font-semibold mt-10">=</div>

        <div className="space-y-2">
          <div className="text-center font-medium">Matrix C ({m}×{p})</div>
          <div
            className="inline-grid gap-1"
            style={{ gridTemplateColumns: `repeat(${p}, minmax(4rem, auto))` }}
          >
            {Array.from({ length: m * p }, (_, idx) => {
              const i = Math.floor(idx / p);
              const j = idx % p;
              const isActive = hover.i === i && hover.j === j;
              return (
                <div key={`${i}-${j}`}>
                  <div
                    className={`w-16 px-2 py-1 text-right border rounded-md bg-gray-50 ${
                      isActive ? "ring-2 ring-indigo-500" : ""
                    }`}
                    onMouseEnter={() => {
                      setHover({ i, j });
                    }}
                    onMouseLeave={() => {
                      setHover({ i: null, j: null });
                      setKIndex(null);
                    }}
                  >
                    {C[i][j]}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Explanation panel */}
      <div className="mt-6 p-4 rounded-xl border bg-white shadow-sm">
        <h2 className="font-semibold mb-2">How a single cell of C is computed</h2>
        {highlightRow == null || highlightCol == null ? (
          <p className="text-sm text-gray-600">Hover over a cell in C to see its contributing row of A and column of B. Use the slider to step through each term of the dot product.</p>
        ) : (
          <div className="space-y-3">
            <div className="text-sm">
              <span className="font-medium">Selected:</span> C[{highlightRow + 1},{highlightCol + 1}] =
              Σ<sub>k=1…{n}</sub> A[{highlightRow + 1},k] · B[k,{highlightCol + 1}]
            </div>

            <div className="flex flex-wrap items-center gap-2 text-sm">
              {terms.map((t, idx) => {
                const active = kIndex == null || idx <= kIndex;
                return (
                  <div
                    key={idx}
                    className={`px-2 py-1 rounded-md border ${
                      active ? "bg-yellow-50 border-yellow-300" : "bg-gray-50 border-gray-200"
                    }`}
                  >
                    A[{highlightRow + 1},{t.k + 1}] · B[{t.k + 1},{highlightCol + 1}] = {t.a}·{t.b} = {t.a * t.b}
                  </div>
                );
              })}
            </div>

            <div className="flex items-center gap-3">
              <label className="text-sm text-gray-700">Step terms:</label>
              <input
                type="range"
                min={-1}
                max={n - 1}
                value={kIndex == null ? -1 : kIndex}
                onChange={(e) => {
                  const v = parseInt(e.target.value, 10);
                  setKIndex(v === -1 ? null : v);
                }}
              />
              <div className="text-sm text-gray-700">
                {kIndex == null ? `Showing all ${n} terms` : `Up to k = ${kIndex + 1}`}
              </div>
            </div>

            <div className="text-sm">
              <span className="font-medium">Partial/Total Sum:</span> {highlightedValue}
            </div>
          </div>
        )}
      </div>

      {/* Mini legend */}
      <div className="mt-4 text-xs text-gray-600">
        <p><span className="inline-block w-3 h-3 align-middle bg-yellow-200 mr-1"></span> Highlighted row/column contributes to the hovered C cell.</p>
        <p>Tip: Change dimensions (1–4). Values are editable; try randomizing for practice.</p>
      </div>
    </div>
  );
}

function DimPicker({ label, value, setValue }) {
  return (
    <label className="text-sm flex items-center gap-2">
      <span className="text-gray-700 whitespace-nowrap">{label}:</span>
      <select
        className="px-2 py-1 border rounded-md bg-white"
        value={value}
        onChange={(e) => setValue(parseInt(e.target.value, 10))}
      >
        {[1, 2, 3, 4].map((v) => (
          <option key={v} value={v}>{v}</option>
        ))}
      </select>
    </label>
  );
}
