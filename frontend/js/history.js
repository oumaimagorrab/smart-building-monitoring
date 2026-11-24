
const API_URL = "http://localhost:5000/api/uploads";

const historyTable = document.getElementById("historyTable");
const historyMessage = document.getElementById("historyMessage");

async function loadHistory() {
    historyTable.innerHTML = `
        <tr><td colspan="4">Chargement...</td></tr>
    `;

    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erreur de chargement.");
        }

        const uploads = data.uploads || [];

        displayHistory(uploads);

    } catch (error) {
        historyTable.innerHTML = `
            <tr><td colspan="4">Impossible de charger l'historique.</td></tr>
        `;
        historyMessage.textContent = error.message;
    }
}

function displayHistory(uploads) {
    historyTable.innerHTML = "";

    if (uploads.length === 0) {
        historyTable.innerHTML = `
            <tr><td colspan="4">Aucune importation enregistrée.</td></tr>
        `;
        historyMessage.textContent = "Aucune donnée disponible.";
        return;
    }

    uploads.forEach(upload => {
        const row = document.createElement("tr");

        const date = new Date(upload.date).toLocaleString("fr-FR");

        const values = [
            upload.filename || "-",
            date,
            upload.logs_count ?? 0
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        const statusCell = document.createElement("td");
        const status = document.createElement("span");

        status.textContent = upload.status || "Inconnu";
        status.className = upload.status === "success"
            ? "status-success"
            : "status-error";

        statusCell.appendChild(status);
        row.appendChild(statusCell);

        historyTable.appendChild(row);
    });

    historyMessage.textContent =
        `${uploads.length} importation(s) enregistrée(s).`;
}

// Charger l'historique à l'ouverture de la page
loadHistory();

