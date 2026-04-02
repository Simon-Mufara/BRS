
// Close modal when clicking outside
window.onclick = function(event) {
    const quoteModal = document.getElementById('quoteModal');
    if (event.target === quoteModal) {
        closeQuoteModal();
    }
};

// Quote Modal functions
function openQuoteModal() {
    const modal = document.getElementById('quoteModal');
    modal.style.display = 'block';
}

function openQuoteFromArea() {
    const areaSelect = document.getElementById('areaSelect').value;
    openQuoteModal();
    document.getElementById('area').value = areaSelect;
}

function openQuoteForService(serviceName) {
    openQuoteModal();
    document.getElementById('service').value = serviceName;
    showQuestions();
}

function closeQuoteModal() {
    const modal = document.getElementById('quoteModal');
    modal.style.display = 'none';
}

// Service-specific questions
const serviceQuestions = {
    'Painting': [
        { question: 'What type of painting do you need?', options: ['Interior', 'Exterior', 'Both'] },
        { question: 'How many rooms/areas need painting?', options: ['1-2', '3-5', 'More than 5'] },
        { question: 'Do you have a color scheme in mind?', options: ['Yes', 'No', 'Need suggestions'] },
        { question: 'Is there any surface preparation needed (e.g., peeling paint)?', options: ['Yes', 'No'] },
        { question: 'What is the approximate square meterage?', options: ['Under 50 sqm', '50-100 sqm', 'Over 100 sqm'] },
        { question: 'Any special finishes (e.g., gloss, matte)?', options: ['Yes', 'No'] }
    ],
    'Tiling': [
        { question: 'What type of tiling?', options: ['Floor', 'Wall', 'Both'] },
        { question: 'Material preference?', options: ['Ceramic', 'Porcelain', 'Natural Stone', 'Other'] },
        { question: 'Area size?', options: ['Small (under 10 sqm)', 'Medium (10-50 sqm)', 'Large (over 50 sqm)'] },
        { question: 'Is the surface prepared?', options: ['Yes', 'No'] },
        { question: 'Any patterns or designs?', options: ['Simple', 'Complex', 'Mosaic'] },
        { question: 'Waterproofing required?', options: ['Yes', 'No'] }
    ],
    'Plumbing': [
        { question: 'Type of plumbing issue?', options: ['Leak repair', 'Installation', 'Maintenance'] },
        { question: 'Affected area?', options: ['Kitchen', 'Bathroom', 'Outdoor', 'Whole house'] },
        { question: 'Urgency?', options: ['Immediate', 'Within a week', 'No rush'] },
        { question: 'Any visible damage?', options: ['Yes', 'No'] },
        { question: 'System type?', options: ['Residential', 'Commercial', 'Industrial'] },
        { question: 'Need new fixtures?', options: ['Yes', 'No'] }
    ],
    'Paving': [
        { question: 'Type of paving?', options: ['Driveway', 'Patio', 'Walkway'] },
        { question: 'Material?', options: ['Concrete', 'Brick', 'Stone', 'Asphalt'] },
        { question: 'Area size?', options: ['Under 50 sqm', '50-100 sqm', 'Over 100 sqm'] },
        { question: 'Existing surface?', options: ['Grass/Soil', 'Old paving', 'Concrete'] },
        { question: 'Drainage needs?', options: ['Yes', 'No'] },
        { question: 'Design preferences?', options: ['Simple', 'Patterned', 'Decorative'] }
    ],
    'Building': [
        { question: 'Type of building project?', options: ['New construction', 'Extension', 'Renovation'] },
        { question: 'Structure size?', options: ['Small', 'Medium', 'Large'] },
        { question: 'Materials preference?', options: ['Brick', 'Concrete', 'Steel', 'Wood'] },
        { question: 'Timeline?', options: ['Urgent', 'Within a week', 'Flexible'] },
        { question: 'Any architectural plans?', options: ['Yes', 'No'] },
        { question: 'Budget range?', options: ['Low', 'Medium', 'High'] }
    ],
    'Partition': [
        { question: 'Type of partition?', options: ['Drywall', 'Glass', 'Wooden'] },
        { question: 'Purpose?', options: ['Office division', 'Room separation', 'Decorative'] },
        { question: 'Height?', options: ['Full height', 'Half height'] },
        { question: 'Soundproofing needed?', options: ['Yes', 'No'] },
        { question: 'Fire rating required?', options: ['Yes', 'No'] },
        { question: 'Installation area?', options: ['Indoor', 'Outdoor'] }
    ],
    'Roofing': [
        { question: 'How steep is your roof?', options: ['All flat and walkable', 'Mostly flat with some steep areas', 'Mostly steep with some flat areas', 'All steep'] },
        { question: 'Type of roof?', options: ['Tile', 'Metal', 'Shingle', 'Flat'] },
        { question: 'Issue?', options: ['Repair', 'Replacement', 'New installation'] },
        { question: 'Size?', options: ['Small house', 'Medium house', 'Large building'] },
        { question: 'Any leaks?', options: ['Yes', 'No'] },
        { question: 'Insulation needed?', options: ['Yes', 'No'] }
    ],
    'Waterproofing': [
        { question: 'Area to waterproof?', options: ['Roof', 'Basement', 'Walls', 'Bathroom'] },
        { question: 'Method preference?', options: ['Membrane', 'Coating', 'Injection'] },
        { question: 'Severity of issue?', options: ['Minor dampness', 'Active leaks', 'Preventive'] },
        { question: 'Surface type?', options: ['Concrete', 'Brick', 'Wood'] },
        { question: 'Timeline?', options: ['Immediate', 'Soon', 'Flexible'] },
        { question: 'Warranty needed?', options: ['Yes', 'No'] }
    ],
    'Tiling & Paving': [
        { question: 'Focus area?', options: ['Tiling only', 'Paving only', 'Both'] },
        { question: 'Location?', options: ['Indoor', 'Outdoor'] },
        { question: 'Material?', options: ['Ceramic', 'Stone', 'Concrete'] },
        { question: 'Size?', options: ['Small', 'Medium', 'Large'] },
        { question: 'Design?', options: ['Simple', 'Patterned'] },
        { question: 'Preparation needed?', options: ['Yes', 'No'] }
    ],
    'Roofing & Windows': [
        { question: 'Focus?', options: ['Roofing', 'Windows', 'Both'] },
        { question: 'Window type?', options: ['Aluminum', 'Wood', 'uPVC'] },
        { question: 'Roof steepness?', options: ['Flat', 'Steep'] },
        { question: 'Number of windows?', options: ['1-5', '6-10', 'More'] },
        { question: 'Energy efficiency?', options: ['Yes', 'No'] },
        { question: 'Security features?', options: ['Yes', 'No'] }
    ],
    'Welding & Partitions': [
        { question: 'Focus?', options: ['Welding', 'Partitions', 'Both'] },
        { question: 'Material for welding?', options: ['Steel', 'Aluminum', 'Other'] },
        { question: 'Partition type?', options: ['Office', 'Industrial'] },
        { question: 'Size?', options: ['Small', 'Large'] },
        { question: 'Custom design?', options: ['Yes', 'No'] },
        { question: 'Timeline?', options: ['Urgent', 'Flexible'] }
    ],
    'Plumbing Services': [
        { question: 'Service type?', options: ['Installation', 'Repair', 'Maintenance'] },
        { question: 'System?', options: ['Water supply', 'Drainage', 'Heating'] },
        { question: 'Urgency?', options: ['Emergency', 'Standard'] },
        { question: 'Fixtures needed?', options: ['Yes', 'No'] },
        { question: 'Inspection required?', options: ['Yes', 'No'] },
        { question: 'Budget?', options: ['Low', 'High'] }
    ],
    'Building Installations': [
        { question: 'Installation type?', options: ['Electrical', 'HVAC', 'Structural'] },
        { question: 'Building size?', options: ['Small', 'Medium', 'Large'] },
        { question: 'New or existing?', options: ['New', 'Existing'] },
        { question: 'Compliance needs?', options: ['Yes', 'No'] },
        { question: 'Timeline?', options: ['Short', 'Long'] },
        { question: 'Custom features?', options: ['Yes', 'No'] }
    ],
    'Painting & Renovations': [
        { question: 'Focus?', options: ['Painting', 'Renovations', 'Both'] },
        { question: 'Scope?', options: ['Single room', 'Whole house'] },
        { question: 'Style?', options: ['Modern', 'Traditional'] },
        { question: 'Budget?', options: ['Low', 'Medium', 'High'] },
        { question: 'Timeline?', options: ['Quick', 'Extended'] },
        { question: 'Eco-friendly?', options: ['Yes', 'No'] }
    ],
    'Maintenance Work': [
        { question: 'Type of maintenance?', options: ['Preventive', 'Corrective'] },
        { question: 'Frequency?', options: ['One-time', 'Ongoing'] },
        { question: 'Areas?', options: ['Interior', 'Exterior', 'Both'] },
        { question: 'Specific issues?', options: ['Yes', 'No'] },
        { question: 'Contract needed?', options: ['Yes', 'No'] },
        { question: 'Budget?', options: ['Low', 'High'] }
    ]
};

