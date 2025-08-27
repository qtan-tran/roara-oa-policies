# ROARA OA Policies

Welcome to the **ROARA OA Policies** repository, part of the **Repercussions of Open Access on Research Assessment (ROARA)** project at Bielefeld University, created by Quoc-Tan Tran. This repository hosts Open Access (OA) policy documents, datasets, and tools for qualitative content analysis to study the impact of OA policies on research evaluation. It is designed for researchers, policymakers, and open science enthusiasts to explore, replicate, or extend the analysis with a strong emphasis on **reproducibility**.

## Project Overview

The ROARA project examines the effects of Open Access (OA) policies on international and national research landscapes, focusing on their intersection with research evaluation. The analysis targets policies from key countries (Germany, the Netherlands, South Africa, Indonesia, Canada, and Colombia), selected for their unique research characteristics, such as R&D expenditures, evaluation approaches, and diversity of research institutions.

Policy documents from major stakeholders (e.g., state ministries, national research councils, public and private funders) are collected from sources like the Sherpa Juliet database and national OA repositories (e.g., OA-Atlas). These documents are stored in this repository for qualitative content analysis, using a codebook developed both inductively and deductively to assess policy type, key features (e.g., immediate OA), range, strength, influence, and links to research evaluation. The goal is to understand how OA mandates shape research assessment practices globally and nationally.

## Repository Structure

The repository is organized for clarity, reproducibility, and ease of use:

- **`policies/`**: Stores canonical OA policy texts as PDFs (`policies/pdf/`), extracted text files (`policies/text/`), and metadata (`policies/metadata/`).
- **`data/`**: Contains raw (`data/raw/`) and processed datasets (`data/processed/`), with controlled vocabularies (`data/lookups/`).
- **`methods/`**: Includes codebooks, policy strength rubrics, sampling strategies, and reliability protocols.
- **`snippets/`**: Houses annotated policy excerpts (`snippets/by_policy/`) and analytical memos (`snippets/memos/`).
- **`analysis/`**: Provides Jupyter notebooks (`analysis/notebooks/`) and Python scripts (`analysis/scripts/`) for data processing and visualization, with outputs in `analysis/outputs/`.
- **`reports/`**: Stores manuscript drafts (`reports/manuscript/`), presentation slides (`reports/slides/`), and references.
- **`templates/`**: Offers reusable templates for metadata and data release checklists.
- **`qa/`**: Contains validation rules (`qa/validation_rules.yaml`) and linting scripts (`qa/lint_tables.py`) for quality assurance.
- **`docs/`**: Includes human-readable guides, naming conventions, data dictionary, and style guidelines.

Each subfolder has a `GUIDE.md` file with instructions for adding, organizing, or validating content. See `docs/` for an overview of conventions and contributor guidelines.

## Reproducibility Instructions

To ensure future research replication, this repository provides all necessary code, data, and documentation to rerun the OA policy analysis. The primary analysis script (`analysis/scripts/score_oa_policies.py`) implements the MELIBEA scoring method (Vincent-Lamarre et al., 2015) to evaluate policy strength.

### Prerequisites
- **Software**:
  - Python 3.8 or higher (tested with Python 3.10).
  - Git for version control (recommended: install with "Git from the command line and also from 3rd-party software" option).
- **Dependencies**:
  - Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` (in the repository root) specifies exact versions, e.g., `pandas==2.2.2`.
- **Expected Runtime**: The `score_oa_policies.py` script processes policy text files in approximately 1–2 minutes on a standard desktop (e.g., 2.5 GHz CPU, 8 GB RAM), depending on the number of files.

### Setup and File Placement
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/[your_username_here]/roara-oa-policies.git
   cd roara-oa-policies
   ```
2. **Place Policy Files**:
   - Store policy text files in `policies/text/` (e.g., `policy_institution.txt`). If using PDFs, extract text to `.txt` files:
     ```bash
     pdftotext policies/pdf/policy.pdf policies/text/policy.txt
     ```
   - Ensure all text files are in `policies/text/`, as the script expects this directory.
3. **Outputs**:
   - The script generates a CSV file (`policy_scores.csv`) in `analysis/outputs/tables/` with policy names, detected options, and MELIBEA scores (initial and updated).

### Running the Analysis
1. **Install Dependencies**:
   ```bash
   pip install pandas
   ```
   (Or use `requirements.txt` if provided.)
2. **Run the Script**:
   ```bash
   python analysis/scripts/score_oa_policies.py
   ```
   - The script reads all `.txt` files in `policies/text/`, applies the MELIBEA scoring (based on regex detection of policy conditions), and outputs results to `analysis/outputs/tables/policy_scores.csv`.
   - The script is thoroughly commented, explaining each step (e.g., condition detection, score calculation).
3. **Verify Outputs**:
   - Check `analysis/outputs/tables/policy_scores.csv` for results.
   - Use `analysis/notebooks/` for exploratory analysis or visualization.

### Adding Your Own Policy Files
- Place new policy text files in `policies/text/`.
- Update metadata in `policies/metadata/` using `templates/policy_metadata_template.yml`.
- Rerun the script to include new policies in the analysis.

### Reproducibility Notes
- **Version Control**: All code and data are versioned via Git. Use tagged releases (e.g., `v1.0.0`) for stable snapshots.
- **Dependency Lock**: The `requirements.txt` ensures consistent library versions.
- **Validation**: Use `qa/lint_tables.py` to validate outputs and `qa/validation_rules.yaml` for data consistency.
- **Archiving**: Repository releases are linked to Zenodo for a citable DOI, ensuring long-term accessibility.

## Forking the Repository
To contribute or adapt this project:
1. **Fork**:
   - Click **Fork** on the [repository page](https://github.com/[your_username_here]/roara-oa-policies).
   - Clone your fork:
     ```bash
     git clone https://github.com/your_username/roara-oa-policies.git
     cd roara-oa-policies
     ```
2. **Create a Branch**:
   ```bash
   git checkout -b your-branch-name
   ```
3. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Describe your changes"
   git push origin your-branch-name
   ```
4. Submit a pull request via GitHub (see `CONTRIBUTING.md`).

## Adapting for Your Project
To use this repository’s structure or code:
- **Copy Structure**: Replicate folders (`policies/`, `data/`, etc.) for your policy analysis.
- **Reuse Code**: Adapt `analysis/scripts/score_oa_policies.py` for your dataset. Modify `DETECTION_RULES` for custom policy characteristics.
- **Add Policies**: Place your policy documents in `policies/text/` or `policies/pdf/`.
- **Follow Templates**: Use `templates/policy_metadata_template.yml` for metadata.

## Contribution Guidelines
See `CONTRIBUTING.md` for details on:
- Adding policy documents or data.
- Branch naming and pull request processes.
- Data ethics and validation protocols (see `qa/`).

## License
- **Data and Documents**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) for open sharing and attribution.
- **Code**: [MIT License](https://opensource.org/licenses/MIT) for reuse and modification.
- See `LICENSE` file for details.

## Contact
For questions, collaboration, or reproducibility support, contact Quoc-Tan Tran at Bielefeld University or open an issue on this repository. For data or analysis inquiries, reach out to the Quoc-Tan Tran <quoc-tan.tran@uni-bielefeld.de>.

Thank you for your interest in the ROARA project!
