<center>
  <img src="https://git.soton.ac.uk/meldb/concepts-processing/-/raw/main/docs/img/University_of_Southampton_Logo.png" height="100" style="padding-right: 50px;" />
  <img src="https://git.soton.ac.uk/meldb/concepts-processing/-/raw/main/docs/img/swansea-university-logo-vector.png" height="100" />
</center>

# A Tool for Automating the Curation of Medical Concepts derived from Coding Lists (ACMC)

### Jakub J. Dylag <sup>1</sup>, Roberta Chiovoloni <sup>3</sup>, Ashley Akbari <sup>3</sup>, Simon D. Fraser <sup>2</sup>, Michael J. Boniface <sup>1</sup>

<sup>1</sup> Digital Health and Biomedical Engineering, School of Electronics and Computer Science, Faculty of Engineering and Physical Sciences, University of Southampton<br>
<sup>2</sup> School of Primary Care Population Sciences and Medical Education, University of Southampton <br>
<sup>3</sup> Population Data Science, Swansea University Medical School, Faculty of Medicine, Health & Life Science, Swansea University <br>

*Correspondence to: Jakub J. Dylag, Digital Health and Biomedical Engineering, School of Electronics and Computer Science, Faculty of Engineering and Physical Sciences, University of Southampton, J.J.Dylag@soton.ac.uk*

### Citation
> Dylag JJ, Chiovoloni R, Akbari A, Fraser SD, Boniface MJ. A Tool for Automating the Curation of Medical Concepts derived from Coding Lists. GitLab [Internet]. May 2024. Available from: https://git.soton.ac.uk/meldb/concepts-processing

## Introduction

ACMC is a tool that automates the verification, translation and organisation of medical coding lists defining  phenotypes for inclusion criteria in cohort analysis. By processing externally sourced clinical inclusion criteria into actionable code lists, this tool ensures consistent and efficient curation of cohort definitions. These code lists can be subsequently used by data providers to construct study cohorts.

## Requirements

- Python 3.9 or higher

## Installation

To install the `acmc` package, simply run:

```bash
pip install acmc
```

Once installed, you'll be ready to use the `acmc` tool along with the associated vocabularies.

## Getting Started

### Install Clinically Assured NHS TRUD Code Mappings

1. **Register at TRUD**

	Registry your account with TRUD  at [NHS TRUD](https://isd.digital.nhs.uk/trud/user/guest/group/0/account/form).

3. **Subscribe and Accept Licenses**: Subscribe to the following data files:

   - [NHS Read Browser](https://isd.digital.nhs.uk/trud/users/guest/filters/2/categories/9/items/8/releases)
   - [NHS Data Migration](https://isd.digital.nhs.uk/trud/users/guest/filters/0/categories/8/items/9/releases)
   - [ICD10 Edition 5 XML](https://isd.digital.nhs.uk/trud/users/guest/filters/0/categories/28/items/259/releases)
   - [OPCS-4.10 Data Files](https://isd.digital.nhs.uk/trud/users/guest/filters/0/categories/10/items/119/releases)

   After subscribing, you'll receive an API key once your request is approved (usually within a few hours).

4. **Get TRUD API KEY**

	Copy your API key from [NHS TRUD Account Management](https://isd.digital.nhs.uk/trud/users/authenticated/filters/0/account/manage) and store it securely.

7. **Add TRUD API KEY to as an environment variable**

	To set the environment variable temporarily (for the current session), run:

	On macOS/Linux:

   ```bash
   export ACMC_TRUD_API_KEY="your_api_key_here"
   ```

   On Windows (Command Prompt or PowerShell):

   ```bash
   setx ACMC_TRUD_API_KEY "your_api_key_here"
   ```

4. **Download and Install TRUD Resources**:

	Run the following `acmc` command to download and process the TRUD resources:

   ```bash
   acmc trud install
   ```

### Install OMOP Vocabularies 

1. **Register with [OHDSI Athena](https://athena.ohdsi.org/auth/login)**

2. **Download vocabularies from [OHDSI Athena](https://athena.ohdsi.org/vocabulary/list)**

	* Required vocabularies include:
	  * 1) SNOMED
	  * 2) ICD9CM
	  * 17) Readv2
	  * 21) ATC
	  * 55) OPCS4
	  * 57) HES Specialty
	  * 70) ICD10CM
	  * 75) dm+d
	  * 144) UK Biobank
	  * 154) NHS Ethnic Category
	  * 155) NHS Place of Service

	You will be notified by email (usually within an hour) with a vocabularies version number and link to download a zip file of OMOP database tables in CSV format. The subject will be `OHDSI Standardized Vocabularies. Your download link` from `pallas@ohdsi.org`

