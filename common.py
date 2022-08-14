from pathlib import Path

# paths = [
#     # in order of creation / more and more zoomed out
#     'DALL·E 2022-08-13 22.45.48 - A man and woman lie on a striped picnic blanket in the grass; photorealistic.png',
#     'DALL·E 2022-08-13 23.02.51 - Top-down view of two people lying on a picnic blanket in a park with a road to the left; photorealistic.png',
#     'DALL·E 2022-08-14 00.07.13 - Satellite view of a park next to a busy road and a pier; photorealistic.png',
#     'DALL·E 2022-08-14 00.45.51 - Satellite view of a pier area; photorealistic.png',
# ]

paths = sorted(filter(lambda p: not p.name.endswith('.zoomed.png'), Path('images').glob('*.png')))
