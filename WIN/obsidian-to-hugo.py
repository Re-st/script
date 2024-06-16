import os
import re
import argparse
from datetime import datetime
from obsidian_to_hugo import ObsidianToHugo

class CustomObsidianToHugo(ObsidianToHugo):
    def __init__(self, obsidian_vault_dir: str, hugo_content_dir: str, processors: list = None, filters: list = None, custom_processors: list = None):
        super().__init__(obsidian_vault_dir, hugo_content_dir)
        self.custom_processors = custom_processors

    def custom_rum(self) -> None:
        """
        Delete the hugo content directory and copy the obsidian vault to the
        hugo content directory, then process the content so that the wiki links
        are replaced with the hugo links.
        """
        self.clear_hugo_content_dir()
        self.copy_obsidian_vault_to_hugo_content_dir()
        self.process_content()
        self.custom_process_content()

    def custom_process_content(self) -> None:
        """
        Looping through all files in the hugo content directory and replace the
        wiki links of each matching file.
        """
        for root, dirs, files in os.walk(self.hugo_content_dir):
            for file in files:
                if file.endswith(".md"):
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = f.read()
                    # If the file matches any of the filters, delete it.
                    keep_file = True
                    for filter in self.filters:
                        if not filter(content, file):
                            os.remove(os.path.join(root, file))
                            keep_file = False
                            break
                    if not keep_file:
                        continue
                    path = os.path.join(root, file)
                    for processor in self.custom_processors:
                        # change path from hugo_content_dir to obsidian_vault_dir
                        path = path.replace(self.hugo_content_dir, self.obsidian_vault_dir)
                        content = processor(content, path)
                    with open(os.path.join(root, file), "w", encoding="utf-8") as f:
                        f.write(content)

def process_file(file_contents: str, file_path: str) -> str:
    # Extract metadata
    metadata_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL | re.MULTILINE)
    metadata_match = metadata_pattern.search(file_contents)

    metadata = ''
    title = ''
    date = ''
    draft = ''
    summary = ''
    urls_str = ''
    if metadata_match:
        metadata = metadata_match.group(1)
        file_contents = metadata_pattern.sub('', file_contents)

        # Remove URL field from metadata
        url_pattern = re.compile(r'(https?://[^\s]+)')
        urls = url_pattern.findall(metadata)
        urls_str = '\n'.join(urls) + '\n\n' if urls else ''
        metadata = url_pattern.sub('', metadata)

        # Extract title and date
        title_pattern = re.compile(r'^title(.*?)$', re.MULTILINE)
        date_pattern = re.compile(r'^date(.*?)$', re.MULTILINE)
        draft_pattern = re.compile(r'^draft(.*?)$', re.MULTILINE)
        summary_pattern = re.compile(r'^summary(.*?)$', re.MULTILINE)

        title_match = title_pattern.search(metadata)
        if title_match:
            title = title_match.group(1).split(':', 1)[-1].strip()
            metadata = title_pattern.sub('', metadata)

        date_match = date_pattern.search(metadata)
        if date_match:
            date = date_match.group(1).split(':', 1)[-1].strip()
            metadata = date_pattern.sub('', metadata)

        draft_match = draft_pattern.search(metadata)
        if draft_match:
            draft = draft_match.group(1).split(':', 1)[-1].strip()
            metadata = draft_pattern.sub('', metadata)

        summary_match = summary_pattern.search(metadata)
        if summary_match:
            summary = summary_match.group(1).split(':', 1)[-1].strip()
            metadata = summary_pattern.sub('', metadata)

    # Get title from file name if not in metadata
    if title == '':
        title = file_path.split(os.sep)[-1].replace('.md', '')
        print(title)

    if date == '':
        # Get modified date of Obsidian file
        file_stat = os.stat(file_path)
        # created_date = datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        date = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

    if not date.endswith(" +0900"):
        date += " +0900"

    if draft == '':
        draft = 'false'

    if summary == '':
        summary = title

    metadata = f"""title: {title}
date: {date}
draft: {draft}
summary: {summary}
""" + metadata

    if metadata[-1] != '\n':
        metadata += '\n'
    # \n\n...\n -> \n
    metadata = re.sub(r'\n\n+', '\n', metadata)
    # Return the processed file contents
    final_contents = f"---\n{metadata}---\n" + urls_str + file_contents
    return final_contents

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Obsidian vault to Hugo content.")
    parser.add_argument("-o", "--obsidian_vault_dir", required=True, help="Path to the Obsidian vault directory")
    parser.add_argument("-c", "--hugo_content_dir", required=True, help="Path to the Hugo content directory")

    args = parser.parse_args()

    obsidian_to_hugo = CustomObsidianToHugo(
        args.obsidian_vault_dir,
        args.hugo_content_dir,
        custom_processors=[process_file],
    )

    obsidian_to_hugo.custom_rum()
