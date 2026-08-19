# BuildRight Solutions - Quotation Agent Website

A professional website for BuildRight Solutions that provides:
- Interactive quotation agent with real-time price estimation
- Client enquiry submission via EmailJS and CallMeBot
- Access to quotation templates and examples
- Responsive design for mobile and desktop

## Features

### Quotation Agent Tab
- Interactive form for generating instant price estimates
- Real-time calculation based on service type, area, dimensions, and quality
- Detailed breakdown of material and labor costs
- Reference number generation for each estimate
- Option to send as enquiry or create professional PDF quotation

### New Enquiry Tab
- Client-facing form for submitting quote requests
- Collects contact information, service needed, location, and job details
- Optional photo uploads (client-side only in this version)
- Sends notifications to you via Email (EmailJS) and WhatsApp (CallMeBot)
- Saves enquiries locally as fallback

### Templates Tab
- Access to pre-built quotation templates
- Ability to use templates as starting points for new quotes
- Visual examples of different project types

## Setup Instructions

### 1. Deploy to GitHub Pages
1. Ensure all files are in the root directory:
   - `index.html`
   - `styles.css`
   - `script.js`
   - `README.md`
2. Push to your GitHub repository
3. Go to Repository Settings → Pages
4. Select source as `main` branch (or `master`)
5. Choose `/ (root)` as the folder
6. Click Save - your site will be published at `https://your-username.github.io/your-repo-name/`

### 2. Configure Notification Services
To make the notification system work, you need to set up:

#### EmailJS (for email notifications)
1. Sign up at [https://www.emailjs.com](https://www.emailjs.com)
2. Create an email service (connect your Gmail: buildright.solutions.agency@gmail.com)
3. Create an email template with these variables:
   - `ref_number`
   - `service`
   - `area`
   - `client_name`
   - `client_contact`
   - `details`
   - `dimensions`
   - `quality`
   - `to_email` (set to your email)
4. Get your:
   - **Public Key** (from Account → General)
   - **Service ID** (from Email Services)
   - **Template ID** (from Email Templates)
5. Replace the placeholder values in `script.js`:
   ```javascript
   const EMAILJS_PUBLIC_KEY  = "your_actual_public_key";
   const EMAILJS_SERVICE_ID  = "your_actual_service_id";
   const EMAILJS_TEMPLATE_ID = "your_actual_template_id";
   ```

#### CallMeBot (for WhatsApp notifications)
1. Save this number on your phone: **+34 644 84 71 04** (CallMeBot's number)
2. From YOUR WhatsApp (062 055 2382), send this exact message to that number:
   `I allow callmebot to send me messages`
3. You'll get a reply with your personal **API key** - copy it
4. In `script.js`, replace:
   ```javascript
   const CALLMEBOT_PHONE  = "27620552382"; // your WhatsApp number (country code, no + or 0)
   const CALLMEBOT_APIKEY = "your_actual_apikey";
   ```
   Note: Use your number in international format without + or leading 0 (e.g., 27620552382 for South Africa)

### 3. Customize for Your Business
- Update company information in `index.html` (header, footer, contact details)
- Modify service types and areas in the forms as needed
- Adjust pricing data in `script.js` if you have specific rates
- Update template examples in the `loadTemplates()` function

## How It Works

### Price Estimation
The quotation agent uses simplified pricing data and formulas to generate instant estimates:
- Material costs based on service type and quality level
- Waste factors applied appropriately (10% for tiles, 5% for other materials)
- Labor calculated based on industry-standard hours per unit
- VAT (15%) added to subtotal for total price

### Notifications
When a user submits an enquiry:
1. EmailJS sends an email to your Gmail with all enquiry details
2. CallMeBot sends a WhatsApp message to your phone with a summary
3. The enquiry is saved to the browser's localStorage as a fallback
4. Each enquiry gets a unique reference number (ENQ-YYYYMMDD-XXXX)

### Templates
The templates tab shows example quotations that users can use as starting points. In a full implementation, these would connect to your BRS Agent system's example data.

## File Structure
```
BRS-Quotation-Website/
├── index.html          # Main HTML structure
├── styles.css          # All styling and responsive design
├── script.js           # All functionality and logic
└── README.md           # This file
```

## Browser Support
- Chrome, Firefox, Safari, Edge (modern browsers)
- Mobile browsers (iOS Safari, Android Chrome)
- Requires JavaScript enabled for full functionality

## Future Enhancements
For a production implementation, consider:
1. **Backend Integration**: Connect to your BRS Agent system for:
   - Access to real quotation examples/templates
   - Generation of actual PDF documents
   - Storage of enquiries in a database
   - User authentication and history
2. **Enhanced Price Data**: Connect to live pricing APIs or databases
3. **Measurement Tools**: Add interactive area calculators
4. **Multi-language Support**: Add Afrikaans or other local languages
5. **Analytics**: Track usage and popular service types

## Troubleshooting

### Notifications Not Working
- Check browser console (F12) for error messages
- Verify EmailJS/CallMeBot credentials are correct
- Ensure you've sent the authorization message to CallMeBot
- Check that your email service is verified in EmailJS

### Layout Issues
- Ensure all files are properly uploaded
- Check for typos in class names or IDs
- Verify CSS is loaded before JavaScript runs

### Form Submission Problems
- Check that all required fields have values
- Verify JavaScript is not blocked by browser extensions
- Check network tab in dev tools for failed requests

## License
This website is provided for use with BuildRight Solutions. Feel free to customize and adapt it for your business needs.

---
*Developed to complement your existing BRS Agent desktop application*
