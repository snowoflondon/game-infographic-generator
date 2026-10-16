"""Compact platform labels for display without modifying researched metadata."""


def format_platforms(platforms: list[str]) -> str:
    """Group known families at their first occurrence; preserve unknown names."""
    families = {
        'PlayStation': {f'PlayStation {n}': str(n) for n in range(1, 6)},
        'Xbox': {'Xbox': '', 'Xbox 360': '360', 'Xbox One': 'One',
                 'Xbox Series X|S': 'Series X|S', 'Xbox Series X': 'Series X',
                 'Xbox Series S': 'Series S'},
        'Nintendo': {'Nintendo Switch': 'Switch', 'Nintendo Switch 2': 'Switch 2',
                     'Nintendo Wii': 'Wii', 'Nintendo Wii U': 'Wii U',
                     'Nintendo DS': 'DS', 'Nintendo 3DS': '3DS',
                     'Nintendo 64': '64', 'Nintendo GameCube': 'GameCube'},
    }
    groups: dict[str, list[str]] = {}
    for platform in platforms:
        family = next((name for name, members in families.items() if platform in members), None)
        key = 'Mobile' if platform in {'iOS', 'Android'} else family or platform
        values = groups.setdefault(key, [])
        if platform not in values:
            values.append(platform)
    labels = []
    for key, members in groups.items():
        if key == 'Mobile':
            labels.append('Mobile')
        elif key in families and len(members) > 1 and all(families[key].get(p) for p in members):
            labels.append(key + ' ' + ' & '.join(families[key][p] for p in members))
        else:
            labels.extend(members)
    return ' / '.join(labels)
