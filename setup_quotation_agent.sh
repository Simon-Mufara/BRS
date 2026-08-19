#!/bin/bash
# BuildRight Solutions Quotation Agent Setup Script
# Run this in GitHub Codespace to set up the quotation agent website

echo "🚀 Setting up BuildRight Solutions Quotation Agent..."

# Create directory if it doesn't exist
mkdir -p quotation-agent
cd quotation-agent

# Create index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BuildRight Solutions - Quotation Agent</title>
    <link rel="stylesheet" href="styles.css">
    <!-- EmailJS SDK - replace with your actual setup -->
    <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"></script>
</head>
<body>
    <!-- Header -->
    <header class="site-header">
        <div class="container">
            <div class="logo">
                <span class="logo-text">BUILD</span><span class="logo-text-alt">RIGHT</span>
            </div>
            <p class="tagline">"We Nail It, You Enjoy It!"</p>
            <div class="contact-info">
                <p><strong>Registration:</strong> 2026/110944/07</p>
                <p><strong>WhatsApp:</strong> 062 055 2382</p>
                <p><strong>Call:</strong> 066 402 8544</p>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container">
        <!-- Navigation Tabs -->
        <nav class="tabs">
            <button class="tab-btn active" data-tab="quotation">Quotation Agent</button>
            <button class="tab-btn" data-tab="enquiry">New Enquiry</button>
            <button class="tab-btn" data-tab="templates">Templates</button>
        </nav>

        <!-- Tab Content -->
        <div class="tab-content">
            <!-- Quotation Agent Tab -->
            <section id="quotation" class="tab-pane active">
                <h2>Instant Quotation Generator</h2>
                <p>Get a professional quotation in minutes with real-time pricing</p>

                <form id="quotation-form" class="quote-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="service-type">Service Type *</label>
                            <select id="service-type" required>
                                <option value="">Select service type...</option>
                                <option value="tiling">Tiling</option>
                                <option value="painting">Painting</option>
                                <option value="plumbing">Plumbing</option>
                                <option value="electrical">Electrical Work</option>
                                <option value="carpentry">Carpentry</option>
                                <option value="waterproofing">Waterproofing</option>
                                <option value="paving">Paving</option>
                                <option value="building">Building/Construction</option>
                                <option value="renovation">General Renovations</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="area">Area/Location *</label>
                            <input type="text" id="area" placeholder="e.g., Sandton, Randburg, Rosebank" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="dimensions">Dimensions/Area Size *</label>
                            <input type="text" id="dimensions" placeholder="e.g., 25m2 bathroom, 3 bedrooms, 50 linear meters" required>
                        </div>

                        <div class="form-group">
                            <label for="quality">Quality Level</label>
                            <select id="quality">
                                <option value="standard">Standard</option>
                                <option value="budget">Budget</option>
                                <option value="premium">Premium</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group full-width">
                        <label for="details">Additional Details</label>
                        <textarea id="details" rows="3" placeholder="Any specific requirements, materials preferences, or special notes..."></textarea>
                    </div>

                    <div class="form-actions">
                        <button type="button" id="generate-estimate" class="btn btn-primary">Generate Price Estimate</button>
                        <button type="button" id="submit-enquiry" class="btn btn-secondary">Send as Enquiry</button>
                    </div>
                </form>

                <!-- Estimate Results -->
                <div id="estimate-results" class="estimate-results hidden">
                    <h3>Price Estimate</h3>
                    <div class="estimate-summary">
                        <div class="estimate-item">
                            <span>Reference:</span>
                            <span id="estimate-ref">ENQ-{{date}}-{{random}}</span>
                        </div>
                        <div class="estimate-item">
                            <span>Service:</span>
                            <span id="estimate-service"></span>
                        </div>
                        <div class="estimate-item">
                            <span>Area:</span>
                            <span id="estimate-area"></span>
                        </div>
                        <div class="estimate-item">
                            <span>Dimensions:</span>
                            <span id="estimate-dimensions"></span>
                        </div>
                        <div class="estimate-item">
                            <span>Quality:</span>
                            <span id="estimate-quality"></span>
                        </div>
                    </div>

                    <div class="estimate-breakdown">
                        <h4>Breakdown</h4>
                        <div id="estimate-details"></div>

                        <div class="estimate-total">
                            <span>Subtotal:</span>
                            <span id="estimate-subtotal">R 0.00</span>
                        </div>
                        <div class="estimate-total">
                            <span>VAT (15%):</span>
                            <span id="estimate-vat">R 0.00</span>
                        </div>
                        <div class="estimate-total estimate-total-final">
                            <span>Total:</span>
                            <span id="estimate-total">R 0.00</span>
                        </div>
                    </div>

                    <div class="estimate-notes">
                        <p><em>* This is an estimate based on average market prices. Final quotation may vary based on site inspection and exact material selection.</em></p>
                        <p><em>* Labour estimates included where applicable. Materials pricing includes typical waste factors (10% for tiles, 5% for other materials).</em></p>
                    </div>

                    <button type="button" id="create-quotation" class="btn btn-success mt-3">Create Professional Quotation PDF</button>
                </div>
            </section>

            <!-- New Enquiry Tab -->
            <section id="enquiry" class="tab-pane">
                <h2>Submit Quote Request</h2>
                <p>Let us know what you need and we'll get back to you quickly</p>

                <form id="enquiry-form" class="enquiry-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="enq-name">Your Name *</label>
                            <input type="text" id="enq-name" required>
                        </div>

                        <div class="form-group">
                            <label for="enq-contact">Contact Number / WhatsApp *</label>
                            <input type="tel" id="enq-contact" placeholder="e.g., 082 123 4567" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="enq-service">Service Needed *</label>
                            <select id="enq-service" required>
                                <option value="">Select service...</option>
                                <option value="Painting">Painting</option>
                                <option value="Tiling">Tiling</option>
                                <option value="Plumbing">Plumbing</option>
                                <option value="Paving">Paving</option>
                                <option value="Building">Building</option>
                                <option value="Partition">Partition</option>
                                <option value="Roofing">Roofing</option>
                                <option value="Waterproofing">Waterproofing</option>
                                <option value="Solar">Solar Installation</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="enq-area">Location/Area *</label>
                            <select id="enq-area" required>
                                <option value="">Select area...</option>
                                <option value="Johannesburg">Johannesburg</option>
                                <option value="Randburg">Randburg</option>
                                <option value="Rosebank">Rosebank</option>
                                <option value="Sandton">Sandton</option>
                                <option value="Midrand">Midrand</option>
                                <option value="Bryanston">Bryanston</option>
                                <option value="Rivonia">Rivonia</option>
                                <option value="Morningside">Morningside</option>
                                <option value="Bedfordview">Bedfordview</option>
                                <option value="Edenvale">Edenvale</option>
                                <option value="Alberton">Alberton</option>
                                <option value="Germiston">Germiston</option>
                                <option value="Roodepoort">Roodepoort</option>
                                <option value="Pretoria">Pretoria</option>
                                <option value="Centurion">Centurion</option>
                                <option value="Soweto">Soweto</option>
                                <option value="Fourways">Fourways</option>
                                <option value="Other Gauteng">Other Gauteng Area</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group full-width">
                        <label for="enq-details">Job Details *</label>
                        <textarea id="enq-details" rows="4" placeholder="Describe the work needed, approximate size, any specific requirements..." required></textarea>
                    </div>

                    <div class="form-group">
                        <label for="enq-photos">Photos (Optional)</label>
                        <input type="file" id="enq-photos" accept="image/*" multiple>
                        <small>Max 5 photos, JPG/PNG under 5MB each</small>
                    </div>

                    <button type="submit" class="btn btn-primary">Send Quote Request</button>
                </form>

                <div id="enquiry-status" class="status-message hidden"></div>
            </section>

            <!-- Templates Tab -->
            <section id="templates" class="tab-pane">
                <h2>Quotation Templates & Examples</h2>
                <p>Start from real examples or use these as templates for your projects</p>

                <div class="templates-grid">
                    <!-- Template cards will be populated by JavaScript -->
                </div>

                <button type="button" id="load-more-templates" class="btn btn-outline mt-3">Load More Examples</button>
            </section>
        </div>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-info">
                    <p><strong>BuildRight Solutions</strong></p>
                    <p>Zandspruit, Honeydew, Roodepoort, Johannesburg, Gauteng, 2170</p>
                    <p>Mon–Thu 6am–6pm, Fri 8am–4pm, Sat 8am–2pm</p>
                </div>
                <div class="footer-links">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="#quotation">Quotation Agent</a></li>
                        <li><a href="#enquiry">New Enquiry</a></li>
                        <li><a href="#templates">Templates</a></li>
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>Contact Us</h4>
                    <p>📱 WhatsApp: 062 055 2382</p>
                    <p>📞 Call: 066 402 8544</p>
                    <p>✉️ Email: buildright.solutions.agency@gmail.com</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 BuildRight Solutions. All rights reserved.</p>
                <p>Registration No: 2026/110944/07</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>
