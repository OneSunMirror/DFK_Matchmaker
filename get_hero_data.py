from asyncio.format_helpers import _format_callback_source
from web3 import Web3  
import numpy as np
import requests
ABI = ABI = """
            [
                {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},
                {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},
                {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"uint256","name":"heroId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"summonerId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"assistantId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"statGenes","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"visualGenes","type":"uint256"}],"name":"HeroSummoned","type":"event"},
                {"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},
                {"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},
                {"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},
                {"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},
                {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},
                {"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},
                {"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
                {"inputs":[],"name":"HERO_MODERATOR_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
                {"inputs":[],"name":"MINTER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
                {"inputs":[],"name":"MODERATOR_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
                {"inputs":[],"name":"PAUSER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"uint256","name":"_statGenes","type":"uint256"},{"internalType":"uint256","name":"_visualGenes","type":"uint256"},
                {"internalType":"enum IHeroTypes.Rarity","name":"_rarity","type":"uint8"},
                {"internalType":"bool","name":"_shiny","type":"bool"},{"components":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"summonerId","type":"uint256"},{"internalType":"uint256","name":"assistantId","type":"uint256"},{"internalType":"uint16","name":"generation","type":"uint16"},{"internalType":"uint256","name":"createdBlock","type":"uint256"},{"internalType":"uint256","name":"heroId","type":"uint256"},{"internalType":"uint8","name":"summonerTears","type":"uint8"},{"internalType":"uint8","name":"assistantTears","type":"uint8"},{"internalType":"address","name":"bonusItem","type":"address"},{"internalType":"uint32","name":"maxSummons","type":"uint32"},{"internalType":"uint32","name":"firstName","type":"uint32"},{"internalType":"uint32","name":"lastName","type":"uint32"},{"internalType":"uint8","name":"shinyStyle","type":"uint8"}],"internalType":"struct ICrystalTypes.HeroCrystal","name":"_crystal","type":"tuple"}],"name":"createHero","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"getHero","outputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"components":[{"internalType":"uint256","name":"summonedTime","type":"uint256"},{"internalType":"uint256","name":"nextSummonTime","type":"uint256"},{"internalType":"uint256","name":"summonerId","type":"uint256"},{"internalType":"uint256","name":"assistantId","type":"uint256"},{"internalType":"uint32","name":"summons","type":"uint32"},{"internalType":"uint32","name":"maxSummons","type":"uint32"}],"internalType":"struct IHeroTypes.SummoningInfo","name":"summoningInfo","type":"tuple"},{"components":[{"internalType":"uint256","name":"statGenes","type":"uint256"},{"internalType":"uint256","name":"visualGenes","type":"uint256"},{"internalType":"enum IHeroTypes.Rarity","name":"rarity","type":"uint8"},{"internalType":"bool","name":"shiny","type":"bool"},{"internalType":"uint16","name":"generation","type":"uint16"},{"internalType":"uint32","name":"firstName","type":"uint32"},{"internalType":"uint32","name":"lastName","type":"uint32"},{"internalType":"uint8","name":"shinyStyle","type":"uint8"},{"internalType":"uint8","name":"class","type":"uint8"},{"internalType":"uint8","name":"subClass","type":"uint8"}],"internalType":"struct IHeroTypes.HeroInfo","name":"info","type":"tuple"},{"components":[{"internalType":"uint256","name":"staminaFullAt","type":"uint256"},{"internalType":"uint256","name":"hpFullAt","type":"uint256"},{"internalType":"uint256","name":"mpFullAt","type":"uint256"},{"internalType":"uint16","name":"level","type":"uint16"},{"internalType":"uint64","name":"xp","type":"uint64"},{"internalType":"address","name":"currentQuest","type":"address"},{"internalType":"uint8","name":"sp","type":"uint8"},{"internalType":"enum IHeroTypes.HeroStatus","name":"status","type":"uint8"}],"internalType":"struct IHeroTypes.HeroState","name":"state","type":"tuple"},{"components":[{"internalType":"uint16","name":"strength","type":"uint16"},{"internalType":"uint16","name":"intelligence","type":"uint16"},{"internalType":"uint16","name":"wisdom","type":"uint16"},{"internalType":"uint16","name":"luck","type":"uint16"},{"internalType":"uint16","name":"agility","type":"uint16"},{"internalType":"uint16","name":"vitality","type":"uint16"},{"internalType":"uint16","name":"endurance","type":"uint16"},{"internalType":"uint16","name":"dexterity","type":"uint16"},{"internalType":"uint16","name":"hp","type":"uint16"},{"internalType":"uint16","name":"mp","type":"uint16"},{"internalType":"uint16","name":"stamina","type":"uint16"}],"internalType":"struct IHeroTypes.HeroStats","name":"stats","type":"tuple"},{"components":[{"internalType":"uint16","name":"strength","type":"uint16"},{"internalType":"uint16","name":"intelligence","type":"uint16"},{"internalType":"uint16","name":"wisdom","type":"uint16"},{"internalType":"uint16","name":"luck","type":"uint16"},{"internalType":"uint16","name":"agility","type":"uint16"},{"internalType":"uint16","name":"vitality","type":"uint16"},{"internalType":"uint16","name":"endurance","type":"uint16"},{"internalType":"uint16","name":"dexterity","type":"uint16"},{"internalType":"uint16","name":"hpSm","type":"uint16"},{"internalType":"uint16","name":"hpRg","type":"uint16"},{"internalType":"uint16","name":"hpLg","type":"uint16"},{"internalType":"uint16","name":"mpSm","type":"uint16"},{"internalType":"uint16","name":"mpRg","type":"uint16"},{"internalType":"uint16","name":"mpLg","type":"uint16"}],"internalType":"struct IHeroTypes.HeroStatGrowth","name":"primaryStatGrowth","type":"tuple"},{"components":[{"internalType":"uint16","name":"strength","type":"uint16"},{"internalType":"uint16","name":"intelligence","type":"uint16"},{"internalType":"uint16","name":"wisdom","type":"uint16"},{"internalType":"uint16","name":"luck","type":"uint16"},{"internalType":"uint16","name":"agility","type":"uint16"},{"internalType":"uint16","name":"vitality","type":"uint16"},{"internalType":"uint16","name":"endurance","type":"uint16"},{"internalType":"uint16","name":"dexterity","type":"uint16"},{"internalType":"uint16","name":"hpSm","type":"uint16"},{"internalType":"uint16","name":"hpRg","type":"uint16"},{"internalType":"uint16","name":"hpLg","type":"uint16"},{"internalType":"uint16","name":"mpSm","type":"uint16"},{"internalType":"uint16","name":"mpRg","type":"uint16"},{"internalType":"uint16","name":"mpLg","type":"uint16"}],"internalType":"struct IHeroTypes.HeroStatGrowth","name":"secondaryStatGrowth","type":"tuple"},{"components":[{"internalType":"uint16","name":"mining","type":"uint16"},{"internalType":"uint16","name":"gardening","type":"uint16"},{"internalType":"uint16","name":"foraging","type":"uint16"},{"internalType":"uint16","name":"fishing","type":"uint16"}],"internalType":"struct IHeroTypes.HeroProfessions","name":"professions","type":"tuple"}],"internalType":"struct IHeroTypes.Hero","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getRoleMember","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleMemberCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"getUserHeroes","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"string","name":"_url","type":"string"},{"internalType":"address","name":"_statScienceAddress","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"string","name":"baseTokenURI","type":"string"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
                {"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"address","name":"_statScienceAddress","type":"address"}],"name":"setStatScienceAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
                {"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},
                {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
                {"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"components":[{"internalType":"uint256","name":"summonedTime","type":"uint256"},{"internalType":"uint256","name":"nextSummonTime","type":"uint256"},{"internalType":"uint256","name":"summonerId","type":"uint256"},{"internalType":"uint256","name":"assistantId","type":"uint256"},{"internalType":"uint32","name":"summons","type":"uint32"},{"internalType":"uint32","name":"maxSummons","type":"uint32"}],"internalType":"struct IHeroTypes.SummoningInfo","name":"summoningInfo","type":"tuple"},{"components":[{"internalType":"uint256","name":"statGenes","type":"uint256"},{"internalType":"uint256","name":"visualGenes","type":"uint256"},{"internalType":"enum IHeroTypes.Rarity","name":"rarity","type":"uint8"},{"internalType":"bool","name":"shiny","type":"bool"},{"internalType":"uint16","name":"generation","type":"uint16"},{"internalType":"uint32","name":"firstName","type":"uint32"},{"internalType":"uint32","name":"lastName","type":"uint32"},{"internalType":"uint8","name":"shinyStyle","type":"uint8"},{"internalType":"uint8","name":"class","type":"uint8"},{"internalType":"uint8","name":"subClass","type":"uint8"}],"internalType":"struct IHeroTypes.HeroInfo","name":"info","type":"tuple"},{"components":[{"internalType":"uint256","name":"staminaFullAt","type":"uint256"},{"internalType":"uint256","name":"hpFullAt","type":"uint256"},{"internalType":"uint256","name":"mpFullAt","type":"uint256"},{"internalType":"uint16","name":"level","type":"uint16"},{"internalType":"uint64","name":"xp","type":"uint64"},{"internalType":"address","name":"currentQuest","type":"address"},{"internalType":"uint8","name":"sp","type":"uint8"},{"internalType":"enum IHeroTypes.HeroStatus","name":"status","type":"uint8"}],"internalType":"struct IHeroTypes.HeroState","name":"state","type":"tuple"},{"components":[{"internalType":"uint16","name":"strength","type":"uint16"},{"internalType":"uint16","name":"intelligence","type":"uint16"},{"internalType":"uint16","name":"wisdom","type":"uint16"},{"internalType":"uint16","name":"luck","type":"uint16"},{"internalType":"uint16","name":"agility","type":"uint16"},{"internalType":"uint16","name":"vitality","type":"uint16"},{"internalType":"uint16","name":"endurance","type":"uint16"},{"internalType":"uint16","name":"dexterity","type":"uint16"},{"internalType":"uint16","name":"hp","type":"uint16"},{"internalType":"uint16","name":"mp","type":"uint16"},{"internalType":"uint16","name":"stamina","type":"uint16"}],"internalType":"struct IHeroTypes.HeroStats","name":"stats","type":"tuple"},{"components":[{"internalType":"uint16","name":"strength","type":"uint16"},{"internalType":"uint16","name":"intelligence","type":"uint16"},{"internalType":"uint16","name":"wisdom","type":"uint16"},{"internalType":"uint16","name":"luck","type":"uint16"},{"internalType":"uint16","name":"agility","type":"uint16"},{"internalType":"uint16","name":"vitality","type":"uint16"},{"internalType":"uint16","name":"endurance","type":"uint16"},{"internalType":"uint16","name":"dexterity","type":"uint16"},{"internalType":"uint16","name":"hpSm","type":"uint16"},{"internalType":"uint16","name":"hpRg","type":"uint16"},{"internalType":"uint16","name":"hpLg","type":"uint16"},{"internalType":"uint16","name":"mpSm","type":"uint16"},{"internalType":"uint16","name":"mpRg","type":"uint16"},{"internalType":"uint16","name":"mpLg","type":"uint16"}],"internalType":"struct IHeroTypes.HeroStatGrowth","name":"primaryStatGrowth","type":"tuple"},{"components":[{"internalType":"uint16","name":"strength","type":"uint16"},{"internalType":"uint16","name":"intelligence","type":"uint16"},{"internalType":"uint16","name":"wisdom","type":"uint16"},{"internalType":"uint16","name":"luck","type":"uint16"},{"internalType":"uint16","name":"agility","type":"uint16"},{"internalType":"uint16","name":"vitality","type":"uint16"},{"internalType":"uint16","name":"endurance","type":"uint16"},{"internalType":"uint16","name":"dexterity","type":"uint16"},{"internalType":"uint16","name":"hpSm","type":"uint16"},{"internalType":"uint16","name":"hpRg","type":"uint16"},{"internalType":"uint16","name":"hpLg","type":"uint16"},{"internalType":"uint16","name":"mpSm","type":"uint16"},{"internalType":"uint16","name":"mpRg","type":"uint16"},{"internalType":"uint16","name":"mpLg","type":"uint16"}],"internalType":"struct IHeroTypes.HeroStatGrowth","name":"secondaryStatGrowth","type":"tuple"},{"components":[{"internalType":"uint16","name":"mining","type":"uint16"},{"internalType":"uint16","name":"gardening","type":"uint16"},{"internalType":"uint16","name":"foraging","type":"uint16"},{"internalType":"uint16","name":"fishing","type":"uint16"}],"internalType":"struct IHeroTypes.HeroProfessions","name":"professions","type":"tuple"}],"internalType":"struct IHeroTypes.Hero","name":"_hero","type":"tuple"}],"name":"updateHero","outputs":[],"stateMutability":"nonpayable","type":"function"},
                {"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"userHeroes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}
            ]
             """
