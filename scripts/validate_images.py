#!/usr/bin/env python3

import logging
from pathlib import Path
import yaml




def _main():
    logging.basicConfig(
        level=logging.INFO,  # change to logging.DEBUG if you need more...
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger(__name__)

    p = Path('content/')
    if not p.exists():
        logger.fatal(f"Path `{p.absolute()}` does not exist; try running `scripts/validate_images.py` from the site root")
        return

    md_file_paths = p.glob('**/*.md')
    for md_file_path in md_file_paths:
        with open(md_file_path) as fp:
            # We want the original file contents to be able to grab the references to <img
            # that (probably) can't be parsed as YAML and aren't pure Markdown either.
            file_contents = fp.read()
            # There should be two components to every doc, "front matter" (YAML/TOML/JSON),
            # followed by the actual Markdown content. We can read the first one but probably
            # don't want to try and parse the actual content.
            logger.debug(f"Loading content from {md_file_path}")
            yaml_content = yaml.safe_load_all(file_contents)
            front_matter = next(yaml_content)
            # From the front matter, get the list of resources, if available.
            resources = front_matter.get('resources')
            if not resources:
                logger.debug(f"No 'resources' key found in front matter of {md_file_path}, continuing")
                continue

            resource_names = []
            resource_paths = set()  # we probably only end up with one element here

            for resource in resources:
                # Get the 'name' property; if it exists add it to the list of resource names
                # to check later in the document.
                name = resource.get('name')
                if name:
                    resource_names.append(name)

                # Get the 'src' property, then see if the file exists.
                src = resource.get('src')
                if not src:
                    logger.warning(f"Resource {resource} does not contain 'src' key, may want to investigate front matter in {md_file_path}")
                    continue

                # If we have a name, but the src doesn't start with that name, throw a warning.
                # Might be a mismatch between the file on disk and the resource name.
                if name and not src.startswith(name):
                    logger.error(f"Resource {resource} with name '{name}' doesn't seem to match prefix of src '{src}'")

                resource_path = md_file_path.with_name(src)
                logger.debug(f"Checking if {resource_path} exists")
                if resource_path.exists():
                    logger.debug(f"Resource {resource_path} exists")
                    resource_paths.add(resource_path)
                else:
                    logger.warning(f"Resource {resource_path} does NOT exist, review directory contents or source in {md_file_path}")

            # If we have resource names to check, make sure they appear in the content.
            for resource_name in resource_names:
                if f"{{< img name=\"{resource_name}\"" in file_contents:
                    logger.debug(f"Resource {resource_name} present in front matter and referenced in file content")
                else:
                    logger.warning(f"A resource named {resource_name} was defined in {md_file_path}, but didn't seem to be referenced as an image in the content")

            # We have a list of resources. For each resource, get the contents of the directory
            # it lives in, flattened into a set. We'll end up with a list that _should_ match the
            # defined resource 'src's in the YAML.
            resources_in_fs = set()
            for resource_path in resource_paths:
                parent_path = resource_path.parent
                for on_disk_path in parent_path.glob('**/*'):
                    resources_in_fs.add(on_disk_path)

            resource_diff = resources_in_fs ^ resource_paths
            resource_diff = resource_diff - set([md_file_path])

            if resource_diff:
                logger.warning(f"Mismatch between filesystem and resources in content: {resource_diff}")



if __name__ == "__main__":
    _main()