EOF

# Create styles.css
cat > styles.css << 'EOF'
/* BuildRight Solutions - Quotation Agent Styles */
/* ------------------------------------------ */
/* Clean, professional design with brand colors */

/* CSS Reset & Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 16px;
    scroll-behavior: smooth;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f8f9fa;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
}

a {
    text-decoration: none;
    color: inherit;
}

ul {
    list-style: none;
}

img {
    max-width: 100%;
    height: auto;
}

/* Header Styles */
.site-header {
    background: linear-gradient(135deg, #1e1e2e 0%, #2b2b3d 100%);
    color: white;
    padding: 2rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.logo-text {
    font-size: 2.5rem;
    font-weight: bold;
    color: #16a085;
}

.logo-text-alt {
    font-size: 2.5rem;
    font-weight: bold;
    color: #e0e0e0;
}

.tagline {
    font-style: italic;
    color: #bdc3c7;
    margin-bottom: 1.5rem;
}

.contact-info {
    background: rgba(255,255,255,0.1);
    padding: 1rem;
    border-radius: 8px;
}

.contact-info p {
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
}

.contact-info strong {
    min-width: 100px;
    display: inline-block;
}

/* Main Content Styles */
main {
    padding: 3rem 0;
}

h2 {
    color: #2c3e50;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #ecf0f1;
}

p {
    margin-bottom: 1rem;
    color: #555;
}

/* Tab Navigation */
.tabs {
    display: flex;
    border-bottom: 2px solid #ecf0f1;
    margin-bottom: 2rem;
}

.tab-btn {
    background: none;
    border: none;
    padding: 1rem 1.5rem;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    color: #7f8c8d;
    transition: all 0.3s ease;
    position: relative;
}

.tab-btn:hover {
    color: #3498db;
}

.tab-btn.active {
    color: #2c3e50;
}

.tab-btn.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 2px;
    background: #16a085;
}

.tab-content {
    min-height: 400px;
}

.tab-pane {
    display: none;
    animation: fadeIn 0.5s ease;
}

.tab-pane.active {
    display: block;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Form Styles */
.quote-form, .enquiry-form {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

.form-row {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.form-group {
    flex: 1;
    margin-bottom: 1rem;
}

.form-group.full-width {
    flex: 100%;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #2c3e50;
    font-size: 0.95rem;
}

input, select, textarea {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid #ecf0f1;
    border-radius: 6px;
    font-size: 1rem;
    transition: all 0.3s ease;
    font-family: inherit;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #16a085;
    box-shadow: 0 0 0 3px rgba(22, 160, 134, 0.2);
}

textarea {
    resize: vertical;
    min-height: 80px;
}

select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%237f8c8d' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 12px;
    padding-right: 2.5rem;
}

/* Button Styles */
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    text-decoration: none;
}

.btn-primary {
    background: #16a085;
    color: white;
}

.btn-primary:hover {
    background: #1abc9c;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(22, 160, 134, 0.3);
}

.btn-secondary {
    background: #95a5a6;
    color: white;
}

.btn-secondary:hover {
    background: #bdc3c7;
}

.btn-success {
    background: #27ae60;
    color: white;
}

.btn-success:hover {
    background: #2ecc71;
}

.btn-outline {
    background: transparent;
    border: 2px solid #16a085;
    color: #16a085;
}

.btn-outline:hover {
    background: #16a085;
    color: white;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

/* Estimate Results */
.estimate-results {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-top: 2rem;
}

.estimate-summary {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #ecf0f1;
}

.estimate-item {
    display: flex;
    justify-content: space-between;
}

.estimate-item span:first-child {
    font-weight: 600;
    color: #7f8c8d;
}

.estimate-item span:last-child {
    color: #2c3e50;
}

.estimate-breakdown {
    margin-bottom: 1.5rem;
}

.estimate-breakdown h4 {
    margin-bottom: 1rem;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.estimate-breakdown h4::before {
    content: '';
    width: 4px;
    height: 16px;
    background: #16a085;
    border-radius: 2px;
}

#estimate-details {
    display: grid;
    gap: 0.75rem;
}

.estimate-detail-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem;
    background: #f8f9fa;
    border-radius: 4px;
    font-size: 0.95rem;
}

.estimate-detail-item:nth-child(even) {
    background: #ecf0f1;
}

.estimate-total {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem;
    font-size: 1.1rem;
    font-weight: 600;
    background: #f8f9fa;
    border-radius: 6px;
}

.estimate-total-final {
    background: #e8f8f5;
    border-top: 2px solid #16a085;
    font-size: 1.2rem;
    margin-top: 0.5rem;
}

.estimate-notes {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px dashed #ecf0f1;
    font-size: 0.9rem;
    color: #7f8c8d;
    line-height: 1.5;
}

.estimate-notes em {
    font-style: italic;
    color: #95a5a6;
}

/* Status Message */
.status-message {
    padding: 1rem;
    border-radius: 6px;
    margin-top: 1.5rem;
    text-align: center;
    font-weight: 600;
}

.status-message.success {
    background: #d5f5e3;
    color: #27ae60;
    border: 1px solid #a8e6cf;
}

.status-message.error {
    background: #fadbd8;
    color: #c0392b;
    border: 1px solid #ebc7c7;
}

.status-message.hidden {
    display: none;
}

/* Templates Grid */
.templates-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.template-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.template-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.template-header {
    background: #16a085;
    color: white;
    padding: 1.5rem;
}

.template-header h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.template-header p {
    margin: 0;
    font-size: 0.9rem;
    opacity: 0.9;
}

.template-body {
    padding: 1.5rem;
}

.template-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: #7f8c8d;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.template-meta span {
    background: #ecf0f1;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
}

.template-description {
    color: #555;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.template-actions {
    display: flex;
    gap: 0.5rem;
}

.template-actions .btn {
    flex: 1;
    padding: 0.75rem;
    font-size: 0.9rem;
}

/* Footer Styles */
.site-footer {
    background: #2c3e50;
    color: #ecf0f1;
    padding: 3rem 0;
    margin-top: 4rem;
}

.footer-content {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-info, .footer-links, .footer-contact {
    flex: 1;
    min-width: 250px;
}

.footer-info h4, .footer-links h4, .footer-contact h4 {
    margin-bottom: 1rem;
    color: #16a085;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.footer-info p {
    margin: 0.5rem 0;
    line-height: 1.6;
}

.footer-links ul {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.footer-links li a {
    color: #bdc3c7;
    transition: color 0.3s ease;
}

.footer-links li a:hover {
    color: #ecf0f1;
}

.footer-contact p {
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.95rem;
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid #34495e;
    color: #95a5a6;
    font-size: 0.9rem;
}

.footer-bottom p {
    margin: 0.5rem 0;
}

/* Responsive Design */
@media (max-width: 768px) {
    .form-row {
        flex-direction: column;
        gap: 0;
    }

    .logo {
        flex-direction: column;
        text-align: center;
    }

    .contact-info {
        text-align: center;
    }

    .contact-info p {
        justify-content: center;
    }

    .tabs {
        flex-wrap: wrap;
    }

    .tab-btn {
        flex: 1;
        text-align: center;
        padding: 0.75rem 1rem;
    }

    .footer-content {
        flex-direction: column;
    }
}

@media (max-width: 480px) {
    .container {
        padding: 0 10px;
    }

    h2 {
        font-size: 1.5rem;
    }

    .quote-form, .enquiry-form {
        padding: 1.5rem;
    }

    .site-header {
        padding: 1.5rem 0;
    }

    .logo-text {
        font-size: 2rem;
    }

    .logo-text-alt {
        font-size: 2rem;
    }
}
EOF

# Create script.js
cat > script.js << 'EOF'
/* BuildRight Solutions - Quotation Agent Script */
/* ------------------------------------------- */
/* Handles form interactions, price estimation, and notifications */

/* Configuration - Replace with your actual credentials */
const EMAILJS_PUBLIC_KEY  = "YOUR_EMAILJS_PUBLIC_KEY"; // TODO: Replace with your EmailJS public key
const EMAILJS_SERVICE_ID  = "YOUR_EMAILJS_SERVICE_ID"; // TODO: Replace with your EmailJS service ID
const EMAILJS_TEMPLATE_ID = "YOUR_EMAILJS_TEMPLATE_ID"; // TODO: Replace with your EmailJS template ID

const CALLMEBOT_PHONE  = "27620555123456"; // TODO: Replace with your WhatsApp number (country code, no + or 0)
const CALLMEBOT_APIKEY = "YOUR_CALLMEBOT_APIKEY"; // TODO: Replace with your CallMeBot API key

// Initialize EmailJS if available
if (window.emailjs) {
    emailjs.init(EMAILJS_PUBLIC_KEY);
}

// Price data for estimation (simplified - in production this would come from an API or database)
const PRICE_DATA = {
    tiling: {
        budget: { tiles: 250, adhesive: 45, grout: 35, waterproofing: 120 },
        standard: { tiles: 350, adhesive: 55, grout: 45, waterproofing: 150 },
        premium: { tiles: 500, adhesive: 70, grout: 60, waterproofing: 180 }
    },
    painting: {
        budget: { paint: 120, primer: 80, sandpaper: 20, masking: 15 },
        standard: { paint: 180, primer: 120, sandpaper: 30, masking: 25 },
        premium: { paint: 250, primer: 180, sandpaper: 40, masking: 35 }
    },
    plumbing: {
        budget: { pipes: 200, fittings: 150, fixtures: 800 },
        standard: { pipes: 280, fittings: 200, fixtures: 1200 },
        premium: { pipes: 350, fittings: 280, fixtures: 1800 }
    },
    electrical: {
        budget: { wiring: 150, outlets: 100, fixtures: 200 },
        standard: { wiring: 200, outlets: 150, fixtures: 300 },
        premium: { wiring: 280, outlets: 200, fixtures: 450 }
    },
    carpentry: {
        budget: { wood: 350, hardware: 80, finish: 120 },
        standard: { wood: 450, hardware: 120, finish: 180 },
        premium: { wood: 550, hardware: 180, finish: 250 }
    },
    waterproofing: {
        budget: { membrane: 180, compound: 120, primer: 60 },
        standard: { membrane: 220, compound: 150, primer: 80 },
        premium: { membrane: 280, compound: 180, primer: 100 }
    },
    paving: {
        budget: { pavers: 200, sand: 40, cement: 80, edging: 60 },
        standard: { pavers: 250, sand: 50, cement: 100, edging: 80 },
        premium: { pavers: 320, sand: 60, cement: 120, edging: 100 }
    },
    building: {
        budget: { bricks: 120, cement: 80, sand: 30, steel: 200 },
        standard: { bricks: 150, cement: 100, sand: 40, steel: 250 },
        premium: { bricks: 180, cement: 120, sand: 50, steel: 300 }
    },
    renovation: {
        budget: { demolition: 200, materials: 300, fixtures: 150 },
        standard: { demolition: 250, materials: 400, fixtures: 200 },
        premium: { demolition: 300, materials: 500, fixtures: 250 }
    }
};

// Waste factors for materials
const WASTE_FACTORS = {
    tiling: 0.10, // 10% waste for tiles
    painting: 0.15, // 15% waste for paint (spillage, overlap)
    plumbing: 0.05, // 5% waste for pipes/fittings
    electrical: 0.05, // 5% waste for wiring/conduit
    carpentry: 0.10, // 10% waste for wood
    waterproofing: 0.05, // 5% waste for membranes/compounds
    paving: 0.10, // 10% waste for pavers/blocks
    building: 0.05, // 5% waste for bricks/blocks
    renovation: 0.15 // 15% waste for mixed materials
};

// Labor rates per hour (ZAR)
const LABOR_RATES = {
    tiling: 180,
    painting: 150,
    plumbing: 220,
    electrical: 200,
    carpentry: 170,
    waterproofing: 160,
    paving: 160,
    building: 190,
    renovation: 180
};

// Estimated hours per unit (simplified)
const LABOR_HOURS = {
    tiling: { per: 'm2', hours: 0.8 }, // 0.8 hours per m2
    painting: { per: 'm2', hours: 0.6 }, // 0.6 hours per m2
    plumbing: { per: 'point', hours: 1.0 }, // 1 hour per plumbing point
    electrical: { per: 'point', hours: 0.8 }, // 0.8 hours per electrical point
    carpentry: { per: 'm2', hours: 0.5 }, // 0.5 hours per m2 (rough carpentry)
    waterproofing: { per: 'm2', hours: 0.4 }, // 0.4 hours per m2
    paving: { per: 'm2', hours: 0.7 }, // 0.7 hours per m2
    building: { per: 'm2', hours: 1.2 }, // 1.2 hours per m2 (wall building)
    renovation: { per: 'm2', hours: 1.0 } // 1 hour per m2 (general renovation)
};

/* DOM Elements */
const quotationForm = document.getElementById('quotation-form');
const enquiryForm = document.getElementById('enquiry-form');
const estimateResults = document.getElementById('estimate-results');
const estimateRef = document.getElementById('estimate-ref');
const estimateService = document.getElementById('estimate-service');
const estimateArea = document.getElementById('estimate-area');
const estimateDimensions = document.getElementById('estimate-dimensions');
const estimateQuality = document.getElementById('estimate-quality');
const estimateDetails = document.getElementById('estimate-details');
const estimateSubtotal = document.getElementById('estimate-subtotal');
const estimateVat = document.getElementById('estimate-vat');
const estimateTotal = document.getElementById('estimate-total');
const generateEstimateBtn = document.getElementById('generate-estimate');
const submitEnquiryBtn = document.getElementById('submit-enquiry');
const createQuotationBtn = document.getElementById('create-quotation');
const enquiryStatus = document.getElementById('enquiry-status');
const templatesGrid = document.querySelector('.templates-grid');
const loadMoreTemplatesBtn = document.getElementById('load-more-templates');

/* Tab Switching */
document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', () => {
        const tabId = button.getAttribute('data-tab');

        // Update active tab button
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        button.classList.add('active');

        // Show active tab content
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(tabId).classList.add('active');
    });
});

