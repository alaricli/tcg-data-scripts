import json
import unicodedata

from pokemontcgsdk import Card, RestClient

RestClient.configure('e04b950b-6e91-4c21-b820-06fd135d9b8a')

def map_rarity(rarity):
    rarity_mapping = {
        "Amazing Rare": "AMAZING",
        "Common": "COMMON",
        "LEGEND": "LEGEND",
        "Promo": "PROMO",
        "Rare": "RARE",
        "Rare ACE": "ACE_SPEC_RARE",
        "Rare BREAK": "RARE_BREAK",
        "Rare Holo": "RARE_HOLO",
        "Rare Holo EX": "RARE_HOLO_EX",
        "Rare Holo GX": "RARE_HOLO_GX",
        "Rare Holo LV.X": "RARE_HOLO_LVX",
        "Rare Holo Star": "SUPER_RARE",
        "Rare Holo V": "ULTRA_RARE",
        "Rare Holo VMAX": "ULTRA_RARE",
        "Rare Prime": "RARE_PRIME",
        "Rare Prism Star": "ULTRA_RARE",
        "Rare Rainbow": "RARE_RAINBOW",
        "Rare Secret": "SUPER_RARE",
        "Rare Shining": "SHINY_RARE",
        "Rare Shiny": "SHINY_RARE",
        "Rare Shiny GX": "SHINY_ULTRA_RARE",
        "Rare Ultra": "ULTRA_RARE",
        "Uncommon": "UNCOMMON",
    }
    return rarity_mapping.get(rarity, "UNKNOWN")

def map_subtypes(subtypes):
    subtype_mapping = {
        "BREAK": "BREAK",
        "Baby": "SPECIAL",
        "Basic": "BASIC",
        "EX": "EX",
        "GX": "GX",
        "Goldenrod Game Corner": "SPECIAL",
        "Item": "ITEM",
        "LEGEND": "LEGEND",
        "Level-Up": "LEVEL_UP",
        "MEGA": "MEGA",
        "Pokémon Tool": "TOOL",
        "Pokémon Tool F": "TOOL",
        "Rapid Strike": "SPECIAL",
        "Restored": "RESTORED",
        "Rocket's Secret Machine": "ROCKETS_SECRET_MACHINE",
        "Single Strike": "SPECIAL",
        "Special": "SPECIAL",
        "Stadium": "STADIUM",
        "Stage 1": "STAGE1",
        "Stage 2": "STAGE2",
        "Supporter": "SUPPORTER",
        "TAG TEAM": "TAG_TEAM",
        "Technical Machine": "TECHNICAL_MACHINE",
        "V": "V",
        "VMAX": "VMAX",
    }
    return [subtype_mapping.get(s, "UNKNOWN") for s in subtypes]

def transform_card(card):
    return {
        "name": card.name,
        "hp": int(card.hp) if card.hp else None,
        "retreatCost": card.convertedRetreatCost,
        "artist": card.artist,
        "regulationMark": card.regulationMark,
        "identifier": card.set.id + "-" + card.number,
        "cardNumber": int(card.number) if card.number else None,
        "nationalPokedexNumber": card.nationalPokedexNumbers[0] if card.nationalPokedexNumbers else None,
        "hasRuleBox": bool(card.rules),
        "hasAbility": bool(card.abilities),
        "ability": " ".join(f"{ability.name} {ability.text}" for ability in card.abilities) if card.abilities else None,
        "trainerCardText": card.rules[0] if card.rules else None,
        "rarity": map_rarity(card.rarity),
        "superType": unicodedata.normalize('NFKD', card.supertype).replace('é', 'e').upper(),
        "subTypes": map_subtypes(card.subtypes),
        "expansionId": card.set.id if card.set else None,
        "energyTypes": [t.upper() for t in card.types] if card.types else [],
        "attackEnergyTypes": list({e.upper() for attack in card.attacks for e in attack.cost}) if card.attacks else [],
        "weakness": [w.type.upper() for w in card.weaknesses] if card.weaknesses else [],
        "resistance": [r.type.upper() for r in card.resistances] if card.resistances else [],
        "rules": card.rules if card.rules else [],
        "cardImages": {
            "small": card.images.small if card.images else None,
            "large": card.images.large if card.images else None,
        },
        "legalities": card.legalities if card.legalities else {},
        "isMobile": False,
        "attacks": [
            {
                "name": attack.name,
                "text": attack.text,
                "cost": ",".join(c.upper() for c in attack.cost),
                "numericalEnergyCost": attack.convertedEnergyCost,
                "damage": attack.damage,
            } for attack in card.attacks
        ] if card.attacks else []
    }

def get_card(card_id):
  try:
    card = Card.find(card_id)
    return card
  except Exception as e:
    return f"An error occured: {e}"

if __name__ == "__main__":
  card_id = input("enter a card id, eg:'xy1-1': ")
  card = get_card(card_id)
  transformed_card = transform_card(card)
  card_json = json.dumps(transformed_card, default=lambda o: o.__dict__, indent=4)
  
  print(card_json)