// Show questions based on selected service
function showQuestions() {
    const service = document.getElementById('service').value;
    const questionsDiv = document.getElementById('questions');
    questionsDiv.innerHTML = '';
    questionsDiv.style.display = 'none';

    if (service && serviceQuestions[service]) {
        questionsDiv.style.display = 'block';
        serviceQuestions[service].forEach((q, index) => {
            const label = document.createElement('label');
            label.textContent = q.question;
            questionsDiv.appendChild(label);

            if (q.options) {
                const select = document.createElement('select');
                select.id = `q${index}`;
                q.options.forEach(opt => {
                    const option = document.createElement('option');
                    option.value = opt;
                    option.textContent = opt;
                    select.appendChild(option);
                });
                questionsDiv.appendChild(select);
            } else {
                const input = document.createElement('input');
                input.type = 'text';
                input.id = `q${index}`;
                questionsDiv.appendChild(input);
            }
        });
    }
}

/// Send quote email
function sendQuoteEmail() {
    const service = document.getElementById('service').value;
    const location = document.getElementById('location').value;
    const area = document.getElementById('area').value;
    const details = document.getElementById('details').value;
    const email = 'buildright.solutions.agency@gmail.com';

    // Generate reference number
    const refNumber = 'QUOTE-' + Date.now().toString(36).toUpperCase() + '-' + Math.random().toString(36).substr(2, 5).toUpperCase();

    // Formatted body with logo text, slogan, and nice structure
    let body = `******************************
     BuildRight Solutions
   We Nail It, You Enjoy It!


Quote Reference Number: ${refNumber}

Service: ${service || 'Not specified'}
Location: ${location || 'Not specified'}
Area: ${area || 'Not specified'}
Additional Details: ${details || 'None'}

Answers to Questions:
`;

    if (service && serviceQuestions[service]) {
        serviceQuestions[service].forEach((q, index) => {
            const answerElem = document.getElementById(`q${index}`);
            const answer = answerElem ? answerElem.value : 'Not answered';
            body += `- ${q.question}: ${answer}\n`;
        });
    }

    body += `
******************************
Thank you for your quote request!
We'll respond soon.

BuildRight Solutions - Johannesburg, Gauteng, ZA
Contact: 066 402 8544 | buildright.solutions.agency@gmail.com
******************************
`;

    const subject = `Quote Request [Ref: ${refNumber}] for ${service || 'Service'} in ${area || 'your area'}`;
    const mailtoLink = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    
    window.open(mailtoLink, '_blank');
    closeQuoteModal();
}

