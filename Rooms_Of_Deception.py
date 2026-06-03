import time
import os
import random

# ─────────────────────────────────────────────
#  Utility
# ─────────────────────────────────────────────

def slow_type(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def pause(sec=0.8):
    time.sleep(sec)

def divider():
    print("\n" + "─" * 40 + "\n")

def get_choice(prompt, options):
    """Keep asking until the player enters a valid option number."""
    while True:
        slow_type(prompt)
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        choice = input("\n> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        slow_type("Please enter a valid number.")

# ─────────────────────────────────────────────
#  Character Classes
# ─────────────────────────────────────────────

CLASSES = {
    "Warrior": {
        "description": "A brave fighter with high strength.",
        "hp": 120,
        "attack": 20,
        "defence": 10,
        "skill": "Shield Bash",
        "skill_desc": "Deals double damage and stuns the enemy for one turn.",
    },
    "Rogue": {
        "description": "A cunning trickster who strikes fast.",
        "hp": 90,
        "attack": 30,
        "defence": 5,
        "skill": "Backstab",
        "skill_desc": "Deals triple damage but can only be used once per fight.",
    },
    "Mage": {
        "description": "A powerful spellcaster with arcane knowledge.",
        "hp": 80,
        "attack": 35,
        "defence": 3,
        "skill": "Fireball",
        "skill_desc": "Hits all enemies for 40 damage (single enemy: 50).",
    },
}

def pick_character(player_num=1):
    divider()
    slow_type(f"Player {player_num} — choose your character class:\n")
    class_names = list(CLASSES.keys())
    for i, name in enumerate(class_names, 1):
        c = CLASSES[name]
        print(f"  {i}. {name} — {c['description']}")
        print(f"       HP:{c['hp']}  ATK:{c['attack']}  DEF:{c['defence']}  Skill: {c['skill']}")
    choice = get_choice("", class_names)
    name_chosen = class_names[choice - 1]
    return name_chosen, dict(CLASSES[name_chosen])

# ─────────────────────────────────────────────
#  Combat System
# ─────────────────────────────────────────────

class Fighter:
    def __init__(self, name, cls_name, stats):
        self.name = name
        self.cls = cls_name
        self.hp = stats["hp"]
        self.max_hp = stats["hp"]
        self.attack = stats["attack"]
        self.defence = stats["defence"]
        self.skill = stats["skill"]
        self.skill_desc = stats["skill_desc"]
        self.skill_used = False
        self.stunned = False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        actual = max(0, dmg - self.defence)
        self.hp = max(0, self.hp - actual)
        return actual

    def basic_attack(self, target):
        dmg = self.attack + random.randint(-5, 5)
        dealt = target.take_damage(dmg)
        slow_type(f"  {self.name} attacks {target.name} for {dealt} damage! ({target.name} HP: {target.hp})")

    def use_skill(self, target):
        if self.skill_used and self.cls == "Rogue":
            slow_type("  Backstab already used! Falling back to basic attack.")
            self.basic_attack(target)
            return

        if self.cls == "Warrior":
            dmg = self.attack * 2 + random.randint(0, 5)
            dealt = target.take_damage(dmg)
            target.stunned = True
            slow_type(f"  {self.name} uses Shield Bash! {dealt} damage — {target.name} is stunned!")
        elif self.cls == "Rogue":
            dmg = self.attack * 3
            dealt = target.take_damage(dmg)
            slow_type(f"  {self.name} uses Backstab! Critical hit for {dealt} damage!")
            self.skill_used = True
        elif self.cls == "Mage":
            dmg = 50
            dealt = target.take_damage(dmg)
            slow_type(f"  {self.name} hurls a Fireball! {dealt} damage to {target.name}!")

def combat(player, enemy_name, enemy_hp, enemy_atk, enemy_def=2):
    divider()
    slow_type(f"⚔️  A {enemy_name} appears!")
    enemy = Fighter(enemy_name, "Enemy", {
        "hp": enemy_hp, "attack": enemy_atk, "defence": enemy_def,
        "skill": "", "skill_desc": ""
    })
    round_num = 1

    while player.is_alive() and enemy.is_alive():
        slow_type(f"\n--- Round {round_num} ---")
        slow_type(f"Your HP: {player.hp} | {enemy_name} HP: {enemy.hp}")

        if player.stunned:
            slow_type(f"  {player.name} is stunned and loses their turn!")
            player.stunned = False
        else:
            action = get_choice("What will you do?", [
                "Basic Attack",
                f"Use Skill: {player.skill} ({player.skill_desc})",
                "Flee (50% chance)"
            ])
            if action == 1:
                player.basic_attack(enemy)
            elif action == 2:
                player.use_skill(enemy)
            elif action == 3:
                if random.random() < 0.5:
                    slow_type("  You successfully fled!")
                    return "fled"
                else:
                    slow_type("  You couldn't escape!")

        if enemy.is_alive():
            # Simple enemy AI — occasionally uses a heavy attack
            if random.random() < 0.25:
                dmg = int(enemy_atk * 1.5) + random.randint(0, 4)
                dealt = player.take_damage(dmg)
                slow_type(f"  {enemy_name} uses a heavy strike for {dealt} damage!")
            else:
                dmg = enemy_atk + random.randint(-3, 3)
                dealt = player.take_damage(dmg)
                slow_type(f"  {enemy_name} attacks for {dealt} damage!")

        round_num += 1

    if player.is_alive():
        slow_type(f"\n✅ You defeated the {enemy_name}!")
        return "win"
    else:
        slow_type(f"\n💀 {player.name} was defeated by the {enemy_name}...")
        return "lose"

# ─────────────────────────────────────────────
#  NPC AI (simple personality-driven responses)
# ─────────────────────────────────────────────

NPC_RESPONSES = {
    "innkeeper": {
        "greeting": "Welcome, traveller. What brings you to the Rooms of Deception?",
        "quest":    "Rumour has it the Shadow Key is hidden beyond the Whispering Hall. Beware the Sentinel.",
        "heal":     "Rest here a while. You look like you need it.",
        "farewell": "Safe travels. The rooms are not kind to the unprepared.",
    },
    "merchant": {
        "greeting": "Ah, a customer! Rare in these parts.",
        "sell":     "I have potions, torches, and the occasional oddity. Choose wisely.",
        "farewell": "Come back if you survive!",
    },
    "guard": {
        "greeting": "Halt! State your business.",
        "allow":    "Very well. You may pass — but stay alert.",
        "warn":     "Many who entered the inner chamber never returned.",
    },
}

def talk_to_npc(npc_key, player):
    npc = NPC_RESPONSES.get(npc_key, {})
    divider()
    slow_type(f"[{npc_key.capitalize()}]: {npc.get('greeting', 'Hello.')}")
    pause()

    if npc_key == "innkeeper":
        choice = get_choice("What do you say?", ["Ask about the quest", "Ask to rest (restore 30 HP)", "Say farewell"])
        if choice == 1:
            slow_type(f"[Innkeeper]: {npc['quest']}")
        elif choice == 2:
            heal = min(30, player.max_hp - player.hp)
            player.hp += heal
            slow_type(f"[Innkeeper]: {npc['heal']}")
            slow_type(f"  You recover {heal} HP. Current HP: {player.hp}")
        else:
            slow_type(f"[Innkeeper]: {npc['farewell']}")

    elif npc_key == "merchant":
        slow_type(f"[Merchant]: {npc['sell']}")
        slow_type("  (You have no gold — the merchant shrugs and lets you pass.)")

    elif npc_key == "guard":
        choice = get_choice("What do you say?", ["State your purpose", "Try to sneak past"])
        if choice == 1:
            slow_type(f"[Guard]: {npc['allow']}")
            slow_type(f"[Guard]: {npc['warn']}")
        else:
            slow_type("  You attempt to sneak past...")
            if random.random() < 0.5:
                slow_type("  You slip by unnoticed!")
            else:
                slow_type("  The guard catches you!")
                result = combat(player, "Guard", enemy_hp=60, enemy_atk=12)
                if result == "lose":
                    return "dead"
    return "ok"

# ─────────────────────────────────────────────
#  Game World — Rooms
# ─────────────────────────────────────────────

def room_entrance(player):
    divider()
    slow_type("You stand at the entrance of a crumbling stone building.")
    slow_type("A sign above the door reads: ROOMS OF DECEPTION")
    pause()
    choice = get_choice("What do you do?", [
        "Enter the building",
        "Examine the surroundings",
        "Turn back (lose the game)"
    ])
    if choice == 1:
        slow_type("You push open the heavy oak door and step inside...")
        return "inn"
    elif choice == 2:
        slow_type("You spot a rusty sword on the ground. You pick it up — it feels heavier than expected.")
        player.attack += 5
        slow_type(f"  Attack increased to {player.attack}!")
        return "inn"
    else:
        slow_type("You turn and walk away. The building watches you leave...")
        return "lose"

def room_inn(player):
    divider()
    slow_type("You find yourself in a dimly lit inn. An innkeeper watches you from behind the counter.")
    result = talk_to_npc("innkeeper", player)
    if result == "dead":
        return "lose"

    choice = get_choice("Where do you go next?", [
        "Head to the market stall",
        "Go straight to the Whispering Hall",
    ])
    if choice == 1:
        return "market"
    else:
        return "hall"

def room_market(player):
    divider()
    slow_type("A rickety market stall sits in the corner. A shady merchant grins at you.")
    talk_to_npc("merchant", player)
    slow_type("\nWith nothing left to buy, you head toward the Whispering Hall.")
    return "hall"

def room_hall(player):
    divider()
    slow_type("You enter the Whispering Hall. The walls seem to breathe.")
    slow_type("A guard blocks the passage ahead.")
    result = talk_to_npc("guard", player)
    if result == "dead":
        return "lose"
    if not player.is_alive():
        return "lose"

    slow_type("\nBeyond the guard, you hear a low growl...")
    pause(1)
    result = combat(player, "Cave Troll", enemy_hp=80, enemy_atk=15, enemy_def=5)
    if result == "lose":
        return "lose"
    if result == "fled":
        slow_type("You flee back to the inn...")
        return "inn"

    slow_type("\nYou find a locked door. A shadow flickers beyond the keyhole.")
    return "final"

def room_final(player):
    divider()
    slow_type("You've reached the heart of the Rooms of Deception.")
    slow_type("The Shadow Sentinel stands before you, guarding the Shadow Key.")
    pause(1)
    slow_type("'Turn back,' it rasps. 'Or face oblivion.'")
    pause()

    choice = get_choice("What do you do?", [
        "Fight the Shadow Sentinel",
        "Attempt to negotiate",
        "Search for another way"
    ])

    if choice == 1:
        result = combat(player, "Shadow Sentinel", enemy_hp=120, enemy_atk=22, enemy_def=8)
        if result == "lose":
            return "lose"
        return "win"

    elif choice == 2:
        slow_type("You try to reason with the Sentinel...")
        if player.cls == "Mage":
            slow_type("It seems to recognise the arcane symbols on your robe.")
            slow_type("'...You may pass, spellweaver.' It steps aside.")
            return "win"
        else:
            slow_type("The Sentinel is unmoved. It raises its blade.")
            result = combat(player, "Shadow Sentinel", enemy_hp=120, enemy_atk=22, enemy_def=8)
            if result == "lose":
                return "lose"
            return "win"

    else:
        slow_type("You search the walls and find a hidden lever...")
        if random.random() < 0.5:
            slow_type("It opens a secret passage! You sneak past the Sentinel and grab the key!")
            return "win"
        else:
            slow_type("The lever triggers a trap — the Sentinel is alerted!")
            result = combat(player, "Shadow Sentinel", enemy_hp=100, enemy_atk=25, enemy_def=5)
            if result == "lose":
                return "lose"
            return "win"

# ─────────────────────────────────────────────
#  Endings
# ─────────────────────────────────────────────

def ending_win(player):
    divider()
    slow_type("🏆  You grasp the Shadow Key. A blinding light fills the room.")
    pause()
    slow_type("The Rooms of Deception crumble around you as you step into the sunlight.")
    pause()
    slow_type(f"  {player.name} the {player.cls} has conquered the Rooms of Deception!")
    slow_type(f"  Final HP: {player.hp}/{player.max_hp}")
    divider()

def ending_lose(player):
    divider()
    slow_type("💀  Darkness closes in...")
    pause()
    slow_type(f"  {player.name} the {player.cls} fell in the Rooms of Deception.")
    slow_type("  The rooms claim another soul.")
    divider()

# ─────────────────────────────────────────────
#  Name Entry
# ─────────────────────────────────────────────

def get_player_name(player_num=1):
    verified = False
    name = ""
    while not verified:
        name = input(f"Player {player_num}, what is your name? ").strip().capitalize()
        pause(0.5)
        print(f"\n  {name}\n")
        confirm = input("Are you sure? (yes / no): ").strip().lower()
        if confirm == "yes":
            verified = True
    return name

# ─────────────────────────────────────────────
#  Single Player Game
# ─────────────────────────────────────────────

def run_single_player():
    slow_type("\n=== SINGLE PLAYER MODE ===\n")
    name = get_player_name(1)
    cls_name, stats = pick_character(1)
    player = Fighter(name, cls_name, stats)
    slow_type(f"\nWelcome, {player.name} the {player.cls}!")
    pause()

    state = "entrance"
    while state not in ("win", "lose"):
        if state == "entrance":
            state = room_entrance(player)
        elif state == "inn":
            state = room_inn(player)
        elif state == "market":
            state = room_market(player)
        elif state == "hall":
            state = room_hall(player)
        elif state == "final":
            state = room_final(player)

    if state == "win":
        ending_win(player)
    else:
        ending_lose(player)

# ─────────────────────────────────────────────
#  Co-op Multiplayer Game (local, turn-based)
# ─────────────────────────────────────────────

def coop_combat(p1, p2, enemy_name, enemy_hp, enemy_atk, enemy_def=2):
    """Both players fight the same enemy, taking turns."""
    divider()
    slow_type(f"⚔️  A {enemy_name} appears! Both players must fight together!")
    enemy = Fighter(enemy_name, "Enemy", {
        "hp": enemy_hp, "attack": enemy_atk, "defence": enemy_def,
        "skill": "", "skill_desc": ""
    })
    players = [p for p in [p1, p2] if p.is_alive()]
    round_num = 1

    while enemy.is_alive() and any(p.is_alive() for p in players):
        slow_type(f"\n--- Round {round_num} ---")
        slow_type(f"  {enemy_name} HP: {enemy.hp}")
        for p in players:
            slow_type(f"  {p.name} HP: {p.hp}")

        for player in players:
            if not player.is_alive() or not enemy.is_alive():
                continue
            if player.stunned:
                slow_type(f"  {player.name} is stunned and loses their turn!")
                player.stunned = False
                continue

            slow_type(f"\n{player.name}'s turn:")
            action = get_choice("What will you do?", [
                "Basic Attack",
                f"Use Skill: {player.skill}",
                "Flee (50% chance)"
            ])
            if action == 1:
                player.basic_attack(enemy)
            elif action == 2:
                player.use_skill(enemy)
            elif action == 3:
                if random.random() < 0.5:
                    slow_type(f"  {player.name} fled from battle!")
                    players.remove(player)
                    break

        if enemy.is_alive():
            target = random.choice([p for p in players if p.is_alive()]) if players else None
            if target:
                dmg = enemy_atk + random.randint(-3, 3)
                dealt = target.take_damage(dmg)
                slow_type(f"  {enemy_name} attacks {target.name} for {dealt} damage!")

        round_num += 1

    if enemy.is_alive():
        return "lose"
    slow_type(f"\n✅ The {enemy_name} is defeated!")
    return "win"

def run_coop():
    slow_type("\n=== CO-OP MULTIPLAYER MODE ===")
    slow_type("Two players, one adventure. Take turns making choices.\n")

    name1 = get_player_name(1)
    cls1, stats1 = pick_character(1)
    p1 = Fighter(name1, cls1, stats1)

    name2 = get_player_name(2)
    cls2, stats2 = pick_character(2)
    p2 = Fighter(name2, cls2, stats2)

    slow_type(f"\nWelcome, {p1.name} the {p1.cls} and {p2.name} the {p2.cls}!")
    pause()

    # Simplified co-op adventure path
    divider()
    slow_type("You both arrive at the entrance of the Rooms of Deception.")

    choice = get_choice("Player 1, what does the group do?", [
        "Enter together",
        "Scout ahead (Player 2 goes first)",
    ])
    slow_type("You push open the doors and step inside together..." if choice == 1
              else f"{p2.name} scouts ahead while {p1.name} watches the entrance...")
    pause()

    # Heal via innkeeper for both
    slow_type("\nThe innkeeper greets you both. She offers a short rest.")
    for p in [p1, p2]:
        heal = min(20, p.max_hp - p.hp)
        p.hp += heal
        if heal:
            slow_type(f"  {p.name} recovers {heal} HP.")

    # Hall fight
    divider()
    slow_type("In the Whispering Hall, a Cave Troll blocks your path!")
    result = coop_combat(p1, p2, "Cave Troll", enemy_hp=100, enemy_atk=14, enemy_def=5)
    if result == "lose" or (not p1.is_alive() and not p2.is_alive()):
        slow_type("\n💀 Both players have fallen. The rooms claim you both.")
        return

    # Final boss
    divider()
    slow_type("You reach the final chamber together. The Shadow Sentinel waits.")
    alive = [p for p in [p1, p2] if p.is_alive()]
    if len(alive) == 2:
        result = coop_combat(p1, p2, "Shadow Sentinel", enemy_hp=150, enemy_atk=20, enemy_def=8)
    else:
        slow_type(f"Only {alive[0].name} remains standing...")
        result = combat(alive[0], "Shadow Sentinel", enemy_hp=130, enemy_atk=20, enemy_def=8)

    if result == "win":
        divider()
        slow_type("🏆  The Shadow Key is yours!")
        slow_type("The Rooms of Deception crumble as you both escape into daylight.")
        for p in [p1, p2]:
            if p.is_alive():
                slow_type(f"  {p.name} the {p.cls} survived with {p.hp}/{p.max_hp} HP!")
    else:
        slow_type("\n💀 The Sentinel was too powerful. The rooms claim you all.")

# ─────────────────────────────────────────────
#  Main Menu
# ─────────────────────────────────────────────

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    slow_type("╔══════════════════════════════════════╗")
    slow_type("║      ROOMS  OF  DECEPTION            ║")
    slow_type("╚══════════════════════════════════════╝")
    pause()

    while True:
        mode = get_choice("\nMain Menu", [
            "Single Player",
            "Co-op Multiplayer (2 players, same keyboard)",
            "Quit"
        ])

        if mode == 1:
            run_single_player()
        elif mode == 2:
            run_coop()
        else:
            slow_type("Thanks for playing. Goodbye!")
            break

        again = get_choice("\nPlay again?", ["Yes", "No"])
        if again == 2:
            slow_type("Thanks for playing. Goodbye!")
            break

if __name__ == "__main__":
    main()