/* Quotation Form Handling */
quotationForm.addEventListener('submit', (e) => {
    e.preventDefault();
});

generateEstimateBtn.addEventListener('click', generatePriceEstimate);
submitEnquiryBtn.addEventListener('click', submitAsEnquiry);
createQuotationBtn.addEventListener('click', createProfessionalQuotation);

enquiryForm.addEventListener('submit', handleEnquirySubmit);

/* Generate Price Estimate */
function generatePriceEstimate() {
    // Get form values
    const serviceType = document.getElementById('service-type').value;
    const area = document.getElementById('area').value;
    const dimensions = document.getElementById('dimensions').value;
    const quality = document.getElementById('quality').value;
    const details = document.getElementById('details').value;

    // Validate
    if (!serviceType || !area || !dimensions) {
        showError('Please fill in all required fields');
        return;
    }

    // Generate reference number
    const refNumber = generateReferenceNumber();
    estimateRef.textContent = refNumber;

    // Update summary
    estimateService.textContent = capitalizeFirstLetter(serviceType);
    estimateArea.textContent = area;
    estimateDimensions.textContent = dimensions;
    estimateQuality.textContent = capitalizeFirstLetter(quality);

    // Calculate estimate
    const estimate = calculateEstimate(serviceType, dimensions, quality, details);

    // Display breakdown
    displayEstimateBreakdown(estimate.breakdown);

    // Update totals
    estimateSubtotal.textContent = formatCurrency(estimate.subtotal);
    estimateVat.textContent = formatCurrency(estimate.vat);
    estimateTotal.textContent = formatCurrency(estimate.total);

    // Show results
    estimateResults.classList.remove('hidden');

    // Scroll to results
    estimateResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* Calculate Estimate */
function calculateEstimate(serviceType, dimensions, quality, details) {
    // Parse dimensions to extract area/quantity
    const areaValue = extractAreaValue(dimensions);
    const wasteFactor = WASTE_FACTORS[serviceType] || 0.1;
    const laborRate = LABOR_RATES[serviceType] || 150;
    const laborHours = LABOR_HOURS[serviceType]?.hours || 0.5;
    const laborPer = LABOR_HOURS[serviceType]?.per || 'm2';

    // Get base prices for service type and quality
    const basePrices = PRICE_DATA[serviceType]?.[quality] || PRICE_DATA[serviceType]?.standard || {};

    // Calculate material costs
    let materialCost = 0;
    const breakdownItems = [];

    for (const [item, pricePerUnit] of Object.entries(basePrices)) {
        // Calculate quantity needed (this is simplified - real implementation would be more complex)
        let quantity = areaValue;

        // Adjust quantity based on item type (simplified logic)
        if (item.includes('tile') || item === 'tiles') {
            quantity = areaValue * (1 + wasteFactor); // Add waste factor
        } else if (item.includes('paint') || item === 'primer' || item.includes('sandpaper')) {
            quantity = areaValue * (1 + WASTE_FACTORS.painting); // Paint waste factor
        } else if (item.includes('pipe') || item.includes('fitting') || item === 'fixtures') {
            quantity = areaValue * 0.5; // Simplified: 0.5 points per m2
        } else if (item.includes('wire') || item.includes('outlet') || item === 'fixtures') {
            quantity = areaValue * 0.3; // Simplified: 0.3 points per m2
        } else if (item.includes('wood') || item === 'hardware' || item === 'finish') {
            quantity = areaValue * 0.8; // Simplified: 0.8 m2 per m2 area
        } else if (item.includes('membrane') || item.includes('compound') || item.includes('primer')) {
            quantity = areaValue * (1 + WASTE_FACTORS.waterproofing); // Waterproofing waste
        } else if (item.includes('paver') || item.includes('sand') || item.includes('cement') || item === 'edging') {
            quantity = areaValue * (1 + WASTE_FACTORS.paving); // Paving waste
        } else if (item.includes('brick') || item.includes('cement') || item.includes('sand') || item === 'steel') {
            quantity = areaValue * 0.5; // Simplified: 0.5 units per m2 for building
        } else {
            quantity = areaValue; // Default
        }

        const itemCost = pricePerUnit * quantity;
        materialCost += itemCost;

        breakdownItems.push({
            name: formatItemName(item),
            quantity: quantity.toFixed(2) + ' m2',
            unitPrice: formatCurrency(pricePerUnit),
            total: formatCurrency(itemCost)
        });
    }

    // Calculate labor costs
    let laborQuantity = areaValue;
    if (laborPer === 'point') {
        laborQuantity = areaValue * 0.5; // Simplified conversion
    }

    const laborHoursTotal = laborQuantity * laborHours;
    const laborCost = laborHoursTotal * laborRate;

    breakdownItems.push({
        name: 'Labour',
        quantity: laborHoursTotal.toFixed(1) + ' hours',
        unitPrice: formatCurrency(laborRate) + '/hour',
        total: formatCurrency(laborCost)
    });

    // Calculate totals
    const subtotal = materialCost + laborCost;
    const vat = subtotal * 0.15; // 15% VAT
    const total = subtotal + vat;

    return {
        breakdown: breakdownItems,
        subtotal: subtotal,
        vat: vat,
        total: total
    };
}

/* Extract numeric area value from dimensions string */
function extractAreaValue(dimensions) {
    // Simple extraction - looks for numbers in the string
    const match = dimensions.match(/(\d+(?:\.\d+)?)\s*(?:m2|sqm|square\s*meters?)/i);
    if (match) {
        return parseFloat(match[1]);
    }

    // If no explicit area, try to get first number
    const numMatch = dimensions.match(/(\d+(?:\.\d+)?)/);
    if (numMatch) {
        return parseFloat(numMatch[1]);
    }

    // Default fallback
    return 10; // Assume 10 m2 if nothing found
}

/* Format item name for display */
function formatItemName(item) {
    return item
        .split(/(?=[A-Z])/)
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
        .replace(/([A-Z]+)/g, match => match.toLowerCase())
        .replace(/\b\w/g, char => char.toUpperCase());
}

/* Display estimate breakdown in the UI */
function displayEstimateBreakdown(breakdown) {
    estimateDetails.innerHTML = '';

    breakdown.forEach(item => {
        const div = document.createElement('div');
        div.className = 'estimate-detail-item';
        div.innerHTML = `
            <span>${item.name}</span>
            <div>
                <span>${item.quantity} × ${item.unitPrice}</span>
                <span>${item.total}</span>
            </div>
        `;
        estimateDetails.appendChild(div);
    });
}

/* Format currency */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-ZA', {
        style: 'currency',
        currency: 'ZAR',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

/* Generate reference number */
function generateReferenceNumber() {
    const datePart = new Date().toISOString().slice(0,10).replace(/-/g,'');
    const randomPart = Math.floor(Math.random() * 9000) + 1000; // 4-digit random
    return `ENQ-${datePart}-${randomPart}`;
}

/* Capitalize first letter */
function capitalizeFirstLetter(string) {
    if (!string) return '';
    return string.charAt(0).toUpperCase() + string.slice(1);
}

/* Show error message */
function showError(message) {
    alert(message); // Simple alert for now - could be enhanced
}

/* Submit as enquiry (uses EmailJS/CallMeBot) */
async function submitAsEnquiry() {
    // Get form values
    const serviceType = document.getElementById('service-type').value;
    const area = document.getElementById('area').value;
    const dimensions = document.getElementById('dimensions').value;
    const quality = document.getElementById('quality').value;
    const details = document.getElementById('details').value;
    const clientName = document.getElementById('q-client-name')?.value || "Not provided";
    const clientContact = document.getElementById('q-client-contact')?.value || "Not provided";

    // Validate
    if (!serviceType || !area || !dimensions) {
        showError('Please fill in all required fields');
        return;
    }

    // Show loading state
    submitEnquiryBtn.disabled = true;
    submitEnquiryBtn.textContent = 'Sending...';

    try {
        // Generate reference number
        const refNumber = generateReferenceNumber();

        // Prepare data for notifications
        const summary =
            `New enquiry ${refNumber}\n` +
            `Service: ${serviceType}\n` +
            `Area: ${area}\n` +
            `Client: ${clientName}\n` +
            `Contact: ${clientContact}\n` +
            `Details: ${details || "—"}\n` +
            `Dimensions: ${dimensions}\n` +
            `Quality: ${quality}`;

        // Send email via EmailJS
        if (window.emailjs) {
            try {
                await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, {
                    ref_number: refNumber,
                    service: serviceType,
                    area: area,
                    client_name: clientName,
                    client_contact: clientContact,
                    details: details || "—",
                    dimensions: dimensions,
                    quality: quality,
                    to_email: "buildright.solutions.agency@gmail.com"
                });
                console.log("Email notification sent.");
            } catch (emailErr) {
                console.error("Email send failed:", emailErr);
                // Continue with WhatsApp even if email fails
            }
        }

        // Send WhatsApp via CallMeBot
        try {
            const waUrl = `https://api.callmebot.com/whatsapp.php?phone=${CALLMEBOT_PHONE}` +
                          `&text=${encodeURIComponent(summary)}&apikey=${CALLMEBOT_APIKEY}`;
            await fetch(waUrl, { mode: "no-cors" });
            console.log("WhatsApp notification sent.");
        } catch (waErr) {
            console.error("WhatsApp send failed:", waErr);
        }

        // Save to localStorage as fallback
        const existing = JSON.parse(localStorage.getItem("brs_enquiries") || "[]");
        existing.push({
            ref: refNumber,
            service: serviceType,
            area: area,
            dimensions: dimensions,
            quality: quality,
            details: details,
            client_name: clientName,
            client_contact: clientContact,
            submittedAt: new Date().toISOString()
        });
        localStorage.setItem("brs_enquiries", JSON.stringify(existing));

        // Show success
        submitEnquiryBtn.disabled = false;
        submitEnquiryBtn.textContent = 'Send as Enquiry';
        alert(`Thanks! Your enquiry has been sent. Reference: ${refNumber}`);

        // Reset form
        quotationForm.reset();
        estimateResults.classList.add('hidden');

    } catch (error) {
        console.error("Submission failed:", error);
        submitEnquiryBtn.disabled = false;
        submitEnquiryBtn.textContent = 'Send as Enquiry';
        alert('Sorry, there was an error sending your enquiry. Please try again.');
    }
}

