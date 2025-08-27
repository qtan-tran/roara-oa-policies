# ROARA OA Policies

Welcome to the **ROARA OA Policies** repository, part of the **Repercussions of Open Access on Research Assessment (ROARA)** project at Bielefeld University, created by Quoc-Tan Tran. This repository hosts a collection of Open Access (OA) policy documents, datasets, and tools for qualitative content analysis to study the impact of OA policies on research evaluation. It is designed for researchers, policymakers, and open science enthusiasts to explore, replicate, or extend the analysis.

## Project Overview

The ROARA project examines the effects of Open Access (OA) policies on international and national research landscapes, with a focus on how these policies intersect with research evaluation. The analysis targets policies from key countries (Germany, the Netherlands, South Africa, Indonesia, Canada, and Colombia), selected for their unique research characteristics, such as R&D expenditures, evaluation approaches, and diversity of research institutions. 

Policy documents from major stakeholders (e.g., state ministries, national research councils, public and private funders) are collected from sources like the Sherpa Juliet database and national OA repositories (e.g., OA-Atlas). These documents are stored in this repository for qualitative content analysis, using a codebook developed both inductively and deductively to assess policy type, key features (e.g., immediate OA), range, strength, influence, and links to research evaluation. The goal is to understand how OA mandates shape research assessment practices globally and nationally.

## Repository Structure

The repository is organized to ensure clarity, reproducibility, and ease of use:

- **`policies/`**: Stores canonical OA policy texts as PDFs (`policies/pdf/`), extracted text files (`policies/text/`), and metadata (`policies/metadata/`).
- **`data/`**: Contains raw (`data/raw/`) and processed datasets (`data/processed/`), along with controlled vocabularies (`data/lookups/`).
- **`methods/`**: Includes codebooks, policy strength rubrics, sampling strategies, and reliability protocols.
- **`snippets/`**: Houses annotated policy excerpts (`snippets/by_policy/`) and analytical memos (`snippets/memos/`).
- **`analysis/`**: Provides Jupyter notebooks (`analysis/notebooks/`) and Python scripts (`analysis/scripts/`) for data processing and visualization, with outputs in `analysis/outputs/`.
- **`reports/`**: Stores manuscript drafts (`reports/manuscript/`), presentation slides (`reports/slides/`), and references.
- **`templates/`**: Offers reusable templates for metadata and data release checklists.
- **`qa/`**: Contains validation rules (`qa/validation_rules.yaml`) and linting scripts (`qa/lint_tables.py`) for quality assurance.
- **`docs/`**: Includes human-readable guides, naming conventions, data dictionary, and style guidelines.

Each subfolder has a `GUIDE.md` file with instructions for adding, organizing, or validating content. See `docs/` for an overview of conventions and contributor guidelines.

## How to Use This Repository

### Forking the Repository
To contribute or adapt this project for your own analysis:
1. **Fork the Repository**:
   - Click the **Fork** button at the top-right of the [repository page](https://github.com/[your_username_here]/roara-oa-policies).
   - This creates a copy under your GitHub account.
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/your_username/roara-oa-policies.git
   cd roara-oa-policies
   ```
3. **Create a Branch** for your changes:
   ```bash
   git checkout -b your-branch-name
   ```
4. Make changes, commit, and push:
   ```bash
   git add .
   git commit -m "Describe your changes"
   git push origin your-branch-name
   ```
5. Submit a pull request via GitHub to contribute back to the main repository (see `CONTRIBUTING.md`).

### Running Code Locally
To run the analysis scripts or process your own policy files:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/[your_username_here]/roara-oa-policies.git
   cd roara-oa-policies
   ```
2. **Set Up Python Environment**:
   - Ensure Python 3.8+ is installed.
   - Install dependencies:
     ```bash
     pip install pandas
     ```
     (Add other dependencies as needed, e.g., for text processing; check `analysis/scripts/` for requirements.)
3. **Add Your Policy Files**:
   - Place policy PDFs in `policies/pdf/` and extract text to `policies/text/` (e.g., using `pdftotext` or similar tools).
   - Example: Convert a PDF to text:
     ```bash
     pdftotext policies/pdf/policy.pdf policies/text/policy.txt
     ```
4. **Run Analysis Scripts**:
   - Example: Run the policy scoring script (based on Vincent-Lamarre et al., 2015):
     ```bash
     python analysis/scripts/score_oa_policies.py
     ```
   - Outputs (e.g., `policy_scores.csv`) will appear in `analysis/outputs/tables/`.
5. **Customize Analysis**:
   - Modify `methods/policy_strength_rubric.md` for your scoring criteria.
   - Use `analysis/notebooks/` for exploratory analysis or visualization.

### Borrowing and Adapting
To use this repository’s structure or code for your own project:
- **Copy the Structure**: Replicate the folder structure (`policies/`, `data/`, etc.) for your own policy analysis.
- **Reuse Code**: Adapt scripts from `analysis/scripts/` (e.g., `score_oa_policies.py`) for your dataset. Update `DETECTION_RULES` in the script to match your policy characteristics.
- **Add Policies**: Collect your own policy documents and place them in `policies/pdf/` or `policies/text/`.
- **Follow Templates**: Use `templates/policy_metadata_template.yml` to standardize metadata for new policies.

## Contribution Guidelines
Contributions are welcome! Please read `CONTRIBUTING.md` for details on:
- How to add policy documents or data.
- Branch naming conventions and pull request processes.
- Data ethics and validation protocols (see `qa/`).

## License
- **Data and Documents**: Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) for open sharing and attribution.
- **Code**: Licensed under [MIT License](https://opensource.org/licenses/MIT) for flexibility in reuse and modification.
- See `LICENSE` file for full details.

## Contact
For questions or collaboration, contact Quoc-Tan Tran at Bielefeld University or open an issue on this repository.
