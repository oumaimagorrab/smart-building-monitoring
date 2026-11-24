
const API_URL = "http://localhost:5000/api/logs";

const logsTable = document.getElementById("logsTable");
const message = document.getElementById("message");

const sensorFilter = document.getElementById("sensorFilter");
const zoneFilter = document.getElementById("zoneFilter");
const typeFilter = document.getElementById("typeFilter");

const searchBtn = document.getElementById("searchBtn");
const resetBtn = document.getElementById("resetBtn");

// Récupérer et afficher les logs
async function loadLogs() {
    logsTable.innerHTML = `
        <tr><td colspan="7">Chargement...</td></tr>
    `;
    message.textContent = "";

    const params = new URLSearchParams();

    if (sensorFilter.value.trim()) {
        params.append("sensor_id", sensorFilter.value.trim());
    }

    if (zoneFilter.value.trim()) {
        params.append("zone", zoneFilter.value.trim());
    }

    if (typeFilter.value.trim()) {
        params.append("log_type", typeFilter.value.trim());
    }

    try {
        const response = await fetch(`${API_URL}?${params.toString()}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erreur lors du chargement.");
        }

        const logs = data.logs || [];
        displayLogs(logs);

    } catch (error) {
        logsTable.innerHTML = `
            <tr><td colspan="7">Impossible de charger les logs.</td></tr>
        `;
        message.textContent = error.message;
    }
}

// Afficher les logs dans le tableau
function displayLogs(logs) {
    logsTable.innerHTML = "";

    if (logs.length === 0) {
        logsTable.innerHTML = `
            <tr><td colspan="7">Aucun log trouvé.</td></tr>
        `;
        return;
    }

    logs.forEach(log => {
        const row = document.createElement("tr");

        const values = [
            log["@timestamp"] || log.timestamp || "-",
            log.sensor_id || "-",
            log.zone || "-",
            log.log_type || "-",
            log.temperature ?? "-",
            log.humidity ?? "-",
            log.co2 ?? "-"
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        logsTable.appendChild(row);
    });

    message.textContent = `${logs.length} log(s) trouvé(s).`;
}

// Bouton de recherche
searchBtn.addEventListener("click", loadLogs);

// Bouton de réinitialisation
resetBtn.addEventListener("click", () => {
    sensorFilter.value = "";
    zoneFilter.value = "";
    typeFilter.value = "";
    loadLogs();
});

// Charger les logs dès l'ouverture de la page
loadLogs();

