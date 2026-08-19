#!/bin/bash
# =============================================
# BUILD RIGHT SOLUTIONS - QUOTATION AGENT SETUP FOR CODESPACE
# =============================================
# RUN THIS ENTIRE SCRIPT IN YOUR GITHUB CODESPACE TERMINAL

echo "🚀 Setting up BuildRight Solutions Quotation Agent in Codespace..."

# Create the quotation agent directory
mkdir -p quotation-agent
cd quotation-agent

# Create all necessary files
echo "📄 Creating index.html..."
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
                                <option value="Partition">Partition</option