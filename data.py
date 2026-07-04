# =====================================================================
#  FIFA WORLD CUP 2026 — DATA
#  48 equipos / 12 grupos de 4
#  ⚠️ Actualiza los grupos cuando salga el sorteo oficial (2025)
# =====================================================================

GROUPS = {
    "A": {"teams": [{"name": "Estados Unidos", "flag": "🇺🇸"}, {"name": "México", "flag": "🇲🇽"}, {"name": "Panamá", "flag": "🇵🇦"}, {"name": "Bolivia", "flag": "🇧🇴"}]},
    "B": {"teams": [{"name": "España", "flag": "🇪🇸"}, {"name": "Marruecos", "flag": "🇲🇦"}, {"name": "Bélgica", "flag": "🇧🇪"}, {"name": "Ucrania", "flag": "🇺🇦"}]},
    "C": {"teams": [{"name": "Francia", "flag": "🇫🇷"}, {"name": "Brasil", "flag": "🇧🇷"}, {"name": "Serbia", "flag": "🇷🇸"}, {"name": "Australia", "flag": "🇦🇺"}]},
    "D": {"teams": [{"name": "Argentina", "flag": "🇦🇷"}, {"name": "Portugal", "flag": "🇵🇹"}, {"name": "Ecuador", "flag": "🇪🇨"}, {"name": "Arabia Saudita", "flag": "🇸🇦"}]},
    "E": {"teams": [{"name": "Inglaterra", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"}, {"name": "Países Bajos", "flag": "🇳🇱"}, {"name": "Irán", "flag": "🇮🇷"}, {"name": "Senegal", "flag": "🇸🇳"}]},
    "F": {"teams": [{"name": "Alemania", "flag": "🇩🇪"}, {"name": "Colombia", "flag": "🇨🇴"}, {"name": "Uruguay", "flag": "🇺🇾"}, {"name": "Turquía", "flag": "🇹🇷"}]},
    "G": {"teams": [{"name": "Japón", "flag": "🇯🇵"}, {"name": "Croacia", "flag": "🇭🇷"}, {"name": "Costa Rica", "flag": "🇨🇷"}, {"name": "Nueva Zelanda", "flag": "🇳🇿"}]},
    "H": {"teams": [{"name": "Dinamarca", "flag": "🇩🇰"}, {"name": "México B", "flag": "🇲🇽"}, {"name": "Camerún", "flag": "🇨🇲"}, {"name": "Eslovenia", "flag": "🇸🇮"}]},
    "I": {"teams": [{"name": "Italia", "flag": "🇮🇹"}, {"name": "Rumania", "flag": "🇷🇴"}, {"name": "Albania", "flag": "🇦🇱"}, {"name": "Irak", "flag": "🇮🇶"}]},
    "J": {"teams": [{"name": "Suiza", "flag": "🇨🇭"}, {"name": "Nigeria", "flag": "🇳🇬"}, {"name": "República Checa", "flag": "🇨🇿"}, {"name": "Indonesia", "flag": "🇮🇩"}]},
    "K": {"teams": [{"name": "Corea del Sur", "flag": "🇰🇷"}, {"name": "Polonia", "flag": "🇵🇱"}, {"name": "Paraguay", "flag": "🇵🇾"}, {"name": "Kenia", "flag": "🇰🇪"}]},
    "L": {"teams": [{"name": "Canadá", "flag": "🇨🇦"}, {"name": "Perú", "flag": "🇵🇪"}, {"name": "Trinidad y Tobago", "flag": "🇹🇹"}, {"name": "Tanzania", "flag": "🇹🇿"}]},
}

KNOCKOUT_ROUNDS = [
    {"id": "r32",   "name": "Ronda de 32",      "slots": 32, "pts": 5},
    {"id": "r16",   "name": "Octavos de Final",  "slots": 16, "pts": 6},
    {"id": "qf",    "name": "Cuartos de Final",  "slots": 8,  "pts": 8},
    {"id": "sf",    "name": "Semifinales",        "slots": 4,  "pts": 11},
    {"id": "3rd",   "name": "Tercer Lugar",       "slots": 2,  "pts": 10},
    {"id": "final", "name": "Gran Final",         "slots": 2,  "pts": 15},
]

SCORING = {
    "group_winner": 3,
    "group_runner": 2,
    "r32": 5,
    "r16": 6,
    "qf": 8,
    "sf": 11,
    "3rd": 10,
    "final_runner": 12,
    "final_winner": 20,
}

ADMIN_PASSWORD = "mundial2026admin"  # ← CAMBIA ESTO antes de publicar
