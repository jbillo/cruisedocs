#!/usr/bin/env python3


from pathlib import Path
import yaml


def _main():
    p = Path('content/')
    md_file_paths = p.glob('**/*.md')
    for md_file_path in md_file_paths:
        print()
        with open(md_file_path) as fp:
            # We want the original file contents to be able to grab the references to <img
            # that (probably) can't be parsed as YAML and aren't pure Markdown either.
            file_contents = fp.read()
            # There should be two components to every doc, "front matter" (YAML/TOML/JSON),
            # followed by the actual Markdown content. We can read the first one but probably
            # don't want to try and parse the actual content.
            print(f"[*] Loading content from {md_file_path}")
            yaml_content = yaml.safe_load_all(file_contents)
            front_matter = next(yaml_content)
            # From the front matter, get the list of resources, if available.
            resources = front_matter.get('resources')
            if not resources:
                print(f"    [*] No 'resources' key found in front matter, continuing")
                continue

            resource_names = []
            resource_paths = []

            for resource in resources:
                # Get the 'name' property; if it exists add it to the list of resource names
                # to check later in the document.
                name = resource.get('name')
                if name:
                    resource_names.append(name)

                # Get the 'src' property, then see if the file exists.
                src = resource.get('src')
                if not src:
                    print(f"    [-] Resource does not contain 'src' key, may want to investigate front matter in {md_file_path}")
                    continue

                # If we have a name, but the src doesn't start with that name, throw a warning.
                # Might be a mismatch between the file on disk and the resource name.
                if name and not src.startswith(name):
                    print(f"    [-] Resource with name '{name}' doesn't seem to match prefix of src '{src}'")

                resource_path = md_file_path.with_name(src)
                print(f"    [*] Checking if {resource_path} exists")
                if resource_path.exists():
                    print(f"        [+] Resource {resource_path} exists")
                    resource_paths.append(resource_path)
                else:
                    print(f"        [-] Resource {resource_path} does NOT exist, review directory contents or source in {md_file_path}")

            # If we have resource names to check, make sure they appear in the content.
            for resource_name in resource_names:
                if f"{{< img name=\"{resource_name}\"" in file_contents:
                    print(f"    [+] Resource {resource_name} present in front matter and referenced in file content")
                else:
                    print(f"    [-] A resource named {resource_name} was defined, but didn't seem to be referenced as an image in the content")


if __name__ == "__main__":
    _main()
