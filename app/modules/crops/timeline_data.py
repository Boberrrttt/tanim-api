"""
Approximate growth cycles (day 1 = planting or field transplant).
Mirrors tanim-app/constants/crop-cycle.ts — keep in sync when editing.

See that file for literature references (IRRI, land-grant extension, FAO, UF-IFAS, etc.).
"""

CROP_TIMELINES: dict = {
    "default": {
        "total_days": 85,
        "planting_window_note": "Generic template — match days-to-maturity on your seed or transplant label.",
        "phases": [
            {"name": "Establishment", "day_start": 1, "day_end": 12, "description": "Germination and early root growth"},
            {"name": "Vegetative", "day_start": 13, "day_end": 38, "description": "Leaf and canopy development"},
            {"name": "Reproductive", "day_start": 39, "day_end": 58, "description": "Flowering and early fruit or grain set"},
            {"name": "Maturation", "day_start": 59, "day_end": 78, "description": "Sizing and ripening"},
            {"name": "Harvest", "day_start": 79, "day_end": 85, "description": "Ready to harvest"},
        ],
    },
    "corn": {
        "total_days": 105,
        "planting_window_note": "Sweet corn is often shorter (~60-100 d); field/grain hybrids often 100-120+ d - check RM on bag.",
        "phases": [
            {"name": "Emergence", "day_start": 1, "day_end": 14, "description": "Germination through early leaf stages (VE-V4)"},
            {"name": "Vegetative", "day_start": 15, "day_end": 58, "description": "Stalk and leaf growth until near tassel"},
            {"name": "Tassel & silk", "day_start": 59, "day_end": 78, "description": "Pollination window; critical for grain set"},
            {"name": "Grain fill", "day_start": 79, "day_end": 99, "description": "Kernel dough to dent; moisture still high"},
            {"name": "Maturity", "day_start": 100, "day_end": 105, "description": "Black layer / harvest moisture for grain corn"},
        ],
    },
    "eggplant": {
        "total_days": 72,
        "planting_window_note": "Cultivars range ~50-80 d after transplant; warm nights (>15C) help fruit set.",
        "phases": [
            {"name": "Establishment", "day_start": 1, "day_end": 12, "description": "Transplant shock recovery and rooting"},
            {"name": "Vegetative", "day_start": 13, "day_end": 32, "description": "Branching and canopy build"},
            {"name": "Flowering", "day_start": 33, "day_end": 48, "description": "Bloom and fruit set"},
            {"name": "Fruiting", "day_start": 49, "day_end": 63, "description": "Fruit enlargement"},
            {"name": "Harvest", "day_start": 64, "day_end": 72, "description": "Repeated picks as fruits reach market size"},
        ],
    },
    "tobacco": {
        "total_days": 110,
        "planting_window_note": "FAO cites ~90-120 d frost-free after transplant; follow local rules and varieties.",
        "phases": [
            {"name": "Establishment", "day_start": 1, "day_end": 20, "description": "Rooting after transplant"},
            {"name": "Vegetative", "day_start": 21, "day_end": 55, "description": "Rapid leaf expansion (grand growth)"},
            {"name": "Topping & suckering", "day_start": 56, "day_end": 80, "description": "Flower removal and sucker control"},
            {"name": "Ripening", "day_start": 81, "day_end": 100, "description": "Leaf color and body for curing type"},
            {"name": "Harvest", "day_start": 101, "day_end": 110, "description": "Priming or stalk harvest per local practice"},
        ],
    },
    "rice": {
        "total_days": 120,
        "planting_window_note": "IRRI: short types ~100-120 d, medium ~120-140 d, long 160+ from seeding/transplant - adjust for cultivar.",
        "phases": [
            {"name": "Establishment", "day_start": 1, "day_end": 30, "description": "Tillering and root system development"},
            {"name": "Vegetative", "day_start": 31, "day_end": 70, "description": "Active tillering; N management critical"},
            {"name": "Reproductive", "day_start": 71, "day_end": 100, "description": "Panicle initiation through heading"},
            {"name": "Ripening", "day_start": 101, "day_end": 115, "description": "Grain filling and moisture drop"},
            {"name": "Harvest", "day_start": 116, "day_end": 120, "description": "Combine or manual at target moisture"},
        ],
    },
    "tomato": {
        "total_days": 75,
        "planting_window_note": "Packet \"days to maturity\" is usually from transplant; early types ~65 d, late ~85 d.",
        "phases": [
            {"name": "Establishment", "day_start": 1, "day_end": 7, "description": "Transplant establishment"},
            {"name": "Vegetative", "day_start": 8, "day_end": 28, "description": "Vine and leaf growth"},
            {"name": "Flowering", "day_start": 29, "day_end": 50, "description": "Bloom and fruit set"},
            {"name": "Fruiting", "day_start": 51, "day_end": 68, "description": "Fruit development and sizing"},
            {"name": "Harvest", "day_start": 69, "day_end": 75, "description": "First picks; indeterminates keep producing"},
        ],
    },
    "sugarcane": {
        "total_days": 450,
        "planting_window_note": "FAO / regional guides: plant crop often 12-18 months (many areas ~15-16 mo optimum age).",
        "phases": [
            {"name": "Germination", "day_start": 1, "day_end": 60, "description": "Shoot emergence and early tillers"},
            {"name": "Tillering", "day_start": 61, "day_end": 150, "description": "Stool building; stand establishment"},
            {"name": "Grand growth", "day_start": 151, "day_end": 300, "description": "Rapid stalk elongation and dry matter"},
            {"name": "Ripening", "day_start": 301, "day_end": 390, "description": "Sucrose accumulation; avoid late drought stress"},
            {"name": "Harvest", "day_start": 391, "day_end": 450, "description": "Plant crop ~12-18 mo globally; ratoon resets cycle"},
        ],
    },
    "cabbage": {
        "total_days": 68,
        "planting_window_note": "Fast cultivars ~55-65 d from transplant; storage types run longer.",
        "phases": [
            {"name": "Establishment", "day_start": 1, "day_end": 12, "description": "Transplant rooting"},
            {"name": "Vegetative", "day_start": 13, "day_end": 35, "description": "Leaf frame before head"},
            {"name": "Heading", "day_start": 36, "day_end": 55, "description": "Head formation and firming"},
            {"name": "Maturation", "day_start": 56, "day_end": 63, "description": "Dense head; watch splitting in heat"},
            {"name": "Harvest", "day_start": 64, "day_end": 68, "description": "Cut when head is firm"},
        ],
    },
    "cotton": {
        "total_days": 165,
        "planting_window_note": "Industry guides cite ~150-180 d planting to harvest-ready; driven by DD60s and variety.",
        "phases": [
            {"name": "Stand", "day_start": 1, "day_end": 35, "description": "Emergence through early nodes"},
            {"name": "Squaring", "day_start": 36, "day_end": 75, "description": "Square formation and vegetative peak"},
            {"name": "Flowering", "day_start": 76, "day_end": 120, "description": "Bloom, boll set, heat-unit driven"},
            {"name": "Boll fill", "day_start": 121, "day_end": 155, "description": "Fiber and seed development"},
            {"name": "Harvest", "day_start": 156, "day_end": 165, "description": "Defoliate when most bolls open; ~150-180 d typical"},
        ],
    },
    "potato": {
        "total_days": 100,
        "planting_window_note": "Early varieties ~75-90 d; maincrop often 90-120 d - check your variety class.",
        "phases": [
            {"name": "Sprouting", "day_start": 1, "day_end": 20, "description": "Emergence and stolon setup"},
            {"name": "Vegetative", "day_start": 21, "day_end": 50, "description": "Canopy closure"},
            {"name": "Tuber initiation", "day_start": 51, "day_end": 70, "description": "Tuber set; critical moisture"},
            {"name": "Bulking", "day_start": 71, "day_end": 94, "description": "Tuber enlargement"},
            {"name": "Harvest", "day_start": 95, "day_end": 100, "description": "Vine senescence; skin set before dig"},
        ],
    },
}
