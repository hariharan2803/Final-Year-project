document.getElementById('moodForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const ageInput = document.getElementById('moodInput').value;
    const age = parseInt(ageInput, 10); // Convert the input to an integer
    const recommendationsDiv = document.getElementById('recommendations'); // Reference to the recommendations div

    // Clear previous messages
    recommendationsDiv.textContent = ''; // Clear any previous messages

    // Check the age range and redirect accordingly
    if (age > 12 && age <= 30) {
        window.location.href = '/quiz'; // Redirect to quiz.html
    } else if (age > 30 && age <= 60) {
        window.location.href = '/quiz1'; // Redirect to quiz1.html
    } else if (age > 60 && age<=150) {
        window.location.href = '/quiz2'; // Redirect to quiz2.html
    } else if(age<=12 && age>0) {
        // Display error message in the recommendations div
        recommendationsDiv.textContent = 'Nothing to get stressed in this age, enjoy your life 😊!! ';
        recommendationsDiv.style.color = 'black'; // Change text color to black
        recommendationsDiv.style.marginTop = '10px'; // Add some space above the message
    }
    else {
        recommendationsDiv.textContent = 'Invalid age input, Enter valid age!!';
        recommendationsDiv.style.color = 'red'; // Change text color to black
        recommendationsDiv.style.marginTop = '10px'; // Add some space above the message
    } 
});


