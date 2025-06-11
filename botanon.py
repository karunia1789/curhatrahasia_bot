
import telebot

import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

waiting_users = []
paired_users = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Selamat datang di *Curhat Anonim*\n\n"
        "Ketik /cari untuk mencari teman ngobrol secara anonim.\n"
        "Ketik /berhenti untuk keluar dari obrolan.",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['cari'])
def cari(message):
    user_id = message.chat.id
    if user_id in paired_users:
        bot.send_message(user_id, "⚠️ Kamu sudah terhubung. Ketik /berhenti untuk keluar.")
        return

    if waiting_users:
        partner_id = waiting_users.pop(0)
        paired_users[user_id] = partner_id
        paired_users[partner_id] = user_id

        bot.send_message(user_id, "✅ Kamu terhubung dengan seseorang. Silakan mulai ngobrol.")
        bot.send_message(partner_id, "✅ Kamu terhubung dengan seseorang. Silakan mulai ngobrol.")
    else:
        waiting_users.append(user_id)
        bot.send_message(user_id, "🔍 Menunggu teman ngobrol...")

@bot.message_handler(commands=['berhenti'])
def berhenti(message):
    user_id = message.chat.id
    if user_id in paired_users:
        partner_id = paired_users.pop(user_id)
        paired_users.pop(partner_id, None)

        bot.send_message(user_id, "❌ Kamu keluar dari obrolan.")
        bot.send_message(partner_id, "⚠️ Temanmu keluar dari obrolan.")
    elif user_id in waiting_users:
        waiting_users.remove(user_id)
        bot.send_message(user_id, "⏹️ Kamu batal menunggu.")
    else:
        bot.send_message(user_id, "ℹ️ Kamu tidak sedang dalam obrolan.")

@bot.message_handler(func=lambda m: True)
def relay_message(message):
    user_id = message.chat.id
    if user_id in paired_users:
        partner_id = paired_users[user_id]
        try:
            bot.send_message(partner_id, message.text)
        except:
            bot.send_message(user_id, "❌ Gagal mengirim pesan.")
    else:
        bot.send_message(user_id, "ℹ️ Kamu belum terhubung dengan siapa pun. Ketik /cari.")

bot.polling()