```
Content of your package

Vocabularies release version: v20240830
acmc-omop Vocabularies:
SNOMED	-	Systematic Nomenclature of Medicine - Clinical Terms (IHTSDO)
ICD9CM	-	International Classification of Diseases, Ninth Revision, Clinical Modification, Volume 1 and 2 (NCHS)
Read	-	NHS UK Read Codes Version 2 (HSCIC)
ATC	-	WHO Anatomic Therapeutic Chemical Classification
OPCS4	-	OPCS Classification of Interventions and Procedures version 4 (NHS)
HES Specialty	-	Hospital Episode Statistics Specialty (NHS)
ICD10CM	-	International Classification of Diseases, Tenth Revision, Clinical Modification (NCHS)
dm+d	-	Dictionary of Medicines and Devices (NHS)
UK Biobank	-	UK Biobank (UK Biobank)
NHS Ethnic Category	-	NHS Ethnic Category
NHS Place of Service	-	NHS Admission Source and Discharge Destination
Installation of the OHDSI Standardized Vocabularies

Please execute the following process:

    Click on this link to download the zip file. Typical file sizes, depending on the number of vocabularies selected, are between 30 and 1500 MB.
    Unpack.
    Reconstitute CPT-4. See below for details.
    If needed, create the tables.
    Load the unpacked files into the tables.
```

Download the OMOP file onto your computer and note the path to the file

4. **Install OMOP vocabularies**

	Run the following `acmc` command to create a local OMOP database from the OMOP zip file with a specific version:

	```bash
	acmc omop install -f <path to downloaded OMOP zip file> -v <release version from email>
	```
Expected output:

```bash
[INFO] - Installing OMOP from zip file: ../data/acmc-omop.zip
[INFO] - Extracted OMOP zip file ../data/acmc-omop.zip to vocab/omop/
[INFO] - Processing 1 of 9 tables: vocab/omop/CONCEPT.csv
[INFO] - Processing 2 of 9 tables: vocab/omop/DOMAIN.csv
[INFO] - Processing 3 of 9 tables: vocab/omop/CONCEPT_CLASS.csv
[INFO] - Processing 4 of 9 tables: vocab/omop/RELATIONSHIP.csv
[INFO] - Processing 5 of 9 tables: vocab/omop/DRUG_STRENGTH.csv
[INFO] - Processing 6 of 9 tables: vocab/omop/VOCABULARY.csv
[INFO] - Processing 7 of 9 tables: vocab/omop/CONCEPT_SYNONYM.csv
[INFO] - Processing 8 of 9 tables: vocab/omop/CONCEPT_ANCESTOR.csv
[INFO] - Processing 9 of 9 tables: vocab/omop/CONCEPT_RELATIONSHIP.csv
[INFO] - OMOP installation completed
```

## **Example Usage**

Follow these steps to initialize and manage a phenotype using `acmc`. In this example, we use a source concept list for the Concept Set `Abdominal Pain` created from [ClinicalCodes.org](ClinicalCodes.org). The source concept codes are read2. We genereate versioned phenotypes for read2 and translate to snomed in normalised, standard formats. 

1. **Initialize a phenotype in the workspace**

	Use the followijng `acmc` command to initialize the phenotype in a local Git repository:

```bash
acmc phen init
```

Expected Output:

```bash
[INFO] - Initialising Phenotype in directory: <path>/concepts-processing/workspace/phen
[INFO] - Creating phen directory structure and config files
[INFO] - Phenotype initialised successfully
```

2. **Copy example medical code lists to the phenotype codes directory**

	From the command prompt, copy medical code lists `/examples/codes`to the phenotype code directory:

```bash
cp -r ./examples/concepts/* ./workspace/phen/concepts
```

   - You can view the source code list here [`res176-abdominal-pain.csv`](.//examples/codes/clinical-codes-org/Symptom%20code%20lists/Abdominal%20pain/res176-abdominal-pain.csv)
   - Alternatively, place your code lists in `./workspace/phen/codes`.

3. **Copy the example phenotype configuration file to the phenotype directory**

	From the command prompt, copy example phenotype configuration files `/examples/config.json` to the phenotype directory:

```bash
cp -r ./examples/config1.yml ./workspace/phen/config.yml
```

   - You can view the configuarion file here [`config.json`](./examples/config.json) 
   - Alternatively, place your own `config.json` file in `./workspace/phen`.
     
4. **Validate the phenotype configuration**

	Use the followijng `acmc` command to validate the phenotype configuration to ensure it's correct:

```bash
acmc phen validate
```

Expected Output:

```bash
[INFO] - Validating phenotype: <path>/concepts-processing/workspace/phen
[INFO] - Phenotype validated successfully
```

5. **Generate phenotype in Read2 code format**

	Use the following `acmc` command to generate the phenotype in `read2` format:

```bash
acmc phen map -t read2
```

Expected Output:

```bash
[INFO] - Processing phenotype: <path>/concepts-processing/workspace/phen
[INFO] - Validating phenotype: <path>/concepts-processing/workspace/phen
[INFO] - Phenotype validated successfully
[INFO] - Processing read2 codes for <path>/concepts-processing/workspace/phen/concepts/clinical-codes-org/Symptom code lists/Abdominal pain/res176-abdominal-pain.csv
[INFO] - Converting to target code type read2
[INFO] - Saved mapped concepts to <path>/concepts-processing/workspace/phen/map/read2.csv
[INFO] - Phenotype processed target code type read2
[INFO] - Phenotype processed successfully
```

The concept sets translating read2 to the acmc normalised CSV format will be stored in `./workspace/phen/concept-set/snomed/` in, e.g. `./workspace/phen/concept-set/read2/ABDO_PAIN.csv`.

6. **Publish phenotype at an initial version**

	Use the following `acmc` command to publish the phenotype at an initial version:

```bash
acmc phen publish
```

Expected Output:

```bash
[INFO] - Validating phenotype: <path>/concepts-processing/workspace/phen
[INFO] - Phenotype validated successfully
[INFO] - New version: 0.0.1
[INFO] - Phenotype published successfully
```

7. **Generate phenotype in Read3 code format**

Generate the phenotype in `read3` format:

```bash
acmc phen map -t read3
```

Expected Output:

```bash
[INFO] - Processing phenotype: <path>/concepts-processing/workspace/phen
[INFO] - Validating phenotype: <path>/concepts-processing/workspace/phen
[INFO] - Phenotype validated successfully
[INFO] - Processing read2 codes for <path>/concepts-processing/workspace/phen/concepts/clinical-codes-org/Symptom code lists/Abdominal pain/res176-abdominal-pain.csv
[INFO] - Converting to target code type read3
[INFO] - Saved mapped concepts to <path>/concepts-processing/workspace/phen/map/read3.csv
[INFO] - Phenotype processed target code type read3
[INFO] - Phenotype processed successfully
```

The concept sets translating read2 to snomed will be stored in acmc CSV format in `./workspace/phen/concept-set/snomed/`, e.g. `./workspace/phen/concept-set/snomed/ABDO_PAIN.csv`

8. **Compare the previous version `0.0.1` with the latest version**

	Use the following `acmc` command to compare the previous version `0.0.1` with the latest version in the workspace phen directory:

```bash
acmc phen diff -ov 0.0.1
```

Expected Output:

```bash
[INFO] - Validating phenotype: ./workspace/v1.0.3/
[INFO] - Phenotype validated successfully
[INFO] - Validating phenotype: <path>/concepts-processing/workspace/phen
[INFO] - Phenotype validated successfully
[INFO] - Phenotypes diff'd successfully
```

A report comparing the phenotype versions will be created in the workspace called './workspace/phen/latest_0.0.1_diff.md'

9. **Publish the phenotype at a major version**

	Use the following `acmc` command to publish the phenotype at a major version:

```bash
acmc phen publish -i major
```

Expected Output:

```bash
[INFO] - Validating phenotype: /home/mjbonifa/datahdd/brcbat/derived_datasets/mjbonifa/concepts-processing/workspace/phen
[INFO] - Phenotype validated successfully
[INFO] - New version: 1.0.0
[INFO] - Phenotype published successfully
```

## Support

If you need help please open an [issue in the repository](https://git.soton.ac.uk/meldb/concepts-processing/-/issues)

## Contributing

Please contacted the corresponding author Jakub Dylag at J.J.Dylag@soton.ac.uk.

## Acknowledgements  

This project was developed in the context of the [MELD-B](https://www.southampton.ac.uk/publicpolicy/support-for-policymakers/policy-projects/Current%20projects/meld-b.page) project, which is funded by the UK [National Institute of Health Research](https://www.nihr.ac.uk/) under grant agreement NIHR203988.

## License

This work is licensed under a [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

![apache2](https://img.shields.io/github/license/saltstack/salt)
