const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const fileUpload = document.getElementById("file-upload");
const fileName = document.getElementById("file-name");
const sendBtn = document.getElementById("send-btn");
const waitDiv = document.getElementById("responseWait");
let uploadedFile = null;
let uploaded = false;
// File upload handler
sendBtn.addEventListener("click", function () {});

fileUpload.addEventListener("change", function () {
  console.log("got it");
  if (this.files && this.files[0]) {
    uploadedFile = this.files[0];
    fileName.textContent = uploadedFile.name;

    if (!uploadedFile) {
      alert("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", uploadedFile);
    waitDiv.style.display = "block";
    fetch("/uploadFile", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((data) => {
        console.log("File uploaded successfully:", data);
        uploaded = true;
        waitDiv.style.display = "none";
        appendMessage(
          "bot",
          `File "${uploadedFile.name}" uploaded! Now you can ask questions about it.`
        );
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
});

// Chat form handler
chatForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (message) {
    waitDiv.style.display = "block";
    appendMessage("user", message);
    chatInput.value = "";
    console.log();
    fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message, uploaded }),
    })
      .then((response) => response.json())
      .then((data) => {
        waitDiv.style.display = "none";
        appendMessage("bot", data.response);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
});

// Append message to chat window
function appendMessage(sender, text) {
  const msgDiv = document.createElement("div");
  msgDiv.className = "msg " + sender;
  msgDiv.textContent = text;
  chatWindow.appendChild(msgDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
