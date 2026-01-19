from telegram.ext import Updater, MessageHandler, Filters

# =========================
# 1️⃣ TOKEN BOT
# =========================
TOKEN = "8554596056:AAH6QcIj9ehxUW5Y37D8sOz1gse0QkCufXQ"



# =========================
# 2️⃣ BẢNG GIÁ THEO KHÁCH
# =========================
KHACH = {
    111111111: {   # khách A
        "MB": {
            "2CB": 37,
            "2CD": 36,
            "3CB": 20,
            "3CXC": 17,
            "DA_T": 1.8
        },
        "THUONG": {
            "2CB": 39.6,
            "2CD": 38,
            "3CB": 21.6,
            "3CXC": 18,
            "DA_T": 2.0
        }
    },
    222222222: {   # khách B
        "MB": {
            "2CB": 38,
            "2CD": 37,
            "3CB": 21,
            "3CXC": 18,
            "DA_T": 1.9
        },
        "THUONG": {
            "2CB": 40,
            "2CD": 39,
            "3CB": 22,
            "3CXC": 19,
            "DA_T": 2.2
        }
    }
}


# =========================
# 3️⃣ LẤY SỐ ĐÀI
# =========================
def lay_so_dai(text):
    for i in range(2, 5):
        if f"{i}dai" in text:
            return i
    return 1   # mặc định MB


# =========================
# 4️⃣ PHÂN LOẠI SỐ
# =========================
def phan_loai(ds_so):
    n = len(ds_so)
    if n == 2:
        return "2CB"
    elif n == 3:
        return "3CB"
    else:
        return "3CXC"


# =========================
# 5️⃣ XỬ LÝ TIN NHẮN
# =========================
def xu_ly_tin(update, context):
    user_id = update.message.from_user.id
    text = update.message.text.lower()

    if user_id not in KHACH:
        update.message.reply_text("❌ Bạn chưa được cấp quyền")
        return

    so_dai = lay_so_dai(text)

    # chọn bảng giá
    if so_dai == 1:
        bang_gia = KHACH[user_id]["MB"]
    else:
        bang_gia = KHACH[user_id]["THUONG"]

    tong = {
        "2CB": 0,
        "2CD": 0,
        "3CB": 0,
        "3CXC": 0,
        "DA": 0
    }

    lines = text.splitlines()

    for line in lines:
        parts = line.split()
        if not parts:
            continue

        # lấy danh sách số
        ds_so = [p for p in parts if p.isdigit()]
        so_con = len(ds_so)

        if so_con == 0:
            continue

        # ===== ĐÁ T =====
        if "đá" in parts or "da" in parts:
            try:
                idx = parts.index("đá") if "đá" in parts else parts.index("da")
                tien = float(parts[idx + 1])
                tien_an = so_con * tien * bang_gia["DA_T"]
                if so_dai > 1:
                    tien_an *= so_dai
                tong["DA"] += tien_an
            except:
                pass
            continue

        # ===== C / AB =====
        tien = 0
        for p in parts:
            if p.startswith("c"):
                tien = float(p.replace("c", ""))
            elif p.startswith("ab"):
                tien = float(p.replace("ab", ""))

        if tien == 0:
            continue
loai = phan_loai(ds_so)
        tien_an = so_con * tien * bang_gia[loai]
        if so_dai > 1:
            tien_an *= so_dai

        tong[loai] += tien_an

    # =========================
    # 6️⃣ TRẢ KẾT QUẢ
    # =========================
    tong_cong = sum(tong.values())

    msg = "✅ Đã nhận tin\n\n"
    msg += f"2CB: {tong['2CB']}\n"
    msg += f"2CD: {tong['2CD']}\n"
    msg += f"3CB: {tong['3CB']}\n"
    msg += f"3CXC: {tong['3CXC']}\n"
    msg += f"Đá: {tong['DA']}\n\n"
    msg += f"🍀 Tổng = {tong_cong}"

    update.message.reply_text(msg)


# =========================
# 7️⃣ CHẠY BOT
# =========================
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, xu_ly_tin))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
