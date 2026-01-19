from telegram.ext import Updater, MessageHandler, Filters

TOKEN = "DAN_TOKEN_CUA_BAN"

# 🔑 KHAI BÁO 2 KHÁCH
KHACH = {
    111111111: {   # user_id khách A
        "c": 21.8,
        "da": 38
    },
    222222222: {   # user_id khách B
        "c": 22,
        "da": 40
    }
}

def tinh_tien(text, cong_thuc):
    tong_c = 0
    tong_da = 0

    lines = text.lower().split("\n")
    for line in lines:
        parts = line.split()
        if "c" in parts:
            so_tien = int(parts[-1])
            tong_c += so_tien * cong_thuc["c"]
        if "da" in parts or "đá" in parts:
            so_tien = int(parts[-1])
            tong_da += so_tien * cong_thuc["da"]

    tong = int(tong_c + tong_da)
    return int(tong_c), int(tong_da), tong


def xu_ly_tin(update, context):
    user_id = update.message.from_user.id
    tin_goc = update.message.text

    if user_id not in KHACH:
        update.message.reply_text("❌ Bạn chưa được cấp quyền")
        return

    cong_thuc = KHACH[user_id]
    c, da, tong = tinh_tien(tin_goc, cong_thuc)

    ket_qua = f"""KOS bot
truong thu
{tin_goc}

Đã nhận tin 🍪
2CB: {c}
ĐáT: {da}

🍀 Tổng = {tong}
"""

    update.message.reply_text(ket_qua)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, xu_ly_tin))
    updater.start_polling()
    updater.idle()

main()
