#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dataflow_model.py
Lab 5 - Modeling Techniques and Diagrammatic Notations
------------------------------------------------------------
Generates:
(a) State machine diagram for the "Appointment" lifecycle.
(b) Data Flow Diagrams (DFD) at Level 0 (Context), Level 1,
    and Level 2 (Decomposition of Process 5.0: Drug safety warning).
All diagrams are generated as TikZ code to embed in LaTeX documents.

Authors: Team 00 (Member 2: Trần Doãn Việt Anh - DFD Specialist)
Run: python3 dataflow_model.py
"""
import os

OUTDIR = os.path.dirname(__file__)

STATE_MACHINE = r"""
\begin{tikzpicture}[
  state/.style={draw, rounded corners, fill=penilight, draw=peniblue,
    minimum width=3.0cm, minimum height=0.9cm, align=center, font=\small},
  >=Stealth, thick
]
\node[state] (init) at (0,0) {Pending confirmation\\(pending\_confirmation)};
\node[state] (confirmed) at (5,0) {Confirmed\\(confirmed)};
\node[state] (done) at (10,0) {Completed\\(completed)};
\node[state] (cancel) at (5,-3) {Cancelled\\(cancelled)};
\node[state] (noshow) at (10,-3) {No-show\\(no\_show)};
\node[draw, circle, fill=black, inner sep=2pt] (start) at (-2.2,0) {};

\draw[->] (start) -- (init);
\draw[->] (init) -- node[above, font=\scriptsize]{Receptionist confirms (UC-05)} (confirmed);
\draw[->] (confirmed) -- node[above, font=\scriptsize]{Doctor completes visit (UC-07)} (done);
\draw[->] (init) -- node[left, font=\scriptsize]{Patient cancels $>$2h before (UC-04)} (cancel);
\draw[->] (confirmed) -- node[right, font=\scriptsize]{Patient cancels $>$2h before (UC-04)} (cancel);
\draw[->] (confirmed) -- node[right, font=\scriptsize]{Time passed, patient did not arrive} (noshow);
\end{tikzpicture}
"""

DFD_CONTEXT = r"""
\begin{tikzpicture}[
  proc/.style={draw, circle, fill=penilight, draw=peniblue, minimum size=3.0cm, align=center, font=\small},
  ext/.style={draw, rectangle, minimum width=2.6cm, minimum height=1.0cm, align=center, font=\small},
  >=Stealth, thick
]
\node[proc] (sys) at (0,0) {0\\MedBook\\System};
\node[ext] (bn) at (-6,3) {Patient};
\node[ext] (bs) at (6,3) {Doctor};
\node[ext] (lt) at (-6,-3) {Receptionist};
\node[ext] (bh) at (6,-3) {Insurance\\partner};

\draw[->] (bn) -- node[above, sloped, font=\scriptsize]{Book/cancel request} (sys);
\draw[->] (sys) -- node[below, sloped, font=\scriptsize]{Confirmation/reminder} (bn);
\draw[->] (bs) -- node[above, sloped, font=\scriptsize]{Visit results, prescription} (sys);
\draw[->] (sys) -- node[below, sloped, font=\scriptsize]{Medical history, warnings} (bs);
\draw[->] (lt) -- node[above, sloped, font=\scriptsize]{Confirm appointment} (sys);
\draw[->] (sys) -- node[below, sloped, font=\scriptsize]{Pending-confirmation list} (lt);
\draw[->] (sys) -- node[above, sloped, font=\scriptsize]{Insurance verification request} (bh);
\draw[->] (bh) -- node[below, sloped, font=\scriptsize]{Coverage verification result} (sys);
\end{tikzpicture}
"""

DFD_LEVEL1 = r"""
\begin{tikzpicture}[
  proc/.style={draw, circle, fill=penilight, draw=peniblue, minimum size=2.1cm, align=center, font=\scriptsize},
  store/.style={draw, rectangle, minimum width=3.0cm, minimum height=0.8cm, align=center, font=\scriptsize,
    path picture={\draw (path picture bounding box.north west) -- (path picture bounding box.north east);
                  \draw (path picture bounding box.south west) -- (path picture bounding box.south east);}},
  ext/.style={draw, rectangle, minimum width=2.2cm, minimum height=0.9cm, align=center, font=\scriptsize},
  >=Stealth, thick
]
\node[ext] (bn) at (-6,2) {Patient};
\node[proc] (p1) at (-2,2) {1.0\\Search\\doctors};
\node[proc] (p2) at (2,2) {2.0\\Book\\appointment};
\node[proc] (p3) at (6,2) {3.0\\Confirm \&\\remind};
\node[proc] (p4) at (2,-2) {4.0\\Record\\visit};
\node[proc] (p5) at (6,-2) {5.0\\Drug safety\\warning};
\node[store] (d1) at (-2,-1) {D1: Doctors};
\node[store] (d2) at (2,0) {D2: Appointments};
\node[store] (d3) at (6,0) {D3: Medical records};
\node[ext] (bs) at (-2,-3.3) {Doctor};

