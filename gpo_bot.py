import discord
from discord import app_commands
from fuzzywuzzy import process
import re
import asyncio
from dotenv import load_dotenv
from webserver import keep_alive
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

GPO_TRADE_CHANNEL_ID = 1384570705772810330

items = {
    # Fruits
    "ito": 75,
    "paw": 50,
    "kage": 50,
    "gura": 100,
    "goro": 50,
    "yami": 50,
    "zushi": 70,
    "hie": 50,
    "suna": 80,
    "yuki": 90,
    "mera": 150,
    "magu": 600,
    "goru (gold)": 100,
    "moku (smoke)": 100,
    "pika": 3500,
    "kira": 100,
    "ope": 2000,
    "tori": 2500,
    "hito: daibutsu (budda)": 3250,
    "ryu: pteranodon (ptero)": 2500,
    "doku (venom)": 4200,
    "mochi": 6500,

    # Gamepass
    "legendary chest": 700,
    "mythical chest": 6000,
    "all seeing eye": 24500,
    "blo's ase": 35000,
    "chromatic ase": 52000,
    "sp reset": 5,
    "dark root": 10,
    "spirit colour essence": 150,
    "spare fruit bag": 100,
    "thriller ship": 300,
    "hoverboard": 600,
    "coffin boat": 1700,
    "striker boat": 1800,
    "golden hammer": 75,
    "devil fruit journal": 150,
    "karoo": 75,

    # Weapons
    "jitte": 200,
    "golden hook": 50,
    "bisento": 50,
    "gravity cane": 50,
    "moria's scissors": 50,
    "borj gauntlets": 150,
    "shusui": 100,
    "crab cutlass": 50,
    "golden pole": 50,
    "neptune's trident": 100,
    "black pitchfork": 50,
    "vera's whip": 50,
    "raiui": 50,
    "soul cane": 200,
    "vrael's pipe": 150,
    "sunken anchor": 1000,
    "boneshiver": 400,
    "roger's ace": 1000,
    "yoru": 5500,
    "kikoku": 10000,

    # Soul King
    "violin": 100,
    "soul king guitar": 2000,
    "soul king outfit": 75,
    "soul king hat": 150,
    "soul king shades": 100,
    "soul king scarf": 30000,

    # Accessories
    "musashi karuta": 25,
    "musashi hat": 25,
    "law's cape": 25,
    "law's outfit": 50,
    "law's hat": 25,
    "domingo's cape": 90,
    "domingo's outfit": 75,
    "domingo's shades": 150,
    "moria outfit": 25,
    "moria hat": 25,
    "moria necklace": 100,
    "batswarm": 600,
    "ryuma's scarf": 300,
    "tomoe's drums": 100,
    "radiant admiral's shades": 300,
    "radiant admiral's outfit": 150,
    "radiant admiral's cape": 200,

    # Seabeast/Kraken/Megalodon
    "sea serpent's core": 200,
    "kraken's core": 100,
    "kraken great sword": 600,
    "kraken armour": 600,
    "sea beast mask": 100,
    "sea beast armour": 50,
    "megalodon tooth": 50, # Указано 30-50, взял максимальное
    "megalodon armour": 150,
    "megalodon helmet": 400,
    "sunken helmet": 2500,
    "sunken armour": 700,

    # Roger/Hawkeye
    "roger's hat": 100,
    "roger's outfit": 450,
    "hawkeye's hat": 100,
    "hawkeye's outfit": 300,

    # Unobtainable
    "candy cane": 64000,
    "og santa hat": 3000,
    "flowers": 13000,
    "flamingo boat": 2500,
    "baal head": 1500,
    "baal cape": 90,
    "hollow fang": 200,
    "jester box": 600,
    "jester hat": 500,
    "jester scythe": 600,
    "jester's outfit": 35000,
    "elo hammer": 1200,
    "og cupid queen wings": 1700,
    "og cupid dress": 2500,
    "cupid's wand": 150,
    "cupid's battleaxe": 100,
    "inferno rocket blade": 300,
    "firework lancer": 300,
    "cupid headband": 150,
    "cupid boat": 50,
    "festival lancer": 300,
    "festival shield": 500,
    "firework rocket launcher": 50,
    "firework daggers": 50,
    "hollow greatsword": 75,
    "hollow halberd": 150,
    "resurrected baal head": 24000,
    "resurrected baal outfit": 300,
    "true baal guard": 8000,
    "iceborn rapier": 200,
    "iceborn blade": 200,
    "iceborn dagger": 100,
    "iceborn katana": 300,
    "stark guns": 1700,
    "coyote outfit": 6000,
    "world ender": 16000,

    # Toji
    "inverted spear of heaven (isoh)": 3250,
    "toji outfit": 4000,
    "yukio": 15000,
    "flower sword": 600,

    # Prestige (removed +/- values as they represent changes, not base value)
    "prestige bag": 76000,
    "prestige firework rocket launcher (pfrl)": 45000,
    "prestige firework dagger (pfd)": 109000,
    "prestige inferno rocket blade (pirb)": 230000,
    "prestige firework lancer (pfl)": 290000,
    "prestige candy cane (pcc)": 465000,

    # Misc
    "valk heads": 15000,
    "black valk head": 33000,
    "blood scythe": 200,
    "nightfall shroud": 4500,
    "black bull": 1000,
    "golden haori": 1000,
    "tentails": 1200,
    "all mythic fruits": 20950, # Это агрегированное значение, но по вашей просьбе включено
    "gunblade": 300,
    "snowcap scepter": 2500,
    "zorana's robe": 600, # Указано 300-600, взял максимальное
    "zorana's haori": 600, # Указано 300-600, взял максимальное
    "frostspire hood": 300,
    "other valk heads": 130000,
    "sparkle valk": 230000,
    "dominus": 875000,
    "cupid bow": 100,
    "blessed cupid bow": 2500,
    "exalted cupid queen outfit": 300,
    "blessed cupid queen outfit": 2000,
    "cupid vanguard outfit": 100,
    "blessed cupid vanguard outfit": 400,
    "cupid queen's scarf": 300,
    "blessed cupid queen's scarf": 2750,
    "exalted cupid queen's wings": 300,
    "blessed exalted cupid queen's wings": 4500,
    "supreme gift box armour": 100,
    "supreme gift box helmet": 100,
    "supreme gift box rocky pet": 150,
    "mega pow": 200,
    "anomalized mega pow": 68000,
    "clown": 1500,
    "troll": 2500,
    "peanut butter jelly time banana": 1500,
    "blo crimson sledgehammer": 1500,
    "kumakawa head": 1400,
    "usamii head": 800,
    "bunyo the bunny": 2000
}