HERO_CONTRACT = '0x5f753dcdf9b1ad9aabc1346614d1f4746fd6ce5c'
rpc_add = "https://api.harmony.one/"



"source https://github.com/0rtis/dfk/blob/master/hero/..."

rarity = {
    0: "Common",
    1: "Uncommon",
    2: "Rare",
    3: "Legendary",
    4: "Mythic",
}

_class = {
    0: "Warrior",
    1: "Knight",
    2: "Thief",
    3: "Archer",
    4: "Priest",
    5: "Wizard",
    6: "Monk",
    7: "Pirate",
    8: "Berserker",
    9: "Seer",
    16: "Paladin",
    17: "DarkKnight",
    18: "Summoner",
    19: "Ninja",
    24: "Dragoon",
    25: "Sage",
    20: "Shapeshifter (tbc)",
    28: "DreadKnight"
}

_ability_gene = {
    0: "Basic1",
    1: "Basic2",
    2: "Basic3",
    3: "Basic4",
    4: "Basic5",
    5: "Basic6",
    6: "Basic7",
    7: "Basic8",
    8: "Basic9",
    9: "Basic10",
    16: "Advanced1",
    17: "Advanced2",
    18: "Advanced3",
    19: "Advanced4",
    20: "Advanced5 (tbc)",
    24: "Elite1",
    25: "Elite2",
    28: "Transcendant1"
}