/* Handle enquiry form submission */
function handleEnquirySubmit(e) {
    e.preventDefault();

    // Get form values
    const name = document.getElementById('enq-name').value.trim();
    const contact = document.getElementById('enq-contact').value.trim();
    const service = document.getElementById('enq-service').value;
    const area = document.getElementById('enq-area').value;
    const details = document.getElementById('enq-details').value.trim();

    // Basic validation
    if (!name || !contact || !service || !area || !details) {
        enquiryStatus.textContent = 'Please fill in all required fields';
        enquiryStatus.className = 'status-message error';
        enquiryStatus.classList.remove('hidden');
        return;
    }

    // Show loading state
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';

    // Process enquiry (similar to submitAsEnquiry but for enquiry form)
    processEnquiry({
        name,
        contact,
        service,
        area,
        details
    }, submitBtn);
}

/* Process enquiry (shared logic) */
async function processEnquiry(formData, submitBtn) {
    try {
        // Generate reference number
        const refNumber = generateReferenceNumber();

        // Prepare summary
        const summary =
            `New enquiry ${refNumber}\n` +
            `Service: ${formData.service}\n` +
            `Area: ${formData.area}\n` +
            `Client: ${formData.name}\n` +
            `Contact: ${formData.contact}\n` +
            `Details: ${formData.details || "—"}`;

        // Send email via EmailJS
        if (window.emailjs) {
            try {
                await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, {
                    ref_number: refNumber,
                    service: formData.service,
                    area: formData.area,
                    client_name: formData.name,
                    client_contact: formData.contact,
                    details: formData.details || "—",
                    to_email: "buildright.solutions.agency@gmail.com"
                });
                console.log("Email notification sent.");
            } catch (emailErr) {
                console.error("Email send failed:", emailErr);
            }
        }

        // Send WhatsApp via CallMeBot
        try {
            const waUrl = `https://api.callmebot.com/whatsapp.php?phone=${CALLMEBOT_PHONE}` +
                          `&text=${encodeURIComponent(summary)}&apikey=${CALLMEBOT_APIKEY}`;
            await fetch(waUrl, { mode: "no-cors" });
            console.log("WhatsApp notification sent.");
        } catch (waErr) {
            console.error("WhatsApp send failed:", waErr);
        }

        // Save to localStorage
        const existing = JSON.parse(localStorage.getItem("brs_enquiries") || "[]");
        existing.push({
            ref: refNumber,
            ...formData,
            submittedAt: new Date().toISOString()
        });
        localStorage.setItem("brs_enquiries", JSON.stringify(existing));

        // Reset form and show success
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Quote Request';
        enquiryForm.reset();

        enquiryStatus.textContent = `Thanks! Your enquiry has been sent. Reference: ${refNumber}`;
        enquiryStatus.className = 'status-message success';
        enquiryStatus.classList.remove('hidden');

        // Hide status after 5 seconds
        setTimeout(() => {
            enquiryStatus.classList.add('hidden');
        }, 5000);

    } catch (error) {
        console.error("Enquiry submission failed:", error);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Quote Request';
        enquiryStatus.textContent = 'Sorry, there was an error sending your enquiry. Please try again.';
        enquiryStatus.className = 'status-message error';
        enquiryStatus.classList.remove('hidden');

        // Hide status after 5 seconds
        setTimeout(() => {
            enquiryStatus.classList.add('hidden');
        }, 5000);
    }
}

