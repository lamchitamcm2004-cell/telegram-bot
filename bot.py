from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8554596056:AAH6QcIj9ehxUW5Y37D8sOz1gse0QkCufXQ"

# USER ID của 2 khách (tạm để 0 – lát mình chỉ cách lấy)
KHACH_A = 0
KHACH_B = 0

def tinh_tien_cong_thuc_A(text):
    # ví dụ công thức A
    return 768

def tinh_tien_cong_thuc_B(text):
    # ví dụ công thức B
    return 1234

async def xu_ly_tin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    noi_dung = update.message.text

    if user_id == KHACH_A:
        tong = tinh_tien_cong_thuc_A(noi_dung)
        await update.message.reply_text(f"🍀 Tổng = {tong}")
    elif user_id == KHACH_B:
        tong = tinh_tien_cong_thuc_B(noi_dung)
        await update.message.reply_text(f"🍀 Tổng = {tong}")
    else:
        await update.message.reply_text("❌ Bạn không có quyền sử dụng bot")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xu_ly_tin))
app.run_polling()
