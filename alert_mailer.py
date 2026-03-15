#!/usr/bin/env python3
import sys
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Constants defined, wazuh mail pass is hidden as it's my dummy account
Server = "smtp.gmail.com"
Port = 465
Sender_Mail = "jameeur2006@gmail.com"
Recipient_Mail = "jameeur2006@gmail.com"

# ONLY REVEAL IF NEEDED
Wazuh_MailPass = "sowkvybojrzxrhpa"


def send_alert(ip_address, target_user, rule_desc):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = MIMEMultipart("alternative")
        msg["Subject"] = " WINDOWS ALERT: SIEM Threat Detected"
        msg["From"] = Sender_Mail
        msg["To"] = Recipient_Mail

        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="border: 1px solid #d4d4d4; padding: 20px; border-radius: 5px; max-width: 600px;">
              <h2 style="color: #d9534f; margin-top: 0;">Security Event Detected</h2>
              <p><strong>Rule:</strong> {rule_desc}</p>
              <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><strong>Source IP</strong></td><td style="padding: 10px; border: 1px solid #ddd;">{ip_address}</td></tr>
                <tr><td style="padding: 10px; border: 1px solid #ddd;"><strong>Target User</strong></td><td style="padding: 10px; border: 1px solid #ddd;">{target_user}</td></tr>
                <tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><strong>Time</strong></td><td style="padding: 10px; border: 1px solid #ddd;">{timestamp}</td></tr>
              </table>
            </div>
          </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(Server, Port, context=context) as server:
            server.login(Sender_Mail, Wazuh_MailPass)
            server.sendmail(Sender_Mail, Recipient_Mail, msg.as_string())
            
    except Exception:
        pass

def main():
    try:
        line = sys.stdin.readline()
        if not line:
            return
        alert = json.loads(line)
        
        alert_data = alert.get("parameters", {}).get("alert", {})
        rule_desc = alert_data.get("rule", {}).get("description", "Unknown Rule")
        
        # Returns username and ip address from wazuh
        win_data = alert_data.get("data", {}).get("win", {}).get("eventdata", {})
        src_ip = win_data.get("ipAddress", "unknown")
        user = win_data.get("targetUserName", "unknown")
        
        if src_ip == "unknown" or not src_ip or src_ip == "-":
            src_ip = alert_data.get("data", {}).get("srcip", "Local/Unknown")
            user = alert_data.get("data", {}).get("dstuser", "Unknown")

        send_alert(src_ip, user, rule_desc)

    except Exception:
        pass

if __name__ == "__main__":
    main()