// Slideshow functionality
let slideIndex = 0;
let currentFilter = 'all';
let slideshowTimer;

function getVisibleSlides() {
    let slides = Array.from(document.querySelectorAll('#previous-work .slide'));
    if (currentFilter === 'all') {
        return slides;
    }
    return slides.filter(slide => slide.getAttribute('data-service') === currentFilter);
}

function showSlides() {
    let visibleSlides = getVisibleSlides();
    if (visibleSlides.length === 0) return;

    // Hide all slides first
    let allSlides = document.querySelectorAll('#previous-work .slide');
    allSlides.forEach(slide => slide.style.display = "none");

    // Ensure slideIndex is within bounds
    if (slideIndex <= 0) {
        slideIndex = 1;
    }
    if (slideIndex > visibleSlides.length) {
        slideIndex = 1;
    }

    // Show the current slide
    visibleSlides[slideIndex - 1].style.display = "block";

    // Auto-advance to next slide
    slideIndex++;
    
    if (slideshowTimer) clearTimeout(slideshowTimer);
    slideshowTimer = setTimeout(showSlides, 3000);
}

function filterSlideshow(service, button) {
    // Stop current slideshow
    if (slideshowTimer) {
        clearTimeout(slideshowTimer);
    }
    
    // Update filter
    currentFilter = service;
    slideIndex = 0; // Reset to 0 so showSlides() will start at 1
    
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    button.classList.add('active');
    
    // Restart slideshow with new filter
    showSlides();
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Filter button event listeners
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', function() {
            const service = this.getAttribute('data-filter');
            filterSlideshow(service, this);
        });
    });
    
    // Team section visibility handler
    const teamSection = document.getElementById('team');
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href === '#team') {
                // Show team section
                teamSection.classList.add('active');
            } else if (href === '#home' || href === '#services' || href === '#previous-work') {
                // Hide team section when navigating away
                teamSection.classList.remove('active');
            }
        });
    });
    
    // Hide team section by default on page load
    teamSection.classList.remove('active');
    
    // Make gallery images clickable to open in new tab
    document.querySelectorAll('#previous-work .slide img').forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            window.open(this.src, '_blank', 'noopener,noreferrer');
        });
        // Add hover title
        img.title = 'Click to view full size';
    });
    
    // FAQ Accordion functionality
    document.querySelectorAll('.faq-question').forEach(button => {
        button.addEventListener('click', function() {
            const faqItem = this.parentElement;
            const isActive = faqItem.classList.contains('active');
            
            // Close all FAQ items
            document.querySelectorAll('.faq-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Open clicked item if it wasn't active
            if (!isActive) {
                faqItem.classList.add('active');
            }
        });
    });
    
    // Testimonials Carousel functionality
    let testimonialIndex = 0;
    const testimonialTrack = document.querySelector('.testimonials-track');
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    const testimonialDotsContainer = document.querySelector('.testimonial-dots');
    let testimonialTimer;
    
    if (testimonialCards.length > 0) {
        // Create dots
        testimonialCards.forEach((_, index) => {
            const dot = document.createElement('span');
            dot.className = 'testimonial-dot';
            if (index === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToTestimonial(index));
            testimonialDotsContainer.appendChild(dot);
        });
        
        function goToTestimonial(index) {
            testimonialIndex = index;
            const offset = -100 * index;
            testimonialTrack.style.transform = `translateX(${offset}%)`;
            
            // Update dots
            document.querySelectorAll('.testimonial-dot').forEach((dot, i) => {
                dot.classList.toggle('active', i === index);
            });
        }
        
        function nextTestimonial() {
            testimonialIndex = (testimonialIndex + 1) % testimonialCards.length;
            goToTestimonial(testimonialIndex);
        }
        
        // Auto-scroll every 15 seconds
        function startTestimonialCarousel() {
            testimonialTimer = setInterval(nextTestimonial, 15000);
        }
        
        // Pause on hover, resume on mouse leave
        testimonialTrack.addEventListener('mouseenter', () => {
            clearInterval(testimonialTimer);
        });
        
        testimonialTrack.addEventListener('mouseleave', () => {
            startTestimonialCarousel();
        });
        
        startTestimonialCarousel();
    }
    
    // Start slideshow
    showSlides();
});
// FAQ Modal System
const faqContent = {
    areas: {
        title: "What areas do you serve?",
        content: <p>BuildRight Solutions proudly serves the entire Gauteng province and surrounding areas. Our primary service areas include:</p>
        <ul style="color: #666; line-height: 2;">
            <li><strong>Johannesburg:</strong> CBD, Sandton, Rosebank, Randburg, Bryanston, Rivonia, Morningside</li>
            <li><strong>West Rand:</strong> Roodepoort, Honeydew, Zandspruit, Florida</li>
            <li><strong>East Rand:</strong> Bedfordview, Edenvale, Alberton, Germiston, Boksburg, Benoni</li>
            <li><strong>North:</strong> Midrand, Fourways, Centurion, Pretoria</li>
            <li><strong>South:</strong> Soweto and surrounding townships</li>
        </ul>
        <p>We also service surrounding areas beyond Gauteng for larger projects. Contact us to confirm service availability in your area!</p>
    },
    quotes: {
        title: "Do you offer free quotes?",
        content: <p><strong>Yes, absolutely!</strong> We provide free, no-obligation quotes for all our services.</p>
        <p><strong>Our Quotation Process:</strong></p>
        <ol style="color: #666; line-height: 2;">
            <li><strong>Request:</strong> Submit your quote request through our website, WhatsApp, or phone</li>
            <li><strong>Assessment:</strong> We review your requirements and may schedule a site visit if needed</li>
            <li><strong>Quote Delivery:</strong> You receive a detailed, transparent quote within 24-48 hours</li>
            <li><strong>No Pressure:</strong> Take your time to review - no obligation to proceed</li>
        </ol>
        <p>All quotes include itemized costs, project timeline, and clear terms. We never charge for quotes!</p>
    },
    timeline: {
        title: "How long does a typical project take?",
        content: <p>Project timelines vary based on scope and complexity:</p>
        <h3 style="color: #000; margin-top: 20px;">Typical Timeframes:</h3>
        <ul style="color: #666; line-height: 2;">
            <li><strong>Small Repairs:</strong> Same day to 2 days (plumbing fixes, small painting jobs)</li>
            <li><strong>Medium Projects:</strong> 3-7 days (room painting, tiling, minor renovations)</li>
            <li><strong>Large Projects:</strong> 2-8 weeks (full renovations, building extensions, major roofing)</li>
        </ul>
        <p><strong>Factors affecting timeline:</strong></p>
        <ul style="color: #666; line-height: 1.8;">
            <li>Project complexity and size</li>
            <li>Weather conditions (for outdoor work)</li>
            <li>Material availability</li>
            <li>Client-requested changes</li>
        </ul>
        <p>We provide accurate timelines in every quote and keep you updated throughout the project.</p>
    },
    licensed: {
        title: "Are you licensed and insured?",
        content: <p><strong>Yes!</strong> BuildRight Solutions is fully registered, licensed, and insured.</p>
        <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <p style="margin: 0;"><strong>Company Registration Number:</strong> 2026/110944/07</p>
        </div>
        <p><strong>Our Credentials:</strong></p>
        <ul style="color: #666; line-height: 2;">
            <li>Registered with CIPC (Companies and Intellectual Property Commission)</li>
            <li>Comprehensive liability insurance coverage</li>
            <li>Compliance with all South African building regulations</li>
            <li>Adherence to Occupational Health and Safety Act requirements</li>
            <li>Proper permits and documentation for all projects</li>
        </ul>
        <p>We operate with complete transparency and professionalism. All documentation is available upon request.</p>
    },
    emergency: {
        title: "Do you handle emergency repairs?",
        content: <p><strong>Yes!</strong> We offer emergency repair services for urgent situations.</p>
        <h3 style="color: #000; margin-top: 20px;">Emergency Services Include:</h3>
        <ul style="color: #666; line-height: 2;">
            <li><strong>Plumbing Emergencies:</strong> Burst pipes, major leaks, geyser failures</li>
            <li><strong>Roof Emergencies:</strong> Storm damage, major leaks, structural issues</li>
            <li><strong>Electrical Issues:</strong> Safety hazards, power failures</li>
            <li><strong>Structural Damage:</strong> Immediate safety concerns</li>
        </ul>
        <p><strong>How to request emergency service:</strong></p>
        <ol style="color: #666; line-height: 2;">
            <li>Call us immediately: <strong>066 402 8544</strong></li>
            <li>WhatsApp for fastest response: <strong>062 055 2382</strong></li>
            <li>Describe the emergency clearly</li>
            <li>Our team will respond ASAP</li>
        </ol>
        <p style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffd700;">
            <strong>Note:</strong> Emergency services may incur additional call-out fees due to urgency and after-hours availability.
        </p>
    },
    payment: {
        title: "What payment methods do you accept?",
        content: <p>We offer flexible payment options for your convenience:</p>
        <h3 style="color: #000; margin-top: 20px;">Accepted Payment Methods:</h3>
        <ul style="color: #666; line-height: 2;">
            <li><strong>Bank Transfer (EFT):</strong> Direct deposit to our business account</li>
            <li><strong>Cash:</strong> Cash payments accepted on-site</li>
            <li><strong>Mobile Payments:</strong> SnapScan, Zapper, and other mobile payment platforms</li>
            <li><strong>Cheque:</strong> For larger commercial projects</li>
        </ul>
        <h3 style="color: #000; margin-top: 20px;">Payment Terms:</h3>
        <ul style="color: #666; line-height: 2;">
            <li><strong>Deposit:</strong> 30-50% upfront for materials and scheduling</li>
            <li><strong>Progress Payments:</strong> For larger projects, staged payments as work progresses</li>
            <li><strong>Final Payment:</strong> Upon project completion and your satisfaction</li>
        </ul>
        <p>All payment terms are clearly outlined in your quote. We believe in transparent pricing with no hidden fees.</p>
    },
    warranty: {
        title: "Do you provide warranties on your work?",
        content: <p><strong>Yes!</strong> We stand behind the quality of our work with comprehensive warranties.</p>
        <h3 style="color: #000; margin-top: 20px;">Warranty Coverage:</h3>
        <ul style="color: #666; line-height: 2;">
            <li><strong>Workmanship Warranty:</strong> 6 months to 2 years depending on service type</li>
            <li><strong>Material Warranty:</strong> As per manufacturer specifications (often 1-10 years)</li>
            <li><strong>Structural Work:</strong> Extended warranties available for major projects</li>
        </ul>
        <h3 style="color: #000; margin-top: 20px;">What's Covered:</h3>
        <ul style="color: #666; line-height: 2;">
            <li>Defects in workmanship</li>
            <li>Material failures (manufacturer warranty)</li>
            <li>Installation issues</li>
            <li>Premature wear under normal use</li>
        </ul>
        <h3 style="color: #000; margin-top: 20px;">What's Not Covered:</h3>
        <ul style="color: #666; line-height: 2;">
            <li>Damage from misuse or neglect</li>
            <li>Normal wear and tear</li>
            <li>Accidental damage</li>
            <li>Modifications by third parties</li>
        </ul>
        <p>Specific warranty terms are provided in writing with every project quote.</p>
    },
    planning: {
        title: "Can you help with project planning and design?",
        content: <p><strong>Absolutely!</strong> We offer comprehensive consultation and planning services.</p>
        <h3 style="color: #000; margin-top: 20px;">Our Planning Services Include:</h3>
        <ul style="color: #666; line-height: 2;">
            <li><strong>Initial Consultation:</strong> Discuss your vision, needs, and budget</li>
            <li><strong>Site Assessment:</strong> Evaluate existing conditions and constraints</li>
            <li><strong>Design Recommendations:</strong> Suggest optimal solutions and materials</li>
            <li><strong>Budget Planning:</strong> Help maximize value within your budget</li>
            <li><strong>Timeline Development:</strong> Create realistic project schedules</li>
            <li><strong>Material Selection:</strong> Guide you through choosing the best materials</li>
        </ul>
        <h3 style="color: #000; margin-top: 20px;">Design Assistance:</h3>
        <ul style="color: #666; line-height: 2;">
            <li>Color scheme recommendations</li>
            <li>Layout optimization</li>
            <li>Modern design trends</li>
            <li>Energy-efficient solutions</li>
            <li>Space-saving ideas</li>
        </ul>
        <p>Our experienced team brings 10+ years of combined expertise to help you achieve the best results for your project.</p>
    }
};

