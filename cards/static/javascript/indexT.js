document.addEventListener('DOMContentLoaded', function() {

    const menuItems = document.querySelectorAll('[data-content]');
    const contentArea = document.getElementById('content-area');
    
    // Map content types to template files
    const templatePaths = {
        review: 'templates/includes/Review.html',
        add: 'templates/includes/decks.html',  
        chat: 'templates/includes/chat.html'
    };

    // Add click handlers to menu items
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const contentType = this.getAttribute('data-content');
            loadContent(contentType);
        });
    });

    async function loadContent(type) {
        try {
            // Check if template path exists
            if (!templatePaths[type]) {
                throw new Error(`No template defined for ${type}`);
            }
            
            // Fetch the HTML template
            const response = await fetch(templatePaths[type]);
            if (!response.ok) {
                throw new Error('Template not found');
            }
            const html = await response.text();
            
            // Replace the content area
            contentArea.innerHTML = html;
            contentArea.classList.add('active-content');
            
            // Initialize the loaded content
            initializeContent(type);
        } catch (error) {
            console.error('Error loading content:', error);
            contentArea.innerHTML = `
                <div class="alert alert-danger">
                    Error loading content: ${error.message}
                </div>
            `;
        }
    }

    function initializeContent(type) {
        switch(type) {
            case 'review':
                setupReviewContent();
                break;
            case 'add':
                setupAddContent();
                break;
            case 'chat':
                setupChatContent();
                break;
        }
    }

    // Setup functions for each content type
    function setupReviewContent() {
        // Initialize review content
        fetchReviewTopics();
    }

    function setupAddContent() {
        // Initialize add topic form
        document.getElementById('addTopicForm')?.addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = {
                title: document.getElementById('topicTitle').value.trim(),
                description: document.getElementById('topicDescription').value.trim(),
                category: document.getElementById('topicCategory').value,
                difficulty: document.getElementById('topicDifficulty').value
            };
    
            // Basic validation
            if (!formData.title) {
                alert('Topic title is required!');
                return;
            }
            try {
                const response = await fetch("{{ url_for('study.create_topic') }}", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        // Include CSRF token if you're using Flask-WTF
                        'X-CSRFToken': '{{ csrf_token() }}'
                    },
                    body: JSON.stringify(formData)
                });
    
                if (response.ok) {
                    const result = await response.json();
                    alert('Topic created successfully!');
                    // Optionally reset the form
                    this.reset();
                    // Optionally redirect or refresh content
                    loadContent('review'); // Refresh review section
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.error || 'Failed to create topic'}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Network error - please try again');
            }
        });
    }  
    
    function setupChatContent() {
        // Initialize chat functionality
        const chatInput = document.getElementById('chatInput');
        const sendButton = document.getElementById('sendMessage');
        
        sendButton?.addEventListener('click', async function() {
            // Your chat message handling
        });
    }

    // Your existing fetch functions...
    async function fetchReviewTopics() {
        try {
            const response = await fetch('/api/topics/review');
            const topics = await response.json();
            // Process and display topics
        } catch (error) {
            console.error('Error:', error);
        }
    }
});

