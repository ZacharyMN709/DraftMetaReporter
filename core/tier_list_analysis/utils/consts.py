TIER_LIST_ROOT = "https://www.17lands.com/tier_list/"


tier_to_rank = {
    "A+": 12,
    "A": 11,
    "A-": 10,
    "B+": 9,
    "B": 8,
    "B-": 7,
    "C+": 6,
    "C": 5,
    "C-": 4,
    "D+": 3,
    "D": 2,
    "D-": 1,
    "F": 0,
    "SB": None,
    "TBD": None
}


rank_to_tier = {v: k for k, v in tier_to_rank.items()}


range_map_vals = [
        (99, 100),
        (95, 99),
        (90, 95),
        (85, 90),
        (76, 85),
        (68, 76),
        (57, 68),
        (45, 57),
        (36, 45),
        (27, 36),
        (17, 27),
        (5, 17),
        (0, 5)
]
