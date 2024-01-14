import movieInfo from './movieinfo.js';

document.addEventListener("DOMContentLoaded", function () {
  const movieTitle = document.getElementById("movie-title");
  const chatMessages = document.getElementById("chat-messages");
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");
  const movieDropdown = document.getElementById("movie-dropdown");
  const movieThumbnail = document.getElementById("movie-thumbnail");
  const yearElement = document.getElementById("year");
  const directorElement = document.getElementById("director");
  const actorsElement = document.getElementById("actors");  
  const loadingSpinner = document.getElementsByClassName('loading-spinner')[0];
  loadingSpinner.style.display = 'none';
  var botColor = '#0000';

  sendButton.addEventListener("click", async function () {
    sendMessage();
  });

  messageInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });

  movieDropdown.addEventListener("change", function () {
    updateMovieInfo();
  });

  updateMovieInfo();

  async function updateMovieInfo() {
    chatMessages.innerHTML = "";    
    const selectedMovie = parseInt(movieDropdown.value) - 1;
    const movieData = movieInfo['movieInfo'][selectedMovie];
    movieThumbnail.style.backgroundImage = `url(${movieData.thumbnail})`;
    yearElement.textContent = movieData.year;
    directorElement.textContent = movieData.director;
    actorsElement.textContent = movieData.actors.join(", ");
    movieTitle.style.background = movieData.color;
    botColor = movieData.color;
  }

  async function sendMessage() {
    const userMessage = messageInput.value;
    appendMessage("User", userMessage);
    messageInput.value = "";
    toggleLoadingSpinner(true);
    try {
      const botResponse = await getBotResponse(userMessage);
      appendMessage("Chatbot", botResponse);
    } catch (error) {
      console.error("Error:", error);
      appendMessage("Chatbot", "An error occurred while processing your request.");
    } finally {
      toggleLoadingSpinner(false);
      messageInput.focus();
    }
  }

  async function getBotResponse(userMessage) {
    const selectedMovie = movieDropdown.value;
    const requestData = {
      FolderNumber: selectedMovie,
      Query: userMessage
    };

    try {
      const response = await fetch("https://x2ttd4pza57vkcw66avblr64ea0tyegv.lambda-url.us-east-1.on.aws/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
      });
      if (response.ok) {
        const responseData = await response.json();
        return responseData.message;
      } else {
        console.error("Error:", response.status, response.statusText);
        throw new Error("An error occurred while processing your request.");
      }
    } catch (error) {
      console.error("Error:", error.message);
      throw new Error("An error occurred while processing your request.");
    }
  }

  function appendMessage(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    if (sender == 'User'){
      messageElement.style.color = 'black';
    }
    else{
      messageElement.style.color = botColor;
    }
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function toggleLoadingSpinner(show) {    
    messageInput.disabled = show;
    sendButton.disabled = show;
  
    if (show) {
      loadingSpinner.style.display = 'flex';
    } else {
      loadingSpinner.style.display = 'none';
    }
  }

});
