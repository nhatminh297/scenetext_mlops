const form = document.querySelector("form"),
  fileInput = document.querySelector(".file-input"),
  progressArea = document.querySelector(".progress-area"),
  uploadedArea = document.querySelector(".uploaded-area"),
  imageDisplayArea = document.querySelector(".image-display-area"),
  imageWithURL = document.querySelector(".url-button"),
  executeButton = document.querySelector(".extract-button");

form.addEventListener("click", () => {
  fileInput.click();
});

form.addEventListener("dragover", function (e) {
  e.preventDefault();
})

form.addEventListener("drop", function (e) {
  e.preventDefault();
  displayImageFromFile(e.dataTransfer.files[0])
})
fileInput.onchange = ({ target }) => {
  let file = target.files[0];
  if (file) {
    // Check if the file is an image
    if (!file.type.startsWith('image/')) {
      alert("Please upload an image file.");
      return;
    }

    let fileName = file.name;
    if (fileName.length >= 12) {
      let splitName = fileName.split('.');
      fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
    }
    displayImageFromFile(file);
  }
}

imageWithURL.addEventListener("click", () => {
  const url = document.querySelector(".url-input").value;
  if (url) {
    displayImageFromURL(url);
  }
});

function displayImageFromFile(file) {
  let reader = new FileReader();
  reader.onload = function (event) {
    displayImage(event.target.result);
  }
  reader.readAsDataURL(file);
}

function displayImageFromURL(url) {
  displayImage(url);
}

function displayImage(src) {
  // Clear the image display area
  imageDisplayArea.innerHTML = "";

  let imgElement = document.createElement("img");
  imgElement.src = src;
  imgElement.classList.add("uploaded-image");

  let column = document.createElement("div");
  column.classList.add("column");
  column.appendChild(imgElement);

  imageDisplayArea.appendChild(column);
}

executeButton.onclick = async () => {
  const imgElement = document.querySelector(".uploaded-image");
  const imgSrc = imgElement.src;
  const imgFile = imgElement.files ? imgElement.files[0] : null;

  if (imgFile || imgSrc) {
    try {
      const formData = new FormData();

      if (imgFile) {
        formData.append("file", imgFile);
      } else if (imgSrc) {
        const response = await fetch(imgSrc);
        const blob = await response.blob();
        formData.append("file", blob, "image.jpg");
      }

      const apiResponse = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
        headers: {
          "Accept": "application/json"
        }
      });

      if (!apiResponse.ok) {
        throw new Error("Failed to get a valid response from the server.");
      }

      const result = await apiResponse.json();
      console.log(result);
      // displayResult(result.prediction);
    } catch (error) {
      console.error("Error during API call:", error);
    }
  } else {
    console.error("No file or image source selected.");
  }
};