function openFAQModal(faqId) {
    const modal = document.getElementById('faqModal');
    const title = document.getElementById('faqModalTitle');
    const content = document.getElementById('faqModalContent');
    
    if (faqContent[faqId]) {
        title.textContent = faqContent[faqId].title;
        content.innerHTML = faqContent[faqId].content;
        modal.style.display = 'block';
    }
}

function closeFAQModal() {
    const modal = document.getElementById('faqModal');
    modal.style.display = 'none';
}

// Close FAQ modal when clicking outside
window.addEventListener('click', function(event) {
    const faqModal = document.getElementById('faqModal');
    if (event.target === faqModal) {
        closeFAQModal();
    }
});

// Enhanced Quote System with Image Upload
let currentStep = 1;
let uploadedImages = [];

function goToStep(stepNumber) {
    // Validate current step before proceeding
    if (stepNumber > currentStep) {
        if (currentStep === 1 && !validateStep1()) {
            return;
        }
    }
    
    // Hide all steps
    document.querySelectorAll('.quote-step-content').forEach(step => {
        step.style.display = 'none';
    });
    
    // Show target step
    document.getElementById('step' + stepNumber).style.display = 'block';
    
    // Update step indicators
    document.querySelectorAll('.step').forEach((step, index) => {
        step.classList.remove('active', 'completed');
        if (index + 1 < stepNumber) {
            step.classList.add('completed');
        } else if (index + 1 === stepNumber) {
            step.classList.add('active');
        }
    });
    
    currentStep = stepNumber;
    
    // If going to step 3, generate review
    if (stepNumber === 3) {
        generateQuoteReview();
    }
}

