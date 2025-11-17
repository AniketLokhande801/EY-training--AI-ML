document.addEventListener("DOMContentLoaded", () => {
  // Show selected file name
  const fileInput = document.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.addEventListener("change", () => {
      const label = document.createElement("p");
      label.textContent = `Selected file: ${fileInput.files[0].name}`;
      fileInput.parentNode.insertBefore(label, fileInput.nextSibling);
    });
  }

  // Collect selected recipients into a hidden input
  const emailForm = document.getElementById("email-form");
  if (emailForm) {
    emailForm.addEventListener("submit", (e) => {
      const checkboxes = emailForm.querySelectorAll('input[name="recipients"]:checked');
      const selected = Array.from(checkboxes).map(cb => cb.value);
      const hiddenInput = document.createElement("input");
      hiddenInput.type = "hidden";
      hiddenInput.name = "recipients";
      hiddenInput.value = selected.join(",");
      emailForm.appendChild(hiddenInput);
    });
  }
});
document.addEventListener("DOMContentLoaded", () => {
  const analyzeForm = document.querySelector('form[action="/analyze_meeting/"]');
  const loading = document.getElementById("loading-animation");

  if (analyzeForm && loading) {
    analyzeForm.addEventListener("submit", () => {
      loading.style.display = "block";
    });
  }

  // Optional: hide animation after page reload
  window.addEventListener("pageshow", () => {
    if (loading) loading.style.display = "none";
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // Show loading animation on Analyze Transcript
  const analyzeForm = document.getElementById("analyze-form");
  const loading = document.getElementById("loading-animation");

  if (analyzeForm && loading) {
    analyzeForm.addEventListener("submit", () => {
      loading.style.display = "block";
    });
  }

  // Collect selected recipients into a hidden input
  const emailForm = document.getElementById("email-form");
  if (emailForm) {
    emailForm.addEventListener("submit", (e) => {
      const checkboxes = emailForm.querySelectorAll('input[name="recipients"]:checked');
      const selected = Array.from(checkboxes).map(cb => cb.value);
      const hiddenInput = document.createElement("input");
      hiddenInput.type = "hidden";
      hiddenInput.name = "recipients";
      hiddenInput.value = selected.join(",");
      emailForm.appendChild(hiddenInput);
    });
  }
})