upgrade_gene = {
    0: 16,
    1: 16,
    2: 17,
    3: 17,
    4: 18,
    5: 18,
    6: 19,
    7: 19,
    8: 20,
    9: 20,
    16: 24,
    17: 24,
    18: 25,
    19: 25,
    20: 20,
    24: 28,
    25: 28,
    28: 28
}

def upgrade_chances(i):
    if i in range(0,20): 
        return 0.25
    if i in range(24,26): 
        return 0.125
    if i == 28: 
        return 0
    return 0 

complement_gene = {
    0: 1,
    1: 0,
    2: 3,
    3: 2,
    4: 5,
    5: 4,
    6: 7,
    7: 6,
    8: 9,
    9: 8,
    16: 17,
    17: 16,
    18: 19,
    19: 18,
    20: 20,
    24: 25,
    25: 24,
    28: 28
}
professions = {
    0: 'Mining',
    2: 'Gardening',
    4: 'Fishing',
    6: 'Foraging',
}

hero_rarity = {
    0: "Common",
    1: "Uncommon",
    2: "Rare",
    3: "Legendary",
    4: "Mythic",
}

rarity_prob = [[58.3, 27, 12.5, 2.0, 0.2],
[53.7, 28.4, 13.8, 3.1, 1.0], 
[49.2, 29.8, 15, 4.3, 1.9], 
[44.6, 31.1, 16.3, 5.4, 2.7],[40, 32.5, 17.5, 6.5, 3.5]
]
    

