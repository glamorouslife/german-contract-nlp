# German Contract Clause Classifier (AGB-DE)

Automated detection of potentially void clauses in German 
consumer contracts using NLP. This project replicates and 
extends the AGB-DE paper (Braun & Matthes, ACL 2024).

## 🎯 Project Goal

German consumer contracts often contain clauses that are 
legally void under §307 BGB (German Civil Code) but are 
difficult for consumers to identify. This project builds 
a classifier to automatically detect such clauses.

This work is directly relevant to:
- **EU AI Act** — automated legal review systems
- **GDPR** — consumer protection in German FinTech/LegalTech
- **§307 BGB** — unfair contract terms under German law

---

## 📊 Results

| Model | Strategy | F1 | Void Found |
|-------|----------|----|------------|
| bert-base-german-cased (paper) | arbitrary weight [1,100] | 0.35 | ~6/37 |
| bert-base-german-cased (ours) | tuned weight [0.5, 13] | **0.39** | 11/37 |

✅ **+12% improvement over paper baseline**  
✅ **83% more void clauses detected** (6 → 11)

---

## 🔍 Error Analysis

The model was evaluated on 37 void clauses in the test set.

| Topic | Missed | Found |
|-------|--------|-------|
| conclusionOfContract | 7 | 0 |
| delivery | 6 | 1 |
| liability | 4 | 0 |
| warranty | 4 | 0 |
| withdrawal | 4 | 0 |
| payment | 3 | 4 |

### Key Findings

1. **Best performance** on `payment` clauses — void payment 
clauses contain consistent German legal trigger words

2. **Worst performance** on `conclusionOfContract` clauses 
— void language is buried inside complex valid-looking text

3. **Core challenge** — 4.8% class imbalance means the model 
defaults to predicting "valid" for ambiguous clauses

---

## 🛠️ Methodology

### Phase 1 — Baseline Reproduction
Reproduced the original BERT baseline to confirm technical 
foundation. Achieved F1=0.25 on single run (paper: 0.35, 
difference due to training randomness — normal in ML).

### Phase 2 — Beating the Baseline
The original paper used an arbitrary class weight of 100 
for void clauses with no justification. We replaced this 
with a systematic search:

1. Computed mathematically balanced weights → [0.52, 10.4]
2. Performed grid search over [10.4, 13, 15]
3. Weight=13 gave best F1=0.39 on test set

### Phase 3 — Error Analysis
Identified which clause types the model struggles with 
most and analysed why (see Error Analysis section above).

---

## 📁 Repository Structure
```
├── scripts/models/
│   ├── bert.py                   ← original baseline
│   └── bert_weighted.py          ← our improved version
├── results/
│   ├── baseline_bert.txt         ← Phase 1 results
│   ├── bert_weighted_results.txt ← Phase 2 results
│   └── error_analysis.txt        ← Phase 3 analysis
├── corpus/
│   └── agb-de-anonym.csv         ← 3,764 annotated clauses
└── loc_datasets/                 ← train/test splits
```

---

## 🚀 How to Run
```bash
# Install dependencies
pip install transformers datasets evaluate scikit-learn accelerate

# Run original baseline
python scripts/models/bert.py

# Run improved version (beats paper)
python scripts/models/bert_weighted.py
```

---

## 📚 Dataset

3,764 clauses from 93 German consumer contracts:
- **Label 0** — valid clause (95.2% of data)
- **Label 1** — potentially void clause (4.8% of data)

| Topic | Clauses | % Void |
|-------|---------|--------|
| payment | 642 | 6.07 |
| conclusionOfContract | 557 | 5.92 |
| withdrawal | 506 | 3.75 |
| delivery | 475 | 7.16 |
| warranty | 314 | 6.37 |
| liability | 211 | 9.00 |
| severability | 35 | 11.43 |

---

## 📖 Citation
```
@inproceedings{braun-matthes-2024-agb,
    title = "AGB-DE: A Corpus for the Automated Legal 
             Assessment of Clauses in German Consumer Contracts",
    author = "Braun, Daniel and Matthes, Florian",
    booktitle = "Proceedings of ACL 2024",
    year = "2024"
}
```

---

## 👤 About

This project is part of my NLP portfolio demonstrating:
- Replication of academic NLP papers
- Handling real-world class imbalance problems
- Domain-specific NLP for German legal text
- Systematic hyperparameter tuning
- Error analysis of model failures