import os
import json
import shutil
import argparse

def load_metadata(meta_path):
    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    alias_map = {}
    for real_name, aliases in data.items():
        alias_map[real_name.lower()] = real_name
        for alias in aliases:
            alias_map[alias.lower()] = real_name
    return data, alias_map


def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def find_best_match(filename, alias_map):
    filename_lower = filename.lower()
    candidates = [alias for alias in alias_map.keys() if alias in filename_lower]
    if not candidates:
        return None
    return max(candidates, key=len)  # longest match


def resolve_real_author(match, alias_map, metadata):
    real_name = alias_map[match]
    aliases = metadata.get(real_name, [])
    first_alias = aliases[0] if aliases else real_name
    folder_name = f"{real_name} ({first_alias})"
    return real_name, folder_name


def move_zip(src_zip, dst_folder):
    base = os.path.basename(src_zip)
    name, ext = os.path.splitext(base)
    target = os.path.join(dst_folder, base)
    counter = 2

    while os.path.exists(target):
        target = os.path.join(dst_folder, f"{name} ({counter}){ext}")
        counter += 1

    shutil.move(src_zip, target)


def organize(src_dir, dst_dir, meta_path):
    metadata, alias_map = load_metadata(meta_path)
    ensure_folder(dst_dir)
    unsorted_dir = os.path.join(dst_dir, "Unsorted")
    ensure_folder(unsorted_dir)

    for file in os.listdir(src_dir):
        if not file.lower().endswith(".zip"):
            continue

        zip_path = os.path.join(src_dir, file)
        match = find_best_match(file, alias_map)

        if match:
            real_name, folder_name = resolve_real_author(match, alias_map, metadata)
            author_dir = os.path.join(dst_dir, folder_name)
            ensure_folder(author_dir)
            print(f"[MATCH] {file} → {folder_name}")
            move_zip(zip_path, author_dir)
        else:
            print(f"[UNSORTED] {file}")
            move_zip(zip_path, unsorted_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="Path to folder containing ZIP files")
    parser.add_argument("--dst", required=True, help="Path to Authors folder")
    parser.add_argument("--meta", required=True, help="Path to metadata.json")
    args = parser.parse_args()

    organize(args.src, args.dst, args.meta)