stats = {
    0: 'Strength',
    2: 'Agility',
    4: 'Intelligence',
    6: 'Wisdom',
    8: 'Luck',
    10: 'Vitality',
    12: 'Endurance',
    14: 'Dexterity'
}

scope_of_genes = [0,1,2,3,4,5,6,7,8] 
'eventually this can be expanded to cover all genes'

muteable_genes = [0,1,3,4,5,6]

_gene_types = {
    0: 'D',
    1: 'R1',
    2: 'R2',
    3: 'R3'
}

stat_traits = {
    0: 'Class',
    1: 'SubClass',
    2: 'Profession',
    3: 'Passive1',
    4: 'Passive2',
    5: 'Active1',
    6: 'Active2',
    7: 'StatBoost1',
    8: 'StatBoost2',
    9: 'statsUnknown1',
    10: 'element',
    11: 'statsUnknown2'
}

SCOPE_OF_TRAITS_COUNT = 9

gene_encoding = {
    0: _class,
    1: _class,
    2: professions,
    3: _ability_gene,
    4: _ability_gene,
    5: _ability_gene,
    6: _ability_gene,
    7: stats,
    8: stats,
}
ALPHABET = '123456789abcdefghijkmnopqrstuvwx'
def __genesToKai(genes):
    BASE = len(ALPHABET)
    buf = ''
    while genes >= BASE:
        mod = int(genes % BASE)
        buf = ALPHABET[int(mod)] + buf
        genes = (genes - mod) // BASE

    # Add the last 4 (finally).
    buf = ALPHABET[int(genes)] + buf

    # Pad with leading 1s.
    buf = buf.rjust(48, '1')

    return ' '.join(buf[i:i + 4] for i in range(0, len(buf), 4))

