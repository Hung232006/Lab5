# LAB 05 REPORT CONTRIBUTION – MEMBER 2
**Course:** CSE703095 – Software Requirements  
**Case Study Project:** MedBook – Online Medical Appointment Booking System  
**Prepared by:** Trần Doãn Việt Anh (Member 2 – Data Flow Diagram Specialist)  
**Deliverables Covered:** Section 2 (DFD Level 2 Description) & Section 4 (DFD Extension Code)  
**Date:** 2026-10-09  

---

## 2 DFD Level 2 – "Drug Safety Warning" Process

### 2.1 Subsystem Overview & Functional Purpose
Process 5.0 (*Drug safety warning*) is an automated clinical decision-support module triggered whenever a doctor prescribes medication during an outpatient consultation (UC-07 / Process 4.0). Prescribing errors—such as administering drugs to which a patient has documented allergies or co-prescribing mutually interacting substances—pose grave clinical hazards. Process 5.0 verifies prospective prescriptions prior to clinical sign-off, notifying the attending physician of contraindications, severity levels, and adverse reactions in real time.

### 2.2 Functional Decomposition (Sub-processes 5.1 to 5.3)
To ensure high cohesion and loose coupling across clinical validation concerns, Process 5.0 is hierarchically decomposed into three focused sub-processes:

1. **Process 5.1 – Look up patient allergy list:**
   - **Trigger & Inputs:** Receives prospective prescription items and `Patient_ID` from primary data store `D3: Medical records`.
   - **Operation:** Executes queries against secondary data store `D4: Allergy List` matching the patient's recorded allergen sensitivities against active pharmaceutical ingredients in the prescribed regimen.
   - **Output:** Emits `Allergy conflict flags` (including allergen details, hypersensitivity type, and severity ranking) to Process 5.3.

2. **Process 5.2 – Look up drug interaction catalog:**
   - **Trigger & Inputs:** Receives prospective drug codes and currently active medications from primary data store `D3: Medical records`.
   - **Operation:** Computes Cartesian pairwise combinations of active substances and performs indexed queries against secondary knowledge base `D5: Interaction Catalog` to evaluate pharmacokinetic and pharmacodynamic interactions.
   - **Output:** Emits `Drug interaction conflicts` (including interaction classification, severity rating, and clinical adverse mechanism) to Process 5.3.

3. **Process 5.3 – Match & generate safety warning:**
   - **Trigger & Inputs:** Consolidates screening findings from Process 5.1 (`Allergy conflict flags`) and Process 5.2 (`Drug interaction conflicts`).
   - **Operation:** Merges risk indicators, evaluates whether risk thresholds exceed safe clinical boundaries, compiles an itemized clinical warning modal, and generates an immutable audit record.
   - **Read/Write Operations:** Performs a **Write** (append-only) operation to secondary store `D6: Warning Log` capturing the generated alerts, timestamp, doctor ID, patient ID, and prescription payload.
   - **External Output:** Dispatches the consolidated `Drug safety warning` alert directly to external entity `Doctor`.

### 2.3 Secondary Data Stores Specification
Process 5.0 encapsulates three secondary data stores that are internal to its operational boundary and abstracted away at Level 1:

| Store ID | Name | Type | Scope | Access Mode | Stored Attributes / Schema |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **D4** | Allergy List | Reference Store | Local to Subsystem 5.0 | **Read-only** (by 5.1) | `Allergy_ID`, `Patient_ID`, `Allergen_Name`, `Reaction_Type`, `Severity_Level`, `Diagnosed_Date` |
| **D5** | Interaction Catalog | Clinical Knowledge Base | Local to Subsystem 5.0 | **Read-only** (by 5.2) | `Interaction_ID`, `Drug_A_Code`, `Drug_B_Code`, `Severity_Class`, `Mechanism`, `Clinical_Recommendation` |
| **D6** | Warning Log | Audit / Event Store | Local to Subsystem 5.0 | **Append / Write** (by 5.3) | `Log_ID`, `Prescription_ID`, `Doctor_ID`, `Patient_ID`, `Timestamp`, `Warnings_Emitted`, `Override_Reason` |

