#!/usr/bin/env python

# Copyright 2026. Mohd Izhar Firdaus Bin Ismail
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import subprocess
import sys
import yaml
import re
import tempfile
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def get_base_dir() -> Path:
    return Path(__file__).parent.resolve()


def get_agreements_dir() -> Path:
    base_dir = get_base_dir()
    for name in ["agreements", "base"]:
        p = base_dir / name
        if p.is_dir():
            return p
    return base_dir / "agreements"


def get_templates_dir() -> Path:
    base_dir = get_base_dir()
    for name in ["templates"]:
        p = base_dir / name
        if p.is_dir():
            return p
    return base_dir / "templates"


def list_agreements():
    agreements_dir = get_agreements_dir()
    if not agreements_dir.exists():
        print(f"Directory not found: {agreements_dir}")
        return
    print("Available agreements:")
    for item in sorted(agreements_dir.iterdir()):
        if item.is_dir():
            # Check if it has content.md
            if (item / "content.md").exists():
                print(f"  - {item.name}")
            else:
                print(f"  - {item.name} (warning: no content.md found)")


def list_templates():
    templates_dir = get_templates_dir()
    if not templates_dir.exists():
        print(f"Directory not found: {templates_dir}")
        return
    print("Available templates:")
    for item in sorted(templates_dir.iterdir()):
        if item.is_file() and not item.name.startswith("."):
            print(f"  - {item.name}")


def parse_frontmatter(content_file: Path):
    """
    Parses YAML frontmatter from a markdown file.
    Returns a tuple of (metadata_dict, body_content).
    """
    metadata = {}
    content = ""
    try:
        with open(content_file, "r", encoding="utf-8") as f:
            content = f.read()

        if content.startswith("---"):
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
            if match:
                frontmatter = match.group(1)
                body = match.group(2)
                metadata = yaml.safe_load(frontmatter) or {}
                return metadata, body
    except Exception as e:
        print(f"Warning: Failed to parse frontmatter: {e}")

    return metadata, content


def main():
    parser = argparse.ArgumentParser(
        description="Generate agreement document using pandoc"
    )

    # Listing options
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List possible agreements based on folder content",
    )
    parser.add_argument(
        "-T",
        "--list-templates",
        action="store_true",
        help="List possible templates based on folder content",
    )

    # Generation options
    parser.add_argument(
        "-a", "--agreement", help="Selected agreement name (folder name)"
    )
    parser.add_argument(
        "-t",
        "--template",
        help="Template name (if doesn't exist in current dir, lookup in templates dir)",
    )
    parser.add_argument(
        "-f",
        "--vars-file",
        default="vars.yml",
        help="Location of vars.yml metadata file (default: vars.yml)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.odt",
        help="Output file name (default: output.odt)",
    )

    args = parser.parse_args()

    if args.list:
        list_agreements()
        sys.exit(0)

    if args.list_templates:
        list_templates()
        sys.exit(0)

    if not args.agreement:
        parser.error(
            "The -a/--agreement argument is required unless using listing flags (-l or -T)"
        )

    base_dir = get_base_dir()

    # Resolve agreement content.md
    agreement_dir = get_agreements_dir() / args.agreement
    content_file = agreement_dir / "content.md"
    if not content_file.exists():
        print(
            f"Error: Agreement content file not found at {content_file}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Load variables from vars.yml
    vars_file = Path(args.vars_file)
    if not vars_file.exists():
        print(f"Error: Variables file not found at {vars_file}", file=sys.stderr)
        sys.exit(1)

    with open(vars_file, "r", encoding="utf-8") as f:
        global_vars = yaml.safe_load(f) or {}

    # Parse frontmatter and body
    metadata, body = parse_frontmatter(content_file)

    # Merge variables (CLI/metadata file overrides frontmatter)
    # Also uppercase keys for compatibility with ${VAR} style in lua if needed,
    # but we will use Jinja2.
    all_vars = {**metadata, **global_vars}

    # Uppercase versions for ${VAR} legacy support
    legacy_vars = {k.upper(): v for k, v in all_vars.items() if isinstance(k, str)}
    all_vars.update(legacy_vars)

    # Resolve template
    if not args.template:
        args.template = metadata.get("default_template", "default.odt")

    template_file = Path(args.template)
    if not template_file.exists():
        # Lookup in templates dir
        template_file = get_templates_dir() / args.template
        if not template_file.exists():
            print(f"Error: Template file not found: {args.template}", file=sys.stderr)
            sys.exit(1)

    # Preprocess body using Jinja2
    env = Environment(loader=FileSystemLoader(str(agreement_dir)))

    # We want to support both Jinja2 tags and ${VAR} style replacements.
    # We can use Jinja2 for the tags, then a simple regex/replace for ${VAR}.
    try:
        jinja_template = env.from_string(body)
        rendered_body = jinja_template.render(**all_vars)

        # Legacy support for ${VAR}
        def legacy_replace(match):
            name = match.group(1).upper()
            return str(all_vars.get(name, match.group(0)))

        rendered_body = re.sub(r"\$\{(.*?)\}", legacy_replace, rendered_body)

    except Exception as e:
        print(f"Error during template preprocessing: {e}", file=sys.stderr)
        sys.exit(1)

    # Write rendered content to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
        # Re-add metadata as YAML frontmatter for pandoc if needed (e.g. for title)
        tmp.write("---\n")
        yaml.dump(metadata, tmp)
        tmp.write("---\n\n")
        tmp.write(rendered_body)
        tmp_path = tmp.name

    try:
        # Check if output is PDF
        is_pdf = args.output.lower().endswith(".pdf")
        pandoc_output = args.output
        if is_pdf:
            # Generate intermediate ODT first
            pandoc_output = str(Path(args.output).with_suffix(".odt").resolve())

        # Construct pandoc command
        cmd = [
            "pandoc",
            "--reference-doc",
            str(template_file),
            tmp_path,
            "-o",
            pandoc_output,
            "--metadata-file",
            str(vars_file),
            "--resource-path",
            f".:{agreement_dir}",
        ]

        filters_dir = base_dir / "filters"
        if filters_dir.exists() and filters_dir.is_dir():
            for lua_filter in sorted(filters_dir.glob("*.lua")):
                cmd.extend(["--lua-filter", str(lua_filter)])
            for regular_filter in sorted(filters_dir.glob("*.filter")):
                cmd.extend(["--filter", str(regular_filter)])

        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

        if is_pdf:
            print(f"Converting {pandoc_output} to PDF using LibreOffice...")
            lo_cmd = [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(Path(args.output).parent.resolve()),
                pandoc_output,
            ]
            subprocess.run(lo_cmd, check=True)
            # Remove intermediate ODT
            if Path(pandoc_output).exists():
                Path(pandoc_output).unlink()

        print(f"Success! Document generated: {args.output}")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(
            "Error: pandoc command not found. Please ensure pandoc is installed and in your PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    finally:
        if Path(tmp_path).exists():
            Path(tmp_path).unlink()


if __name__ == "__main__":
    main()