/* Create professional quotation (placeholder - would integrate with backend) */
function createProfessionalQuotation() {
    alert('This feature would generate a professional PDF quotation using your BRS Agent system.\nIn a full implementation, this would connect to your backend to create a polished PDF document.');
    // In reality, this would send data to your backend which would:
    // 1. Use your existing quotation.py generator
    // 2. Create a PDF with proper formatting
    // 3. Either download it or provide a link to download
}

/* Load templates (example data) */
function loadTemplates() {
    // Example templates - in reality these would come from your BRS examples.py or a database
    const templates = [
        {
            id: 1,
            title: "Bathroom Tiling",
            service: "Tiling",
            area: "Johannesburg",
            description: "Complete bathroom tiling with waterproofing",
            image: "https://via.placeholder.com/300x200"
        },
        {
            id: 2,
            title: "Living Room Painting",
            service: "Painting",
            area: "Randburg",
            description": "Interior painting of living room and hallway",
            image: "https://via.placeholder.com/300x200"
        },
        {
            id: 3,
            title: "Kitchen Plumbing",
            service: "Plumbing",
            area: "Sandton",
            description": "New kitchen plumbing installation",
            image: "https://via.placeholder.com/300x200"
        },
        {
            id: 4,
            title: "Bedroom Carpentry",
            service: "Carpentry",
            area: "Rosebank",
            description": "Built-in wardrobes and shelving",
            image: "https://via.placeholder.com/300x200"
        },
        {
            id: 5,
            title: "Driveway Paving",
            service: "Paving",
            area: "Pretoria",
            description": "Interlocking paver driveway installation",
            image: "https://via.placeholder.com/300x200"
        },
        {
            id: 6
        }
    ];

    // Clear and populate grid
    templatesGrid.innerHTML = '';

    templates.forEach(template => {
        const card = document.createElement('div');
        card.className = 'template-card';
        card.innerHTML = `
            <div class="template-header">
                <h3>${template.title}</h3>
                <p>${template.service} • ${template.area}</p>
            </div>
            <div class="template-body">
                <img src="${template.image}" alt="${template.title}" class="template-image">
                <p class="template-description">${template.description}</p>
                <div class="template-actions">
                    <button class="btn btn-primary" onclick="useTemplate(${template.id})">Use This Template</button>
                    <button class="btn btn-outline" onclick="viewTemplateDetails(${template.id})">View Details</button>
                </div>
            </div>
        `;
        templatesGrid.appendChild(card);
    });
}

