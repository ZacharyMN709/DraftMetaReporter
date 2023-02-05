def clean_card_tier(card_tier_data: dict) -> dict:
    return {
        'Card': card_tier_data['name'],
        'Tier': card_tier_data['tier'],
        'Sideboard': card_tier_data['flags']['synergy'],
        'Synergy': card_tier_data['flags']['synergy'],
        'Buildaround': card_tier_data['flags']['buildaround'],
        'Comment': card_tier_data['comment'],
    }
