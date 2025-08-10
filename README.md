# Benchmarking Large Language Models on Multiple Tasks in Bioinformatics NLP with Prompting

> **Paper:** [arXiv:2503.04013](https://arxiv.org/abs/2503.04013)
> **Authors:** Anonymous ACL Submission (at the time of summary)
> **Summary:** This paper introduces **Bio-benchmark**, a comprehensive framework for evaluating Large Language Models (LLMs) on 30 bioinformatics tasks without fine-tuning. It also presents **BioFinder**, a novel tool for accurately extracting answers from LLM responses, significantly outperforming existing methods. The study benchmarks six leading LLMs, revealing their intrinsic capabilities and limitations across diverse biological domains.

---

<!-- Placeholder for Figure 1 -->
*<p align="center">Figure 1 from the paper would be placed here, showing an overview of the Bio-benchmark framework.</p>*

## 📄 Abstract

Large Language Models (LLMs) are increasingly vital tools for solving biological problems, but existing benchmarks are often inadequate for evaluating their performance across diverse tasks. This paper introduces **Bio-benchmark**, a comprehensive, prompting-based framework covering 30 key tasks in proteins, RNA, drugs, electronic health records (EHR), and traditional Chinese medicine (TCM). Using this benchmark, the authors evaluate six mainstream LLMs (including GPT-4o and Llama-3.1-70b) in **0-shot and few-shot Chain-of-Thought (CoT) settings** to assess their intrinsic capabilities without fine-tuning. To enhance evaluation efficiency, the paper proposes **BioFinder**, a new tool that increases answer extraction accuracy by over 40% compared to existing methods. The results identify which biological tasks are well-suited for current LLMs, highlight areas needing improvement, and inform recommendations for developing more robust, specialized LLMs for bioinformatics.

---

## 🔑 Key Contributions

This work makes three primary contributions to the field:

1.  **A Comprehensive Bioinformatics Benchmark (Bio-benchmark):**
    *   A new benchmark consisting of **30 important tasks** across seven domains: Protein, RNA, RNA-Binding Protein (RBP), Drug, Electronic Health Record (EHR), Medical QA, and Traditional Chinese Medicine (TCM).
    *   It tests six mainstream LLMs to evaluate their performance in **zero-shot and few-shot (with CoT)** settings, revealing their inherent, pre-trained knowledge.

2.  **A Novel Answer Extraction Tool (BioFinder):**
    *   An answer extraction tool specifically designed for bioinformatics tasks.
    *   It accurately extracts answers from unstructured LLM responses, achieving **over 40% higher accuracy** than existing methods like RegEx.

3.  **In-depth Analysis and Recommendations:**
    *   A thorough evaluation of LLM performance, identifying which tasks are currently well-suited for LLMs (e.g., medical QA, drug design) and which are challenging (e.g., RNA structure prediction, drug-drug interaction).
    *   Proposes prompt-based strategies to enhance performance and provides architectural recommendations for future biological LLM development.

---

## 🔬 The Bio-benchmark Framework

Bio-benchmark is meticulously constructed from various high-quality sources, ensuring data diversity and relevance. The tasks are divided into two main categories: **Biological Sequence Data** and **Biomedical Textual Data**.

### Biological Sequence Tasks
*   **Protein (4 subtasks):**
    *   `Protein Family Sequence Design`: Generate sequences for a given Pfam ID.
    *   `Protein Species Prediction`: Classify the species of a protein from its sequence.
    *   `Protein Inverse-Folding`: Design a protein sequence from its secondary structure.
    *   `Protein Structure Prediction`: Predict the secondary structure from a sequence.
*   **RNA (5 subtasks):**
    *   `RNA Family Sequence Design`: Generate sequences for a given Rfam ID.
    *   `RNA Function Prediction`: Predict function from an RNA sequence.
    *   `RNA Inverse-Folding`: Design an RNA sequence from its dot-bracket structure.
    *   `RNA Structure Prediction`: Predict the secondary structure from a sequence.
    *   `sgRNA Efficiency Prediction`: Predict the gene-editing efficiency of a given sgRNA.
*   **RNA-Binding Protein (RBP) (1 subtask):**
    *   `RNA-Protein Interaction`: Predict if an RNA sequence binds to a specific protein.
*   **Drug (3 subtasks):**
    *   `Drug Design`: Predict the efficacy of a molecule (SMILES string) against bacteria.
    *   `Drug-Drug Interaction`: Predict one of 86 types of interactions between two drugs.
    *   `Drug-Target Interaction`: Predict the binding affinity between a drug and a target.

### Biomedical Textual Tasks
*   **Electronic Health Record (EHR) (3 subtasks):**
    *   `Disease Diagnosis`: Predict diagnostic outcomes from patient data.
    *   `Treatment Planning`: Analyze patient data to devise treatment plans.
    *   `Medical Report Generation`: Generate reports from doctor-patient dialogues.
*   **General Medical QA (Multiple subtasks):**
    *   Utilizes expert-verified exam questions from diverse sources like **MedQA** (USA, China, Taiwan), **MedMCQA** (India), and **HeadQA** (Spain).
*   **Traditional Chinese Medicine (TCM) QA (Multiple subtasks):**
    *   Employs high-quality datasets like **CMB/CMMLU** and **TCM SD** to test understanding of classical texts and real clinical cases.

---

## ⚙️ Methodology

### Evaluation Pipeline
The study uses a prompting-based approach to evaluate LLMs without any task-specific fine-tuning.

1.  **Prompting:** Questions are presented to the LLMs using two strategies:
    *   **0-shot:** The model receives only the question and instructions.
    *   **Few-shot with Chain-of-Thought (CoT):** The model is given a few examples (e.g., 5-shot) of question-answer pairs with reasoning steps before being asked the target question.
2.  **Answer Extraction with BioFinder:** Since LLMs produce free-form text, the custom-built **BioFinder** tool is used to accurately extract the final answer (e.g., a specific sequence, a multiple-choice option, or a "true/false" value) from the generated text.
3.  **Evaluation:**
    *   **Objective Tasks:** Answers are compared against a ground truth using metrics like Accuracy, Recovery Rate, and Bit Score.
    *   **Subjective Tasks:** Long-text answers are evaluated using a fine-grained framework assessing **Comprehensiveness**, **Hallucination Rate**, **Omission Rate**, and **Consistency**.

### BioFinder: The Answer Extraction Tool
A key innovation of this work is **BioFinder**, an LLM-based tool fine-tuned from `xFinder-llama3-8b`. It is designed to overcome the limitations of regular expressions and general-purpose LLMs for extracting answers in bioinformatics contexts.

| Task Type | RegEx (OpenCompass) | GPT-4o (as extractor) | **BioFinder (Proposed)** |
| :--- | :---: | :---: | :---: |
| Sequence Extraction | 68.0% | 38.5% | **93.5%** |
| **Overall Objective Tasks** | 72.1% | 62.9% | **94.7%** |
| Natural Language Inference (NLI) | - | 59.9% | **89.8%** |

*Table 1 from the paper shows BioFinder's superior performance in both answer extraction and NLI tasks.*

---

## 📊 Key Findings and Analysis

### General Observations
*   **Prompt Formatting is Crucial:** The way biological sequences are formatted significantly impacts performance. Separating characters with **newline characters** yielded over **3x higher alignment accuracy** compared to continuous strings, as this helps the BPE tokenizer process individual elements correctly.
*   **Few-shot vs. 0-shot:**
    *   Few-shot prompting provides a major boost for tasks where LLMs have less pre-trained knowledge (e.g., **TCM, Protein Species Prediction**).
    *   For tasks where LLMs are already strong (e.g., **General Medical QA**), few-shot prompting offers minimal or even negative impact.

### Performance by Domain
*   **Protein & RNA:**
    *   **Prediction is easier than generation:** Predicting a structure from a sequence (e.g., Protein Structure Prediction) is significantly more successful than generating a sequence from a structure (Inverse-Folding).
    *   **Llama-3.1-70b** and **Mistral-large-2** show strong performance in species/function prediction with few-shot prompts.
    *   Generating sequences from family IDs (Pfam/Rfam) is impossible in a 0-shot setting but becomes feasible with 10-shot examples.
*   **Drug Design:**
    *   LLMs perform exceptionally well in predicting a drug's efficacy, with most models achieving **>80% accuracy** in a 5-shot setting.
    *   Predicting **Drug-Target interactions** is moderately successful (~70% accuracy).
    *   Predicting **Drug-Drug interactions** is a major weakness, with performance being "unsatisfactory" across all models.
*   **EHR and Medical QA:**
    *   This is a **strong area for LLMs**. They achieve high accuracy on diagnostic tasks and multiple-choice questions, often performing well even in a 0-shot setting.
    *   **GPT-4o** consistently performs at the top for these text-based reasoning tasks.
*   **Traditional Chinese Medicine (TCM):**
    *   0-shot performance is modest, but **few-shot prompting leads to significant improvement** (e.g., TCMSD accuracy jumps from 31.7% to 65.3%). This suggests that providing in-context examples is highly effective for specialized domains.

---

## ⚠️ Limitations

The authors acknowledge several limitations:
*   **No Fine-Tuning:** The study only evaluates the intrinsic capabilities of LLMs. Fine-tuning would likely improve performance on specific tasks.
*   **Benchmark Scope:** While comprehensive, the 30 tasks cannot cover all bioinformatics challenges, which may affect the generalizability of the findings.
*   **BioFinder's Dependency:** The accuracy of BioFinder, though high, can be compromised if LLM outputs are overly ambiguous or complex.
*   **Computational Costs:** The resource-intensive nature of using LLMs is not addressed, which could be a barrier for researchers with limited resources.

---

## ©️ Citation

```bibtex
@misc{anonymous2025benchmarking,
      title={Benchmarking Large Language Models on Multiple Tasks in Bioinformatics NLP with Prompting}, 
      author={Anonymous},
      year={2025},
      eprint={2503.04013},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