def parse_items(text: str):
    result = {}
    parts = re.split(r',\s*', text.lower())
    for part in parts:
        match = re.match(r'(?:(\d+)\s+)?(.+)', part)
        if match:
            count = int(match.group(1)) if match.group(1) else 1
            name = match.group(2).strip()
            result[name] = result.get(name, 0) + count
    return result

def find_closest(item):
    match, score = process.extractOne(item, items.keys())
    return match if score > 80 else None

def compute_total(item_dict):
    total = 0
    details = []
    failed = []
    for name, count in item_dict.items():
        match = find_closest(name)
        if match:
            value = items[match] * count
            total += value
            details.append(f"{count} × {match} = {value}")
        else:
            failed.append(name)
    return total, details, failed

async def item_autocomplete(interaction: discord.Interaction, current: str):
    # Разделяем строку по запятой
    parts = [p.strip() for p in current.lower().split(",")]
    last = parts[-1] if parts else ""

    # Парсим число (если есть)
    match = re.match(r"(?:(\d+)\s+)?(.+)", last)
    count = match.group(1) if match and match.group(1) else ""
    query = match.group(2) if match else last

    # Ищем совпадения по названию предмета
    suggestions = []
    for item in items:
        score = process.extractOne(query, [item])[1] if query else 100
        if score > 50:
            prefix = f"{count} " if count else ""
            suggestion = prefix + item
            full = ", ".join(parts[:-1] + [suggestion])
            if len(full) <= 100:  # Discord ограничение
                suggestions.append(app_commands.Choice(name=full, value=full))
        if len(suggestions) >= 20:
            break

    return suggestions

# 💬 Команда с автодополнением
@tree.command(name="trade", description="Сравнить вашу торговлю с предложением оппонента")
@app_commands.describe(yours="Что вы предлагаете", theirs="Что предлагает другой игрок")
@app_commands.autocomplete(yours=item_autocomplete, theirs=item_autocomplete)
async def trade(interaction: discord.Interaction, yours: str, theirs: str):
    if interaction.channel_id != GPO_TRADE_CHANNEL_ID:
        await interaction.response.send_message(
            "❌ Использование этой команды разрешено только в определённом канале.",
            ephemeral=True
        )
        return

    your_items = parse_items(yours)
    their_items = parse_items(theirs)

    your_total, your_details, your_failed = compute_total(your_items)
    their_total, their_details, their_failed = compute_total(their_items)

    if your_failed or their_failed:
        msg = ""
        if your_failed:
            for wrong in your_failed:
                suggestion, _ = process.extractOne(wrong, items.keys())
                msg += f"Не найдено '{wrong}'. Возможно, вы имели в виду **{suggestion}**?\n"
        if their_failed:
            for wrong in their_failed:
                suggestion, _ = process.extractOne(wrong, items.keys())
                msg += f"Не найдено '{wrong}'. Возможно, вы имели в виду **{suggestion}**?\n"
        await interaction.response.send_message(msg, ephemeral=True)
        return

    diff = your_total - their_total
    percent = round(abs(diff) / max(your_total, their_total) * 100, 2)
    if your_total > their_total:
        result = f"❌ Вы **в минусе** на {percent}%"
    elif your_total < their_total:
        result = f"✅ Вы **в плюсе** на {percent}%"
    else:
        result = "⚖️ Обмен **равноценен**"

    await interaction.response.send_message(
        "**Вы предложили:**\n" +
        "\n".join(your_details) + f"\nИтого: `{your_total}`\n\n" +
        "**Оппонент предложил:**\n" +
        "\n".join(their_details) + f"\nИтого: `{their_total}`\n\n" +
        result
    )

    # ⏳ Удаление ответа бота через 30 секунд
    sent_message = await interaction.original_response()
    await asyncio.sleep(30)
    try:
        await sent_message.delete()
    except discord.NotFound:
        pass

@client.event
async def on_ready():
    await tree.sync()
    print(f"Бот запущен как {client.user}")

keep_alive()
load_dotenv()
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
