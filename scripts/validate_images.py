#!/usr/bin/env python3


from pathlib import Path
import yaml


def _main():
    p = Path('content/')
    md_file_paths = p.glob('**/*.md')
    for md_file_path in md_file_paths:
        with open(md_file_path) as fp:
            # There should be two components to every doc, "front matter" (YAML/TOML/JSON),
            # followed by the actual Markdown content. We can read the first one but probably
            # don't want to try and parse the actual content.
            print(f"[*] Loading content from {md_file_path}")
            yaml_content = yaml.safe_load_all(fp)
            front_matter = next(yaml_content)
            # From the front matter, get the list of resources, if available.
            resources = front_matter.get('resources')
            if not resources:
                print(f"    [*] No 'resources' key found in front matter, continuing")
                continue

            for resource in resources:
                # Get the 'src' property, then see if the file exists.
                src = resource.get('src')
                if not src:
                    print(f"    [-] Resource does not contain 'src' key, may want to investigate front matter in {md_file_path}")
                    continue

                resource_path = md_file_path.with_name(src)
                print(f"    [*] Checking if {resource_path} exists")
                if resource_path.exists():
                    print(f"        [+] Resource {resource_path} exists")
                else:
                    print(f"        [-] Resource {resource_path} does NOT exist, review directory contents or source in {md_file_path}")
        print()

if __name__ == "__main__":
    _main()