def genes2traits(genes):
    traits = []

    stat_raw_kai = "".join(__genesToKai(genes).split(' '))
    for ki in range(0, len(stat_raw_kai)):
        kai = stat_raw_kai[ki]
        value_num = __kai2dec(kai)
        traits.append(value_num)

    assert len(traits) == 48
    arranged_traits = [[], [], [], []]
    for i in range(0, 12):
        index = i << 2
        for j in range(0, len(arranged_traits)):
            arranged_traits[j].append(traits[index + j])

    arranged_traits.reverse()
    return arranged_traits

def __kai2dec(kai):
    return ALPHABET.index(kai)

def get_contract(hero_id, rpc_address):
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_address))   
        contract_address = Web3.toChecksumAddress(HERO_CONTRACT)
        contract = w3.eth.contract(contract_address, abi=ABI)
        hero_contract = contract.functions.getHero(hero_id).call() 
                 
        return hero_contract
    except Exception as inst:
        return None
     

def get_ability_gene(group):
    return [_ability_gene.get(group[5]), _ability_gene.get(group[6]),_ability_gene.get(group[3]),_ability_gene.get(group[4])]

#contract = get_contract(12469,rpc_add) 
#genes = contract[2][0]

'gene_prob array of probabilities to be dominate before mutation for all possible traits:'  

def get_gene_prob(hero_contract):
    raw_genes = hero_contract[2][0]
    return calc_prob(raw_genes)

def get_gene_prob_graphql(id):
    r = requests.post(graphql, json={'query': HERO_QUERY % (id)}).json()['data']['hero']
    #print(r)
    if (r is None):
        return None, None, None
    return calc_prob(int(r['statGenes']))

HERO_QUERY = """
query {
  hero(id: %d) {
    statGenes
    assistantId {numberId}
    summonerId {numberId}
    mainClass
    level
    generation
    rarity
    maxSummons
    summons
  }    
}

"""
graphql = 'https://defi-kingdoms-community-api-gateway-co06z8vi.uc.gateway.dev/graphql'



def get_other_hero_data_graphql(id):
    hero_details ={}
    r = requests.post(graphql, json={'query': HERO_QUERY % (id)}).json()['data']['hero']
    hero_details['summonerId'] = r['summonerId']['numberId']
    hero_details['assistantId'] = r['assistantId']['numberId']
    hero_details['primary_Class'] = r['mainClass']
    hero_details['level'] = r['level']
    hero_details['summons'] = r['summons']
    hero_details['maxsummons'] = r['maxSummons']
    hero_details['generation'] = r['generation']
    hero_details['rarity'] = hero_rarity[r['rarity']]
    hero_details['rarity_num'] = r['rarity']
    Desc = hero_details['rarity'] + " " + hero_details['primary_Class'] + ", Gen " + str(hero_details['generation']) + ", Level " + str(hero_details['level']) + ", " + str(hero_details['maxsummons'] - hero_details['summons']) + "/" + str(hero_details['maxsummons']) + " Summons"
    return hero_details, Desc

