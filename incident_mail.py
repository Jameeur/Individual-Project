import smtplib
import os
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# These can be modified based on which sender and recipent alert will be sent
Server = "smtp.gmail.com"
Port = 465
Sender_Mail = "jameeur2006@gmail.com"
Wazuh_MailPass = os.environ.get("WAZUH_MAIL_PASS")
Recipient_Mail = "jameeur2006@gmail.com"

def send_alert(alert_json):
    try:
        rule_desc = alert_json.get('rule', {}).get('description', 'Security Alert')
        agent_name = alert_json.get('agent', {}).get('name', 'Unknown Agent')
        src_ip = alert_json.get('data', {}).get('srcip', 'Unknown IP')
        timestamp = alert_json.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f" WAZUH ALERT: {rule_desc}"
        msg["From"] = Sender_Mail
        msg["To"] = Recipient_Mail

        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="border: 1px solid #d4d4d4; padding: 20px; border-radius: 5px; max-width: 600px;">
              <h2 style="color: #d9534f; margin-top: 0;">Security Event Detected</h2>
              <p><strong>Rule:</strong> {rule_desc}</p>
              <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><strong>Source IP</strong></td><td style="padding: 10px; border: 1px solid #ddd;">{src_ip}</td></tr>
                <tr><td style="padding: 10px; border: 1px solid #ddd;"><strong>Agent</strong></td><td style="padding: 10px; border: 1px solid #ddd;">{agent_name}</td></tr>
                <tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><strong>Time</strong></td><td style="padding: 10px; border: 1px solid #ddd;">{timestamp}</td></tr>
              </table>
              <p style="margin-top: 20px; font-size: 12px; color: #777;">Author: Jameeur Rahman</p>
            </div>
          </body>
        </html>
        """

        #Will send once message is done
        msg.attach(MIMEText(html, "html"))
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(Server, Port, context=context) as server:
            server.login(Sender_Mail, Wazuh_MailPass)
            server.sendmail(Sender_Mail, Recipient_Mail, msg.as_string())
            
        return True

    except Exception as e:
        print(f"Failed to send mail {e}")
        return False
