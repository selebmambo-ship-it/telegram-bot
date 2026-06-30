from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import phonenumbers
from phonenumbers import (
    geocoder,
    carrier,
    timezone,
    PhoneNumberFormat,
    number_type,
)

TOKEN = "8886821322:AAGnasBcx0agwoW4xyr3SK-LvN66LYq1UVg"

mode_user = {}

keyboard = [
    [
        InlineKeyboardButton("📱 Phone Lookup", callback_data="phone")
    ],
    [
        InlineKeyboardButton("📊 Statistik", callback_data="stats"),
        InlineKeyboardButton("ℹ️ Bantuan", callback_data="help")
    ]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
🤖 PREMIUM TOOLS BOT

Selamat datang.

Silakan pilih menu di bawah.

Developer : Supri
Version : 1.0
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "phone":
        mode_user[query.from_user.id] = "phone"

        await query.edit_message_text(
            """
📱 PHONE LOOKUP

Kirim nomor yang ingin dicek.

Contoh:
+628123456789
atau
08123456789
"""
        )

    elif data == "stats":
        await query.edit_message_text(
            """
📊 Statistik

Belum ada data.
"""
        )

    elif data == "help":
        await query.edit_message_text(
            """
ℹ️ Bantuan

/start = Membuka menu.
"""
        )


async def pesan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if mode_user.get(uid) != "phone":
        return

    nomor = update.message.text.strip()

    if nomor.startswith("08"):
        nomor = "+62" + nomor[1:]

    try:
        parsed = phonenumbers.parse(nomor)

        valid = phonenumbers.is_valid_number(parsed)
        possible = phonenumbers.is_possible_number(parsed)

        negara = geocoder.description_for_number(parsed, "id")
        operator = carrier.name_for_number(parsed, "id")
        zona = ", ".join(timezone.time_zones_for_number(parsed))

        nasional = phonenumbers.format_number(
            parsed,
            PhoneNumberFormat.NATIONAL
        )

        internasional = phonenumbers.format_number(
            parsed,
            PhoneNumberFormat.INTERNATIONAL
        )

        e164 = phonenumbers.format_number(
            parsed,
            PhoneNumberFormat.E164
        )

        tipe = number_type(parsed)

        if tipe == phonenumbers.PhoneNumberType.MOBILE:
            tipe = "📱 Mobile"
        elif tipe == phonenumbers.PhoneNumberType.FIXED_LINE:
            tipe = "☎️ Rumah"
        elif tipe == phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE:
            tipe = "📞 Mobile/Rumah"
        elif tipe == phonenumbers.PhoneNumberType.TOLL_FREE:
            tipe = "🆓 Toll Free"
        elif tipe == phonenumbers.PhoneNumberType.PREMIUM_RATE:
            tipe = "💰 Premium"
        elif tipe == phonenumbers.PhoneNumberType.VOIP:
            tipe = "🌐 VoIP"
        else:
            tipe = "❓ Unknown"

        hasil = f"""
🤖 PREMIUM TOOLS BOT

📱 HASIL CEK NOMOR

📞 {internasional}
🌍 {negara}
🏢 {operator}
📱 {tipe}
✅ {"Valid" if valid else "Tidak Valid"}
🟢 {"Aktif" if possible else "Tidak Diketahui"}

━━━━━━━━━━━━━━
🌐 Kode : +{parsed.country_code}
🕒 Zona : {zona}
"""

        await update.message.reply_text(hasil)

    except Exception:
        await update.message.reply_text("❌ Nomor tidak valid.")
# ==============================
# MAIN
# ==============================

app = Application.builder().token(TOKEN).build()

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    CallbackQueryHandler(
        menu
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        pesan
    )
)

print("🤖 Bot Online...")

app.run_polling()