def get_other_hero_data(hero_contract):
    #print(hero_contract)
    hero_details ={}
    hero_details['summonerId'] = hero_contract[1][2]
    hero_details['assistantId'] = hero_contract[1][3]
    hero_details['primary_Class'] = _class[hero_contract[2][8]]
    hero_details['level'] = hero_contract[3][3]
    hero_details['summons'] = hero_contract[1][4]
    hero_details['maxsummons'] = hero_contract[1][5]
    hero_details['generation'] = hero_contract[2][4]
    hero_details['rarity'] = hero_rarity[hero_contract[2][2]]
    hero_details['rarity_num'] = hero_contract[2][2]
    Desc = hero_details['rarity'] + " " + hero_details['primary_Class'] + ", Gen " + str(hero_details['generation']) + ", Level " + str(hero_details['level']) + ", " + str(hero_details['maxsummons'] - hero_details['summons']) + "/" + str(hero_details['maxsummons']) + " Summons"
    return hero_details, Desc
    
def check_same_parents(a1, a2, a3, b1, b2, b3):
    txt_1 = ["Hero 1", "Hero 1's Parent 1", "Hero 1 Parent 2"]
    txt_2 = ["Hero 2", "Hero 2's Parent 1", "Hero 2 Parent 2"]
    h1 =[a1, a2, a3]
    h2 =[b1, b2, b3]
    for i in range(3):
        for j in range(3):
            if (h1[i] == h2[j]) and (int(h1[i])!=0):
                return False, txt_1[i] + " and " + str(txt_2[j]) + " are the same (" + str(h1[i]) + ")"
    return True, ""

def calc_rarity(r1, r2):
    prob = []
    for i in range(5):
        dict = {
            'name' : hero_rarity[i],
            'chance' : round((rarity_prob[r1][i] + rarity_prob[r2][i])/2, 2)       
        }
        prob.append(dict)
    return prob

def calc_prob(raw_genes):
    p_genes = np.zeros([11,32])
    swap_p = [0.75, 0.1875, 0.046875, 0.015625]
    genes = genes2traits(raw_genes)
    #print(genes)
    dict_gene_all = []
    dict_gene = {}
    c = len(scope_of_genes)
    filter_string_l = ['0'] * (33 * 4 * c)
    for i in range(11):
        for j in range(4):
            dict_gene['type'] = stat_traits[i]
            if i in scope_of_genes:
                dict_gene[_gene_types[j]] = gene_encoding[i][genes[j][i]]
                filter_string_l[((j*c*33) +(i*33) + genes[j][i])] = '1'
            p_genes[i][genes[j][i]] += swap_p[j]
        if i in scope_of_genes:
            dict_gene_all.append(dict_gene)
            dict_gene = {}
    filter_string = int(''.join(map(str,filter_string_l)),2)
    #print(filter_string)
    return p_genes, dict_gene_all, filter_string            
    
#print(get_gene_prob(contract))