/* Use template (populate quotation form) */
function useTemplate(templateId) {
    // Switch to quotation tab
    document.querySelector('.tab-btn[data-tab="quotation"]').click();

    // In a real implementation, this would populate the form with template data
    alert('Template loaded! In a full implementation, this would populate the form with the selected template data.');

    // For demo, just show a message
    const quotationForm = document.getElementById('quotation-form');
    quotationForm.reset();

    // Set some default values based on template
    if (templateId === 1) {
        document.getElementById('service-type').value = 'tiling';
        document.getElementById('area').value = 'Johannesburg';
        document.getElementById('dimensions').value = '5m2 bathroom';
        document.getElementById('quality').value = 'standard';
    }
    // ... other templates
}

/* View template details */
function viewTemplateDetails(templateId) {
    alert(`Viewing details for template ${templateId}\nIn a full implementation, this would show a modal with more information about this template.`);
}

/* Initialize page */
document.addEventListener('DOMContentLoaded', () => {
    // Load templates
    loadTemplates();

    // Add year to footer
    const yearElement = document.querySelector('.footer-bottom');
    if (yearElement) {
        const currentYear = new Date().getFullYear();
        yearElement.innerHTML = yearElement.innerHTML.replace('2026', currentYear);
    }

    // Check if we're on a mobile device and adjust accordingly
    if (window.innerWidth < 768) {
        // Mobile-specific adjustments could go here
    }
});
EOF

