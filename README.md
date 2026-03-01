# Agreements / Document Generator

This project provides sample agreements for an IT services company and automates their generation using `pandoc`. It combines markdown content files containing agreement text with specific OpenDocument templates, applying variables defined in a YAML file.

## License

The contents of this repository are licensed under the **CC0 1.0 Universal (CC0 1.0) Public Domain Dedication**. 
To view a copy of this license, visit [http://creativecommons.org/publicdomain/zero/1.0/](http://creativecommons.org/publicdomain/zero/1.0/).

## Disclaimer

**THIS DOES NOT CONSTITUTE LEGAL ADVICE.** 

THE DOCUMENTS, TEMPLATES, AND SCRIPTS PROVIDED IN THIS REPOSITORY ARE FOR INFORMATIONAL AND EDUCATIONAL PURPOSES ONLY. THEY DO NOT CONSTITUTE LEGAL ADVICE AND SHOULD NOT BE RELIED UPON AS SUCH. THERE IS ABSOLUTELY NO WARRANTY, EXPRESS OR IMPLIED, REGARDING THE LEGAL EFFICACY, ACCURACY, OR SUITABILITY OF ANY OF THE DOCUMENTS OR CODE PROVIDED HERE. YOU ASSUME ALL RESPONSIBILITY AND RISK FOR THE USE OF THESE MATERIALS. IT IS STRONGLY RECOMMENDED TO CONSULT WITH A QUALIFIED ATTORNEY BEFORE USING ANY LEGAL DOCUMENTS.

## Prerequisites

- [pandoc](https://pandoc.org/) (must be installed and available in your PATH)

## Usage

The primary script for generating documents is `generate.py`.

```bash
./generate.py -a <agreement_name> [options]
```

### Options

| Flag | Long Flag | Description |
| --- | --- | --- |
| `-a` | `--agreement` | **(Required)** Selected agreement name (folder name inside `agreements/`). |
| `-t` | `--template` | Template name (if it doesn't exist in current dir, it will be looked up in the `templates/` folder). If not specified, the script reads `default_template:` from the agreement's YAML frontmatter, or defaults to `default.ott`. |
| `-f` | `--vars-file` | Location of the metadata YAML file containing variable definitions (default: `vars.yml`). |
| `-o` | `--output` | Output file name for the generated document (default: `output.odt`). |
| `-l` | `--list` | List all available agreements based on the `agreements/` folder content. |
| `-T` | `--list-templates`| List all available templates based on the `templates/` folder content. |

### Examples

**List available agreements:**
```bash
./generate.py --list
```

**Generate a document:**
```bash
./generate.py -a my-agreement -o signed_contract.odt
```

**Generate a document with a specific metadata file and template:**
```bash
./generate.py -a my-agreement -f custom_vars.yml -t custom.ott -o output.odt
```

## Directory Structure

- `agreements/` - Contains subdirectories for each agreement. Each subdirectory should contain a `content.md` file with the agreement text.
- `templates/` - Contains the `.ott` (OpenDocument Text Template) or similar template files used for styling the documents.
- `filters/` - Contains Lua filters (`*.lua`) or pandoc filters (`*.filter`) that will be automatically applied during generation.
- `vars.yml` - The default variables file containing metadata to inject into the documents.

