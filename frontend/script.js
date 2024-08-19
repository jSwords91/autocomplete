const userInput = document.getElementById('userInput');
const suggestions = document.getElementById('suggestions');

// Typing timer
let typingTimer;
const doneTypingInterval = 150; // ms -- trial and error here

// Event Listeners
userInput.addEventListener('input', handleInput);

// Input Handler
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

const debouncedGetPredictions = debounce(getPredictions, doneTypingInterval);

function handleInput() {
    if (userInput.value) {
        debouncedGetPredictions();
    } else {
        suggestions.innerHTML = '';
    }
}

// Fetch Predictions
function getPredictions() {
    console.log('Fetching predictions for:', userInput.value);
    fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: userInput.value })
    })
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Received predictions:', data.predictions);
            displaySuggestions(data.predictions);
        })
        .catch(error => {
            console.error('Error:', error);
            suggestions.innerHTML = `Error fetching predictions: ${error.message}`;
        });
}
// Display Suggestions
function displaySuggestions(predictions) {
    suggestions.innerHTML = predictions
        .map(([word, score]) => {
            const safeWord = word.replace(/'/g, "\\'");
            return `<div class="suggestion" onclick="applySuggestion('${safeWord}')">${word} (${(score * 100).toFixed(0)}%)</div>`;
        })
        .join('');
}
// Apply Suggestion
function applySuggestion(word) {
    const currentText = userInput.value;
    const cursorPosition = userInput.selectionStart;

    const newText = currentText.slice(0, cursorPosition) + word + currentText.slice(cursorPosition);
    userInput.value = newText;

    const newCursorPosition = cursorPosition + word.length;
    userInput.setSelectionRange(newCursorPosition, newCursorPosition);

    userInput.focus();
    handleInput();
}
