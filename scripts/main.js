
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
    
    // Start slideshow
    showSlides();
});