### 2.4 Data-Flow Balance Verification (Level 1 vs. Level 2)
In accordance with structured systems analysis principles (Gane & Sarson / Yourdon notations), a child diagram is balanced if and only if all data flows entering and leaving the parent process at Level 1 are accounted for at Level 2, and no foreign boundary flows are introduced.

| Boundary Interface | Level 1 (Process 5.0 Boundary) | Level 2 (Sub-Processes 5.1, 5.2, 5.3 Boundary) | Balancing Status |
| :--- | :--- | :--- | :--- |
| **Incoming Flows** | `Prescription & patient history`<br>*(Source: D3: Medical records)* | 1. `Prescription & patient ID` $\rightarrow$ Process 5.1<br>2. `Prescribed drug items` $\rightarrow$ Process 5.2<br>*(Total aggregate inflow = Prescription & patient history from D3)* | **Strictly Balanced** ($\sum \text{In}_{\text{L1}} \equiv \sum \text{In}_{\text{L2}}$) |
| **Outgoing Flows** | `Drug safety warning`<br>*(Destination: Doctor)* | `Drug safety warning`<br>*(Source: Process 5.3 $\rightarrow$ Destination: Doctor)* | **Strictly Balanced** ($\sum \text{Out}_{\text{L1}} \equiv \sum \text{Out}_{\text{L2}}$) |
| **Internal Data Stores** | Not visible at Level 1 *(encapsulated)* | `D4: Allergy List` (Read by 5.1)<br>`D5: Interaction Catalog` (Read by 5.2)<br>`D6: Warning Log` (Written by 5.3) | **Strictly Balanced** *(Stores remain local within Process 5.0 boundary)* |
| **Internal Inter-process Flows** | Not visible at Level 1 *(encapsulated)* | 1. `Allergy conflict flags` (5.1 $\rightarrow$ 5.3)<br>2. `Interaction conflicts` (5.2 $\rightarrow$ 5.3) | **Strictly Balanced** *(Internal flows do not cross subsystem boundary)* |

#### Formal Balancing Equations:
$$\text{Boundary\_Inputs}(P_{5.0}) = \{ \text{Flow}(D3 \rightarrow P_{5.0}) \} = \{ \text{Flow}(D3 \rightarrow P_{5.1}) \cup \text{Flow}(D3 \rightarrow P_{5.2}) \}$$
$$\text{Boundary\_Outputs}(P_{5.0}) = \{ \text{Flow}(P_{5.0} \rightarrow \text{Doctor}) \} = \{ \text{Flow}(P_{5.3} \rightarrow \text{Doctor}) \}$$

### 2.5 Software Engineering Readiness & Handoff Justification
This Level 2 decomposition is production-ready for software architecture and engineering handoff because:
1. **Independent Microservices / Asynchronous Validation:** Sub-processes 5.1 and 5.2 operate on distinct reference stores and can be implemented as concurrent asynchronous workers, minimizing prescription submission latency.
2. **Auditability & Legal Traceability:** Explicit write access to `D6: Warning Log` guarantees compliance with medical software standards (recording whether warnings were acknowledged or overridden).
3. **Decoupled Data Governance:** Separating patient-specific health records (`D4`) from static pharmacology knowledge bases (`D5`) simplifies database indexing, caching strategies, and HIPAA/GDPR access controls.

---

## 4 Extension Code: DFD Level 2 in Code

### 4.1 Python Code Extension (`code/dataflow_model.py`)
The Python generation script was extended to define and output `dfd_level2.tikz`:

```python
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
```

### 4.2 Standalone TikZ Source Code (`code/dfd_level2.tikz`)
To render the diagram directly in LaTeX documents:

```latex
\begin{figure}[htbp]
\centering
\input{code/dfd_level2.tikz}
\caption{DFD Level 2 – Detailed Decomposition of Process 5.0 (Drug Safety Warning)}
\label{fig:dfd_level2}
\end{figure}
```