function validateStep1() {
    const service = document.getElementById('service').value;
    const location = document.getElementById('location').value;
    
    if (!service) {
        alert('Please select a service');
        return false;
    }
    if (!location) {
        alert('Please enter a location');
        return false;
    }
    return true;
}

function handleImageUpload(event) {
    const files = event.target.files;
    const maxFiles = 5;
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    if (uploadedImages.length + files.length > maxFiles) {
        alert('Maximum ' + maxFiles + ' images allowed');
        return;
    }
    
    Array.from(files).forEach(file => {
        if (file.size > maxSize) {
            alert(file.name + ' is too large. Maximum size is 5MB');
            return;
        }
        
        if (!file.type.startsWith('image/')) {
            alert(file.name + ' is not an image file');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            uploadedImages.push({
                name: file.name,
                data: e.target.result,
                size: file.size
            });
            displayImagePreview();
        };
        reader.readAsDataURL(file);
    });
}

function displayImagePreview() {
    const container = document.getElementById('imagePreviewContainer');
    container.innerHTML = '';
    
    uploadedImages.forEach((image, index) => {
        const div = document.createElement('div');
        div.className = 'image-preview-item';
        div.innerHTML = 
            <img src=" + image.data + " alt=" + image.name + ">
            <button class="image-remove-btn" onclick="removeImage( + index + )">×</button>
        ;
        container.appendChild(div);
    });
}