# Create README.md
cat > README.md << 'EOF'
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
EOF

# Go back to parent directory
cd ..

echo "✅ Setup complete! Files created in ./quotation-agent/ directory"
echo ""
echo "📝 Next Steps:"
echo "1. Edit quotation-agent/script.js to replace placeholder credentials with your actual EmailJS and CallMeBot values"
echo "2. Copy the files to your GitHub repository:"
echo "   cp quotation-agent/* /path/to/your/BRS/repo/"
echo "3. Commit and push to your GitHub repo"
echo "4. Configure GitHub Pages (if not already set):"
echo "   - Go to repo Settings → Pages"
echo "   - Source: main branch, / (root) folder"
echo "   - Save"
echo "5. Visit your site at https://your-username.github.io/BRS/"
echo ""
echo "🔑 To get your credentials:"
echo "   - EmailJS: Sign up at emailjs.com, connect Gmail, create service/template"
echo "   - CallMeBot: Save +34 644 84 71 04, WhatsApp that number: 'I allow callmebot to send me messages', get API key"
echo ""
echo "💡 Tip: You can run this setup script again anytime to reset or update the files"
EOF

# Make the script executable
chmod +x setup_quotation_agent.sh

echo ""
echo "🎉 Setup script created: setup_quotation_agent.sh"
echo "   Run it with: ./setup_quotation_agent.sh"
echo ""