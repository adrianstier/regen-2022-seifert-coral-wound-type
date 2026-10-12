"""Refine the completed inventory without making further remote requests."""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'image_archive_inventory_2026-10-12'
summaries = []
for filename, size_field in [('drive_files.csv', 'size'), ('nas_files.csv', 'bytes')]:
    with (OUT / filename).open(newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    for row in rows:
        path = row['relative_path'].lower()
        if 'island experiment' in path:
            row['category'] = 'other_experiment_island'
        elif row['extension'] == '.heic':
            row['category'] = 'source_image_candidate'
    with (OUT / filename).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    groups = defaultdict(list)
    for row in rows:
        groups[(row['project'], row['category'])].append(row)
    for (project, category), group in groups.items():
        checksums = {row.get('md5Checksum') for row in group if row.get('md5Checksum')}
        summaries.append({
            'inventory': filename, 'project': project, 'category': category,
            'files': len(group), 'bytes': sum(int(row.get(size_field) or 0) for row in group),
            'extensions': dict(Counter(row['extension'] for row in group)),
            'unique_available_drive_md5': len(checksums) if filename == 'drive_files.csv' else None,
        })
    if filename == 'drive_files.csv':
        duplicates = defaultdict(list)
        for row in rows:
            if row.get('md5Checksum'):
                duplicates[row['md5Checksum']].append({
                    'id': row['id'], 'project': row['project'],
                    'relative_path': row['relative_path'], 'bytes': int(row.get('size') or 0),
                })
        (OUT / 'drive_duplicate_checksums.json').write_text(json.dumps(
            {key: group for key, group in duplicates.items() if len(group) > 1}, indent=2))
old = json.loads((OUT / 'summary.json').read_text())
old['summary'] = summaries
old['classification_notes'] = [
    'HEIC files are image candidates; Island experiment and A pulchra are outside manuscript scope.',
    'Source-image candidates include native files and exports; counts are not unique photographs.',
    'Available Drive MD5s identify exact binary duplicates only, not alternate exports of one image.',
    'Size comparisons are limited to literal matching paths and do not establish checksum identity.',
]
(OUT / 'summary.json').write_text(json.dumps(old, indent=2))
print(json.dumps(summaries, indent=2))