function removeImage(index) {
    uploadedImages.splice(index, 1);
    displayImagePreview();
}

function generateQuoteReview() {
    const service = document.getElementById('service').value;
    const location = document.getElementById('location').value;
    const details = document.getElementById('details').value;
    const reviewBox = document.getElementById('quoteReview');
    
    let reviewHTML = 
        <div class="review-item">
            <div class="review-label">Service Requested:</div>
            <div class="review-value"> + service + </div>
        </div>
        <div class="review-item">
            <div class="review-label">Location:</div>
            <div class="review-value"> + location + </div>
        </div>
    ;
    
    // Add service-specific questions
    if (serviceQuestions[service]) {
        let questionsHTML = '';
        serviceQuestions[service].forEach((q, index) => {
            const answerElem = document.getElementById('q' + index);
            if (answerElem) {
                questionsHTML += 
                    <div style="margin-bottom: 8px;">
                        <strong style="color: #000;"> + q.question + </strong><br>
                        <span style="color: #666;"> + answerElem.value + </span>
                    </div>
                ;
            }
        });
        if (questionsHTML) {
            reviewHTML += 
                <div class="review-item">
                    <div class="review-label">Service Details:</div>
                    <div class="review-value"> + questionsHTML + </div>
                </div>
            ;
        }
    }
    
    if (details) {
        reviewHTML += 
            <div class="review-item">
                <div class="review-label">Additional Details:</div>
                <div class="review-value"> + details + </div>
            </div>
        ;
    }
    
    if (uploadedImages.length > 0) {
        let imagesHTML = '<div class="review-images">';
        uploadedImages.forEach(image => {
            imagesHTML += '<img src="' + image.data + '" alt="Project photo">';
        });
        imagesHTML += '</div>';
        
        reviewHTML += 
            <div class="review-item">
                <div class="review-label">Uploaded Photos ( + uploadedImages.length + ):</div>
                <div class="review-value"> + imagesHTML + </div>
            </div>
        ;
    }
    
    reviewBox.innerHTML = reviewHTML;
}