def calc_likelyhood(gene1, gene2):
    new_genes = np.zeros([11,32])
    dict_result = []
    for i in scope_of_genes:
        for j in range(32):
            if (i in muteable_genes) and (j in complement_gene):
                upgrade_p = (gene1[i][j] * gene2[i][complement_gene[j]])  * upgrade_chances(j)
                new_genes[i][upgrade_gene[j]] += upgrade_p
                new_genes[i][j] -= upgrade_p *0.5
                new_genes[i][complement_gene[j]] -= upgrade_p * 0.5
            new_genes[i][j] += gene1[i][j] * 0.5 +  gene2[i][j] * 0.5 
    prim = {}
    sub = {}
    pass1 ={} 
    pass2 ={}
    act1 ={}
    act2 ={}
    prof = {} 
    stat1 = {}
    stat2 = {}  
    for j in complement_gene:
        prim[_class[j]] = round(new_genes[0,j]*100,2) 
        sub[_class[j]] = round(new_genes[1,j]*100,2) 
        pass1[_ability_gene[j]] = round(new_genes[3,j]*100,2)
        pass2[_ability_gene[j]] = round(new_genes[4,j]*100,2)
        act1[_ability_gene[j]] = round(new_genes[5,j]*100,2) 
        act2[_ability_gene[j]] = round(new_genes[6,j]*100,2)
    for j in professions:
        prof[professions[j]] = round(new_genes[2,j]*100,2)
    for j in stats:
        stat1[stats[j]] = round(new_genes[7,j]*100,2)
        stat2[stats[j]] = round(new_genes[8,j]*100,2)

    dict_result.append([{'name' : x, 'chance' : y} for x,y in sorted(prim.items(), key=lambda item: item[1], reverse=True) if y!=0.0])
    dict_result.append([{'name' : x, 'chance' : y} for x,y in sorted(sub.items(), key=lambda item: item[1], reverse=True) if y!=0.0])
    dict_result.append([{'name' : x, 'chance' : y}for x,y in sorted(pass1.items(), key=lambda item: item[1], reverse=True) if y!=0.0])
    dict_result.append([{'name' : x, 'chance' : y} for x,y in sorted(pass2.items(), key=lambda item: item[1], reverse=True) if y!=0.0])
    dict_result.append([{'name' : x, 'chance' : y} for x,y in sorted(act1.items(), key=lambda item: item[1], reverse=True) if y!=0.0])
    dict_result.append([{'name' : x, 'chance' : y} for x,y in sorted(act2.items(), key=lambda item: item[1], reverse=True) if y!=0.0])
    dict_result.append([{'name' : x, 'chance' : y}for x,y in sorted(prof.items(), key=lambda item: item[1], reverse=True) if y!=0.0])
    dict_result.append([{'name' : x, 'chance' : y}for x,y in sorted(stat1.items(), key=lambda item: item[1], reverse=True) if y!=0.0])
    dict_result.append([{'name' : x, 'chance' : y}for x,y in sorted(stat2.items(), key=lambda item: item[1], reverse=True) if y!=0.0])
    #print(dict_result)
    return  dict_result

def calc_likelyhood_adv(gene1, gene2):
    new_genes = np.zeros([11,32])
    for i in scope_of_genes:
        for j in range(32):
            if (i in muteable_genes) and (j in complement_gene):
                upgrade_p = (gene1[i][j] * gene2[i][complement_gene[j]])  * upgrade_chances(j)
                new_genes[i][upgrade_gene[j]] += upgrade_p
                new_genes[i][j] -= upgrade_p *0.5
                new_genes[i][complement_gene[j]] -= upgrade_p * 0.5
            new_genes[i][j] += gene1[i][j] * 0.5 +  gene2[i][j] * 0.5 
    dict_lists = [[] for i in range(SCOPE_OF_TRAITS_COUNT)]
    #print(dict_lists)
    for j in range(32):
        for i in scope_of_genes:
            if j in gene_encoding[i]:
                likelihood = round(new_genes[i,j]*100,2)
                if likelihood > 0:
                    mutated = round(100*(new_genes[i,j] - ((gene1[i][j] + gene2[i][j])) * 0.5),2)
                    dict_lists[i].append({'name' : gene_encoding[i][j], 'chance' : likelihood, 'mutated' : mutated})
    #print(dict_lists)
    return dict_lists

def get_users_heroes(user_address, rpc_address):
    w3 = Web3(Web3.HTTPProvider(rpc_address))

    contract_address = Web3.toChecksumAddress(HERO_CONTRACT)
    contract = w3.eth.contract(contract_address, abi=ABI)

    return contract.functions.getUserHeroes(Web3.toChecksumAddress(user_address)).call()


#gene_prob_2, gene_details_2 = get_gene_prob_graphql(123223)
#gene_prob_1, gene_details_1 = get_gene_prob_graphql(21223)
#summon_result = calc_likelyhood(gene_prob_1, gene_prob_2)
#summon_result = calc_likelyhood_adv(gene_prob_1, gene_prob_2)

#'print(get_contract(125261, rpc_add)[1][2:4])'

#print(get_other_hero_data_graphql(190639))

#print(get_other_hero_data(get_contract(12321, rpc_add)))