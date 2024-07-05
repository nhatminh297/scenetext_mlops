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
  const textArea = document.getElementsByClassName('text-display-area')[0]
  textArea.style.visibility = 'hidden'
  while (textArea.firstChild) {
    textArea.removeChild(textArea.lastChild);
  }

  let imgElement_1 = document.createElement("img");
  imgElement_1.src = src;
  imgElement_1.classList.add("uploaded-image");

  let column_1 = document.createElement("div");
  column_1.classList.add("column");
  column_1.appendChild(imgElement_1);

  let canvas = document.createElement("canvas")
  canvas.classList.add("bounding-box")

  let column_2 = document.createElement("div");
  column_2.classList.add("column");
  column_2.appendChild(canvas)


  imageDisplayArea.appendChild(column_1);
  imageDisplayArea.appendChild(column_2);
}

executeButton.onclick = async () => {
  const imgElement = document.querySelector(".uploaded-image");
  const imgSrc = imgElement.src;
  const modelOCR = document.getElementById('models_OCR').value
  if (imgSrc) {
    try {
      const formData = new FormData();
      const response = await fetch(imgSrc);
      const blob = await response.blob();
      formData.append("file", blob, "image.jpg");
      formData.append("model", modelOCR);
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
      console.log(result['prediction']);
      printDetectedText(result['prediction'])
      drawBoundingBoxes(result['prediction'])

    } catch (error) {
      console.error("Error during API call:", error);
    }
  } else {
    console.error("No file or image source selected.");
  }
}
function printDetectedText(detectedObjects) {
  const textArea = document.getElementsByClassName('text-display-area')[0]
  textArea.style.visibility = 'visible'
  detectedObjects.forEach((obj) => {
    text = obj[1]
    var word = document.createElement('p')
    word.innerHTML = text
    textArea.appendChild(word)
  });
}
function drawBoundingBoxes(detectedObjects) {
  const canvas = document.getElementsByClassName("bounding-box")[0];
  const context = canvas.getContext("2d");
  //const outputImage = document.getElementsByClassName("output-image");
  const uploadedImage = document.getElementsByClassName("uploaded-image")[0];

  const img = new Image();
  img.onload = function () {
    canvas.width = img.width;
    canvas.height = img.height;
    context.drawImage(img, 0, 0);

    detectedObjects.forEach((obj) => {
      drawBoundingBox(obj);
    });
  };
  img.src = uploadedImage.src;

  function drawBoundingBox(arr) {
    context.beginPath();
    points = arr[0];
    context.moveTo(points[0][0], points[0][1]);
    for (let i = 1; i < points.length; i++) {
      context.lineTo(points[i][0], points[i][1]);
    }
    context.closePath();
    context.lineWidth = 2;
    context.strokeStyle = "red";
    context.stroke();
    context.font = "Bold 13px Arial";
    context.fillStyle = "red";
    context.fillText(arr[1], points[0][0], points[0][1] - 10);
  }
  detectedObjects.forEach((obj) => {
    drawBoundingBox(obj);
  });
}