
const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");
const dropZone = document.getElementById("dropZone");
const fileInfo = document.getElementById("fileInfo");
const fileName = document.getElementById("fileName");
const fileSize = document.getElementById("fileSize");
const removeFile = document.getElementById("removeFile");
const uploadBtn = document.getElementById("uploadBtn");
const resultMessage = document.getElementById("resultMessage");

let selectedFile = null;

// Ouvrir le sélecteur de fichiers
browseBtn.addEventListener("click", () => {
    fileInput.click();
});

// Sélectionner un fichier
fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];

    if (file) {
        selectFile(file);
    }
});

// Vérifier et afficher le fichier
function selectFile(file) {
    const extension = file.name.split(".").pop().toLowerCase();

    if (!["csv", "json"].includes(extension)) {
        showMessage("Format non accepté. Utilisez CSV ou JSON.", "error");
        return;
    }

    selectedFile = file;

    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);

    fileInfo.classList.remove("hidden");
    uploadBtn.disabled = false;

    resultMessage.classList.add("hidden");
}

// Formater la taille du fichier
function formatFileSize(bytes) {
    if (bytes < 1024) {
        return bytes + " octets";
    }

    return (bytes / 1024).toFixed(2) + " Ko";
}

// Supprimer le fichier sélectionné
removeFile.addEventListener("click", () => {
    selectedFile = null;
    fileInput.value = "";

    fileInfo.classList.add("hidden");
    uploadBtn.disabled = true;

    resultMessage.classList.add("hidden");
});

// Glisser-déposer
dropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropZone.classList.remove("drag-over");

    const file = event.dataTransfer.files[0];

    if (file) {
        selectFile(file);
    }
});

// Importer le fichier vers Flask
uploadBtn.addEventListener("click", async () => {
    if (!selectedFile) {
        showMessage("Veuillez sélectionner un fichier.", "error");
        return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Importation en cours...";

    try {
        const response = await fetch("http://localhost:5000/api/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erreur lors de l'importation.");
        }

        showMessage(
            `Importation réussie ! ${data.logs_count} logs ont été importés.`,
            "success"
        );

        selectedFile = null;
        fileInput.value = "";
        fileInfo.classList.add("hidden");

    } catch (error) {
        showMessage(error.message, "error");
    } finally {
        uploadBtn.disabled = !selectedFile;
        uploadBtn.textContent = "Importer le fichier";
    }
});

// Afficher un message
function showMessage(message, type) {
    resultMessage.textContent = message;
    resultMessage.className = `result-message ${type}`;
}