\draw[->] (bn) -- node[above, font=\tiny]{Search criteria} (p1);
\draw[->] (p1) -- node[right, font=\tiny]{Doctor query} (d1);
\draw[->] (p1) -- node[above, font=\tiny]{Selected doctor} (p2);
\draw[->] (p2) -- node[right, font=\tiny]{Save booking} (d2);
\draw[->] (d2) -- node[right, font=\tiny]{Appt status} (p3);
\draw[->] (p3) to[out=135, in=45] node[above, font=\tiny]{Confirmation / reminder} (bn);
\draw[->] (bs) -- node[above, sloped, font=\tiny]{Diagnosis \& Rx} (p4);
\draw[->] (p4) -- node[above, sloped, font=\tiny]{Save record} (d3);
\draw[->] (d3) -- node[right, font=\tiny]{Prescription \& history} (p5);
\draw[->] (p5) to[out=-150, in=-30] node[below, sloped, font=\tiny]{Drug safety warning} (bs);
\draw[->] (p2) -- node[above, sloped, font=\tiny]{Check schedule} (d1);
\end{tikzpicture}
"""

DFD_LEVEL2 = r"""
\begin{tikzpicture}[
  proc/.style={draw, circle, fill=penilight, draw=peniblue, minimum size=2.2cm, align=center, font=\scriptsize},
  store/.style={draw, rectangle, minimum width=3.2cm, minimum height=0.8cm, align=center, font=\scriptsize,
    path picture={\draw (path picture bounding box.north west) -- (path picture bounding box.north east);
                  \draw (path picture bounding box.south west) -- (path picture bounding box.south east);}},
  ext/.style={draw, rectangle, minimum width=2.4cm, minimum height=0.9cm, align=center, font=\scriptsize},
  >=Stealth, thick
]
% --- Boundary / Interface Nodes (Level 1 Parent Context) ---
\node[store] (d3) at (-6.5, 0) {D3: Medical records\\(Level 1 Store)};
\node[ext] (bs) at (7.5, 0) {Doctor\\(External Entity)};

% --- Level 2 Sub-processes (Decomposition of Process 5.0) ---
\node[proc] (p51) at (-1.8, 2.3) {5.1\\Look up patient\\allergy list};
\node[proc] (p52) at (-1.8, -2.3) {5.2\\Look up drug\\interaction catalog};
\node[proc] (p53) at (3.0, 0) {5.3\\Match \& generate\\safety warning};

% --- Secondary Data Stores (Internal to Process 5.0) ---
\node[store] (d4) at (-1.8, 4.4) {D4: Allergy List};
\node[store] (d5) at (-1.8, -4.4) {D5: Interaction Catalog};
\node[store] (d6) at (3.0, -3.2) {D6: Warning Log};

% --- Inflows from Level 1 Boundary (D3) ---
\draw[->] (d3) to[out=40, in=180] node[above, sloped, font=\tiny]{Prescription \& patient ID} (p51);
\draw[->] (d3) to[out=-40, in=180] node[below, sloped, font=\tiny]{Prescribed drug items} (p52);

% --- Store Access Operations ---
\draw[->] (d4) -- node[right, font=\tiny]{Known allergens (Read)} (p51);
\draw[->] (d5) -- node[right, font=\tiny]{Interaction rules (Read)} (p52);
\draw[->] (p53) -- node[right, font=\tiny]{Audit entry (Write)} (d6);

% --- Internal Sub-process Data Flows ---
\draw[->] (p51) to[out=0, in=135] node[above, sloped, font=\tiny]{Allergy conflicts} (p53);
\draw[->] (p52) to[out=0, in=-135] node[below, sloped, font=\tiny]{Interaction conflicts} (p53);

% --- Outflow to Level 1 Boundary (Doctor) ---
\draw[->] (p53) -- node[above, font=\tiny]{Drug safety warning} (bs);
\end{tikzpicture}
"""


def main():
    files = {
        "state_machine_appointment.tikz": STATE_MACHINE,
        "dfd_context_level0.tikz": DFD_CONTEXT,
        "dfd_level1.tikz": DFD_LEVEL1,
        "dfd_level2.tikz": DFD_LEVEL2,
    }
    for fname, content in files.items():
        path = os.path.join(OUTDIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"[OK] Generated: {path}")


if __name__ == "__main__":
    main()
