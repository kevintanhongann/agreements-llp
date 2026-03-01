#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import argparse
import subprocess
import sys
from pathlib import Path

def get_base_dir() -> Path:
    return Path(__file__).parent.resolve()

def get_agreements_dir() -> Path:
    # Check for both 'agreements' and 'base' as mentioned in prompt/example
    base_dir = get_base_dir()
    for name in ["agreements", "base"]:
        p = base_dir / name
        if p.is_dir():
            return p
    return base_dir / "agreements"

def get_templates_dir() -> Path:
    base_dir = get_base_dir()
    for name in ["templates", "template"]:
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

def main():
    parser = argparse.ArgumentParser(description="Generate agreement document using pandoc")
    
    # Listing options
    parser.add_argument("-l", "--list", action="store_true", help="List possible agreements based on folder content")
    parser.add_argument("-T", "--list-templates", action="store_true", help="List possible templates based on folder content")
    
    # Generation options
    parser.add_argument("-a", "--agreement", help="Selected agreement name (folder name)")
    parser.add_argument("-t", "--template", help="Template name (if doesn't exist in current dir, lookup in templates dir)")
    parser.add_argument("-f", "--vars-file", default="vars.yml", help="Location of vars.yml metadata file (default: vars.yml)")
    parser.add_argument("-o", "--output", default="terms.odt", help="Output file name (default: terms.odt)")
    
    args = parser.parse_args()
    
    if args.list:
        list_agreements()
        sys.exit(0)
        
    if args.list_templates:
        list_templates()
        sys.exit(0)
        
    if not args.agreement:
        parser.error("The -a/--agreement argument is required unless using listing flags (-l or -T)")
        
    if not args.template:
        parser.error("The -t/--template argument is required unless using listing flags (-l or -T)")
        
    base_dir = get_base_dir()
    
    # Resolve agreement content.md
    agreement_dir = get_agreements_dir() / args.agreement
    content_file = agreement_dir / "content.md"
    if not content_file.exists():
        print(f"Error: Agreement content file not found at {content_file}", file=sys.stderr)
        sys.exit(1)
        
    # Resolve template
    template_file = Path(args.template)
    if not template_file.exists():
        # Lookup in templates dir
        template_file = get_templates_dir() / args.template
        if not template_file.exists():
            print(f"Error: Template file not found: {args.template}", file=sys.stderr)
            sys.exit(1)
            
    # Resolve vars file
    vars_file = Path(args.vars_file)
    if not vars_file.exists():
        print(f"Error: Variables file not found at {vars_file}", file=sys.stderr)
        sys.exit(1)
        
    # Look for vars.lua in the same directory as the script
    lua_filter = base_dir / "filters" / "vars.lua"
    
    # Construct pandoc command
    # pandoc --reference-doc template/agreement.ott base/general-terms-of-engagement/content.md -o terms.odt --metadata-file vars.yml --lua-filter vars.lua
    cmd = [
        "pandoc",
        "--reference-doc", str(template_file),
        str(content_file),
        "-o", args.output,
        "--metadata-file", str(vars_file)
    ]
    
    if lua_filter.exists():
        cmd.extend(["--lua-filter", str(lua_filter)])
    else:
        print(f"Warning: Lua filter {lua_filter} not found, proceeding without it.")
        
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print("Success!")
    except subprocess.CalledProcessError as e:
        print(f"Pandoc command failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: pandoc command not found. Please ensure pandoc is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
