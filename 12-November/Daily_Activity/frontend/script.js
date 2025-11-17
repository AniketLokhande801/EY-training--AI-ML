const apiBase = "http://127.0.0.1:8000";

// --- Step 1: Analyze Meeting ---

document.getElementById("analyzeBtn").addEventListener("click", async () => {

  const fileInput = document.getElementById("fileInput");

  const loader = document.getElementById("loader");

  const resultBox = document.getElementById("analysisResult");

  if (!fileInput.files.length) {

    alert("Please upload a .docx file first!");

    return;

  }

  const formData = new FormData();

  formData.append("file", fileInput.files[0]);

  loader.classList.remove("hidden");

  resultBox.value = "";

  try {

    const response = await fetch(`${apiBase}/analyze_meeting/`, {

      method: "POST",

      body: formData,

    });

    const data = await response.json();

    if (data.status === "success") {

      resultBox.value = data.content;

    } else {

      resultBox.value = "❌ Error analyzing meeting.";

    }

  } catch (error) {

    resultBox.value = "❌ Server error. Please check your backend.";

  }

  loader.classList.add("hidden");

});

// --- Step 2: Send Email ---

document.getElementById("sendEmailBtn").addEventListener("click", async () => {

  const emails = document.getElementById("emailInput").value.trim();

  const content = document.getElementById("analysisResult").value;

  const emailStatus = document.getElementById("emailStatus");

  if (!emails || !content) {

    alert("Please provide recipient emails and analyze a meeting first!");

    return;

  }

  const formData = new FormData();

  formData.append("emails", emails);

  formData.append("content", content);

  emailStatus.innerHTML = "📨 Sending email...";

  try {

    const response = await fetch(`${apiBase}/send_emails/`, {

      method: "POST",

      body: formData,

    });

    const data = await response.json();

    if (data.status === "success") {

      emailStatus.innerHTML = "✅ Email sent successfully!";

      emailStatus.style.color = "green";

    } else {

      emailStatus.innerHTML = "❌ Email sending failed!";

      emailStatus.style.color = "red";

    }

  } catch (error) {

    emailStatus.innerHTML = "❌ Server error while sending email.";

    emailStatus.style.color = "red";

  }

});

