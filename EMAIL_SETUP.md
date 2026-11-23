# Email Configuration Guide

This guide explains how to set up email notifications for your portfolio contact form.

## Overview

When someone fills out the contact form on your portfolio, the system:
1. ✅ Saves the message to the database (always happens)
2. ✉️ Sends an email notification to you (if configured)

## Quick Setup

### 1. Update Your `.env` File

Copy the email settings from `.env.example` and update with your details:

```env
# Enable email sending
MAIL_ENABLED=True

# Your email address (where you'll receive messages)
MAIL_TO=your-email@example.com

# SMTP settings (see provider-specific guides below)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_TLS=True
SMTP_SSL=False
```

### 2. Restart the Backend

After updating `.env`, restart your FastAPI server:

```bash
cd backend
python run.py
```

## Provider-Specific Setup

### Gmail

**Recommended for personal portfolios**

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Copy the generated password

3. Update your `.env`:
```env
MAIL_ENABLED=True
MAIL_TO=your-email@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
SMTP_TLS=True
SMTP_SSL=False
```

### Outlook / Hotmail

1. Update your `.env`:
```env
MAIL_ENABLED=True
MAIL_TO=your-email@outlook.com
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
SMTP_TLS=True
SMTP_SSL=False
```

### SendGrid (Recommended for Production)

**Best for deployed portfolios with high traffic**

1. Sign up at https://sendgrid.com (free tier: 100 emails/day)
2. Create an API Key
3. Update your `.env`:
```env
MAIL_ENABLED=True
MAIL_TO=your-email@example.com
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_TLS=True
SMTP_SSL=False
```

### Mailgun

1. Sign up at https://mailgun.com
2. Get your SMTP credentials from the dashboard
3. Update your `.env`:
```env
MAIL_ENABLED=True
MAIL_TO=your-email@example.com
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=your-mailgun-username
SMTP_PASSWORD=your-mailgun-password
SMTP_TLS=True
SMTP_SSL=False
```

### Custom SMTP Server

If you have your own SMTP server:

```env
MAIL_ENABLED=True
MAIL_TO=your-email@yourdomain.com
SMTP_HOST=mail.yourdomain.com
SMTP_PORT=587  # or 465 for SSL
SMTP_USERNAME=your-username
SMTP_PASSWORD=your-password
SMTP_TLS=True  # Set to False if using SSL
SMTP_SSL=False  # Set to True if using port 465
```

## Testing

### 1. Test from the Frontend

1. Start both backend and frontend
2. Navigate to the Contact section
3. Fill out and submit the form
4. Check your email inbox

### 2. Test Directly (API)

Using curl:

```bash
curl -X POST http://localhost:8000/api/v1/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Message",
    "message": "This is a test message from the contact form."
  }'
```

Or using the Postman collection provided in `backend/postman_collection.json`.

## Email Template

The email you receive will include:
- 📧 Sender's name and email (with Reply-To set automatically)
- 📝 Subject line (if provided)
- 💬 Message content
- 🎨 Nice HTML formatting with your portfolio brand colors

## Troubleshooting

### "Authentication failed"
- **Gmail**: Make sure you're using an App Password, not your regular password
- **Outlook**: Check that "less secure apps" is enabled
- **All**: Verify username and password are correct

### "Connection refused" or "Connection timeout"
- Check `SMTP_HOST` and `SMTP_PORT` are correct
- Ensure your firewall isn't blocking outbound SMTP
- Try using port 465 with `SMTP_SSL=True`

### "Emails not arriving"
- Check your spam/junk folder
- Verify `MAIL_TO` is correct
- Check backend logs for errors: `tail -f backend/logs/app.log`

### Form submits but no email
- If `MAIL_ENABLED=False`, emails won't be sent (by design)
- Check backend console for error messages
- Messages are still saved to the database even if email fails

## Viewing Stored Messages

Even without email, all contact form submissions are saved to the database. You can view them using the API:

```bash
# Get all messages
curl http://localhost:8000/api/v1/contact/messages

# Get unread messages only
curl http://localhost:8000/api/v1/contact/messages?is_read=false
```

## Production Recommendations

For deployed portfolios:

1. ✅ Use a dedicated email service (SendGrid, Mailgun, AWS SES)
2. ✅ Set up proper DNS records (SPF, DKIM, DMARC)
3. ✅ Use environment variables (never commit credentials)
4. ✅ Enable rate limiting on the contact endpoint
5. ✅ Add CAPTCHA to prevent spam

## Security Notes

- 🔒 Never commit `.env` files to version control
- 🔒 Use app-specific passwords instead of main account passwords
- 🔒 Rotate SMTP credentials periodically
- 🔒 Use HTTPS in production

## Need Help?

- Check backend logs for detailed error messages
- Test with `MAIL_ENABLED=False` first to ensure form submission works
- Verify SMTP settings with your email provider's documentation
