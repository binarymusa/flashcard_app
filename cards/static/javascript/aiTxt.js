
async function getAISummary(topicId, topicTitle){
    document.getElementById('modalTopicTitle').textContent = topicTitle;
    
    try{
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic_id: topicId,
                topic_title: topicTitle
            })
        })
        // .then(response => response.json())
        // .catch(error => console.log(error))
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        document.getElementById('aiSummaryContent').innerHTML = `
            <div class="summary-content">
                ${data.response}
            </div>`;
    }catch(error){
        document.getElementById('aiSummaryError').innerHTML = `
            <div class="alert alert-danger">
                Failed to load summary: ${error.message}
            </div>`;
    }
}