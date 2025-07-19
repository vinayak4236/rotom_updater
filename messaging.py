import imaplib, smtplib, email, pywhatkit
from email.mime.text import MIMEText
from modules.speech_output import speak

# ---------- Gmail ----------
GMAIL_USER = "dinkukunbi@gmail.com"
GMAIL_PASS = "Vinayak@2005"   # 16-char app password, NOT real password

def fetch_unread_count() -> int:
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASS)
        mail.select("inbox")
        status, msgs = mail.search(None, "UNSEEN")
        mail.logout()
        return len(msgs[0].split()) if msgs[0] else 0
    except Exception as e:
        return 0

def read_latest_unread() -> str:
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASS)
        mail.select("inbox")
        status, msgs = mail.search(None, "UNSEEN")
        if not msgs[0]:
            mail.logout()
            return "No unread emails."
        latest = msgs[0].split()[-1]
        typ, data = mail.fetch(latest, "(RFC822)")
        raw = data[0][1]
        msg = email.message_from_bytes(raw)
        subject = msg["Subject"]
        frm = msg["From"]
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")
        mail.logout()
        return f"From {frm}, subject {subject}. Message: {body[:120]}..."
    except Exception as e:
        return f"Could not read email: {e}"

def send_email(to, subject, body):
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = to
        server.send_message(msg)
        server.quit()
        return f"Email sent to {to}"
    except Exception as e:
        return f"Could not send email: {e}"

# ---------- WhatsApp ----------
def send_whatsapp(phone: str, message: str) -> str:
    import pywhatkit, pyautogui, time
    pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=False)
    time.sleep(2)          # wait for the field to populate
    pyautogui.press("enter")  # send the message
    return f"WhatsApp sent to {phone}"