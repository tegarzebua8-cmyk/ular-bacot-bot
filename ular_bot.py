import random
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
TANGGA = {4: 25, 13: 46, 33: 49, 42: 63, 50: 69, 62: 81, 74: 92}
ULAR = {27: 5, 40: 3, 43: 18, 54: 31, 66: 45, 76: 58, 89: 53, 99: 41}
TRUTH = ["Stalking mantan terakhir kapan?", "Suka siapa di grup ini?", "Rahasia yang belum orang tau?"]
DARE = ["VN nyanyi balonku ada 5!", "Ganti nama jadi Budak Grup 10 menit!", "Kirim selfie jelek!"]
games = {}

async def ularmulai(update, context):
    games[update.effective_chat.id] = {"pemain": {}, "giliran": [], "turn": 0}
    await update.message.reply_text("🐍 GAME DIMULAI!\n/gabung buat ikut\n/lempar buat main!")

async def gabung(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    if chat_id not in games:
        return await update.message.reply_text("Ketik /ularmulai dulu")
    game = games[chat_id]
    game["pemain"][user.id] = {"nama": user.first_name, "pos": 1}
    game["giliran"].append(user.id)
    await update.message.reply_text(f"✅ {user.first_name} gabung!")

async def lempar(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    if chat_id not in games:
        return await update.message.reply_text("Belum mulai gamenya")
    game = games[chat_id]
    dadu = random.randint(1,6)
    pemain = game["pemain"][user.id]
    pos_awal = pemain["pos"]
    pos = pos_awal + dadu
    if pos > 100: pos = pos_awal
    msg = f"🎲 {user.first_name} dapat {dadu} | {pos_awal} -> {pos}"
    if pos in TANGGA:
        msg += f"\n🪜 NAIK TANGGA {pos}->{TANGGA[pos]}\nTRUTH: {random.choice(TRUTH)}"
        pos = TANGGA[pos]
    if pos in ULAR:
        msg += f"\n🐍 KENA ULAR {pos}->{ULAR[pos]}\nDARE: {random.choice(DARE)}"
        pos = ULAR[pos]
    pemain["pos"] = pos
    if pos == 100:
        await update.message.reply_text(f"🏆 {user.first_name} MENANG SAMPAI 100!")
        del games[chat_id]
    else:
        await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("ularmulai", ularmulai))
app.add_handler(CommandHandler("gabung", gabung))
app.add_handler(CommandHandler("lempar", lempar))
app.run_polling()
