# Benchmarking Large Language Models on Multiple Tasks in Bioinformatics NLP with Prompting

> **Paper:** [arXiv:2503.04013]
> **Authors:** Anonymous ACL Submission (at the time of summary)
> **Summary:** This paper introduces **Bio-benchmark**, a comprehensive framework for evaluating Large Language Models (LLMs) on 30 bioinformatics tasks without fine-tuning. It also presents **BioFinder**, a novel tool for accurately extracting answers from LLM responses, significantly outperforming existing methods. The study benchmarks six leading LLMs, revealing their intrinsic capabilities and limitations across diverse biological domains.

---

<p align="center">
  <img src="figs/ss.png" alt="Overview of the Bio-benchmark framework" width="800"/>
</p>
<p align="center">
  <em>Figure 1: Overview of the paper. Bio-benchmark is divided into sequence and text data. The process involves using six LLMs to generate answers for 30 subtasks, extracting them with BioFinder, and then performing evaluation and analysis.</em>
</p>

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

## 📈 Complete Benchmark Results

The following table details the performance of six large language models across all 30 subtasks in the Bio-benchmark, comparing zero-shot (0-shot) and five-shot (5-shot) settings.

<div style="overflow-x: auto; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">

| Domain | Subtask | Count | GPT-4o (0s) | GPT-4o (5s) | InternLM-2.5 20b (0s) | InternLM-2.5 20b (5s) | Llama-3.1 70b (0s) | Llama-3.1 70b (5s) | Mistral-large-2 (0s) | Mistral-large-2 (5s) | Qwen 2.5-72b (0s) | Qwen 2.5-72b (5s) | Yi-1.5 34b (0s) | Yi-1.5 34b (5s) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Protein** | Protein-species-prediction | 200 | 9.00 | 76.50 | 4.00 | 78.50 | 9.50 | 79.00 | 8.50 | 82.00 | 10.00 | 76.00 | 12.00 | 75.00 |
| | Protein-inverse-folding | 264 | 6.97 | 6.29 | 1.46 | 4.64 | 6.69 | 6.88 | 5.65 | 6.70 | 7.02 | 6.95 | 4.48 | 5.77 |
| | Protein-structure-prediction | 264 | 25.09 | 29.79 | 3.96 | 28.21 | 24.63 | 34.31 | 21.02 | 24.23 | 18.11 | 27.13 | 5.99 | 23.99 |
| **RBP** | RNA-binding-protein | 70 | 57.14 | 61.43 | 44.29 | 50.00 | 52.86 | 51.43 | 52.86 | 71.43 | 47.14 | 47.14 | 48.57 | 48.57 |
| **RNA** | RNA-function-prediction | 280 | 4.64 | 87.86 | 2.14 | 78.57 | 3.93 | 88.57 | 4.64 | 71.79 | 6.07 | 79.29 | 3.93 | 91.07 |
| | RNA-inverse-folding | 200 | 19.76 | 21.71 | 20.64 | 27.19 | 19.50 | 26.25 | 20.62 | 22.90 | 20.28 | 21.92 | 12.99 | 21.82 |
| | RNA-structure-prediction | 200 | 0.50 | 2.14 | 0.00 | 2.26 | 0.07 | 0.75 | 0.65 | 0.10 | 0.43 | 0.07 | 0.09 | 0.37 |
| | sgRNA-efficiency-prediction | 300 | 0.67 | 39.33 | 36.67 | 0.00 | 1.33 | 0.67 | 7.67 | 0.33 | 0.33 | 20.67 | 0.00 | 13.33 |
| **Drug** | Drug-Drug-interaction | 86 | 46.51 | 33.72 | 12.79 | 10.47 | 36.05 | 36.05 | 25.58 | 36.05 | 34.88 | 31.40 | 22.09 | 29.07 |
| | Drug-Target-interaction | 60 | 43.33 | 70.00 | 40.00 | 73.33 | 51.67 | 61.67 | 10.00 | 50.00 | 43.33 | 58.33 | 33.33 | 58.33 |
| | Drug-design | 58 | 70.69 | 84.48 | 81.03 | 84.48 | 12.07 | 86.21 | 48.28 | 91.38 | 44.83 | 87.93 | 58.62 | 86.21 |
| **EHR** | Agentclinic | 214 | 82.24 | 62.15 | 63.55 | 69.16 | 79.44 | 80.84 | 78.97 | 78.97 | 73.83 | 77.57 | 61.21 | 67.29 |
| | CMB-Clinic | 74 | 94.93 | 93.92 | 80.95 | 84.66 | 88.90 | 85.14 | 95.54 | 77.08 | 98.56 | 97.97 | 91.55 | 81.35 |
| | IMCS-MRG | 200 | 63.02 | 69.02 | 62.82 | 0.00 | 67.21 | 70.21 | 61.56 | 68.64 | 62.98 | 68.48 | 69.20 | 69.40 |
| **Medical** | HeadQA | 120 | 90.00 | 90.83 | 66.67 | 66.67 | 86.67 | 83.33 | 86.67 | 83.33 | 82.50 | 83.33 | 70.83 | 64.17 |
| | MedLFQA-HealthQA | 50 | 43.76 | 43.03 | 44.27 | 45.03 | 26.75 | 31.84 | 39.19 | 45.24 | 37.37 | 43.20 | 40.81 | 42.67 |
| | MedLFQA-KQA | 50 | 42.34 | 40.41 | 32.73 | 35.89 | 18.12 | 26.76 | 32.93 | 37.55 | 30.82 | 36.25 | 30.77 | 26.88 |
| | MedLFQA-LiveQA | 50 | 29.57 | 29.60 | 26.05 | 28.69 | 17.76 | 19.95 | 24.80 | 28.67 | 25.07 | 28.25 | 22.82 | 19.85 |
| | MedLFQA-MedicationQA | 50 | 32.70 | 36.94 | 33.54 | 36.31 | 21.45 | 24.25 | 28.99 | 33.84 | 35.82 | 36.26 | 28.51 | 27.08 |
| | MedMCQA | 100 | 78.00 | 79.00 | 56.00 | 56.00 | 76.00 | 80.00 | 78.00 | 84.00 | 67.00 | 70.00 | 57.00 | 60.00 |
| | MedQA-CN | 50 | 82.00 | 82.00 | 82.00 | 80.00 | 84.00 | 82.00 | 70.00 | 72.00 | 88.00 | 90.00 | 82.00 | 84.00 |
| | MedQA-TW | 50 | 90.00 | 88.00 | 60.00 | 66.00 | 86.00 | 86.00 | 80.00 | 76.00 | 82.00 | 82.00 | 62.00 | 64.00 |
| | MedQA-US | 50 | 92.00 | 80.00 | 52.00 | 54.00 | 86.00 | 84.00 | 84.00 | 80.00 | 84.00 | 68.00 | 46.00 | 48.00 |
| | MMCU | 142 | 59.15 | 61.27 | 35.92 | 38.03 | 62.68 | 59.15 | 48.59 | 46.48 | 62.68 | 63.38 | 46.48 | 49.30 |
| **TCM** | CMB-Exam | 200 | 56.00 | 60.50 | 62.50 | 61.50 | 50.50 | 51.00 | 43.50 | 45.50 | 59.50 | 64.00 | 54.50 | 68.50 |
| | CMMLU-TCM | 185 | 72.97 | 73.51 | 80.00 | 82.70 | 65.41 | 71.35 | 61.62 | 57.84 | 82.70 | 83.24 | 78.38 | 83.78 |
| | MedLFQA-TCM | 200 | 72.00 | 73.50 | 82.00 | 85.00 | 63.00 | 64.50 | 59.00 | 61.50 | 82.50 | 90.00 | 75.50 | 87.50 |
| | TCMSD | 200 | 39.00 | 68.75 | 30.00 | 60.75 | 16.00 | 69.25 | 32.25 | 67.00 | 38.25 | 67.25 | 34.50 | 59.00 |

</div>

---

## ©️ Citation

```bibtex
@article{jiang2025benchmarking,
  title={Benchmarking large language models on multiple tasks in bioinformatics nlp with prompting},
  author={Jiang, Jiyue and Chen, Pengan and Wang, Jiuming and He, Dongchen and Wei, Ziqin and Hong, Liang and Zong, Licheng and Wang, Sheng and Yu, Qinze and Ma, Zixian and others},
  journal={arXiv preprint arXiv:2503.04013},
  year={2025}
}
