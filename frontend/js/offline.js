const OFFLINE_QUEUE_KEY = "healthtriage_offline_queue";


function getOfflineQueue() {
    try {
        return JSON.parse(
            localStorage.getItem(OFFLINE_QUEUE_KEY)
        ) || [];
    } catch (error) {
        console.error("Could not read offline queue:", error);
        return [];
    }
}


function saveOfflineCase(caseData) {
    const queue = getOfflineQueue();

    const offlineCase = {
        offline_id: "OFF-" + Date.now(),
        created_at: new Date().toISOString(),
        sync_status: "pending",
        data: caseData
    };

    queue.push(offlineCase);

    localStorage.setItem(
        OFFLINE_QUEUE_KEY,
        JSON.stringify(queue)
    );

    console.log("Case saved offline:", offlineCase.offline_id);

    return offlineCase;
}


function removeOfflineCase(offlineId) {
    const queue = getOfflineQueue();

    const updatedQueue = queue.filter(
        item => item.offline_id !== offlineId
    );

    localStorage.setItem(
        OFFLINE_QUEUE_KEY,
        JSON.stringify(updatedQueue)
    );
}


async function syncOfflineCases() {

    const queue = getOfflineQueue();

    if (queue.length === 0) {
        return;
    }

    console.log(
        `Attempting to sync ${queue.length} offline case(s)...`
    );

    for (const offlineCase of queue) {

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/api/triage",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(
                        offlineCase.data
                    )
                }
            );

            if (response.ok) {

                const result = await response.json();

                console.log(
                    "Offline case synced:",
                    offlineCase.offline_id
                );

                removeOfflineCase(
                    offlineCase.offline_id
                );

                localStorage.setItem(
                    "lastSyncedTriage",
                    JSON.stringify(result)
                );

            } else {

                console.log(
                    "Sync failed:",
                    response.status
                );
            }

        } catch (error) {

            console.log(
                "Backend unavailable. Keeping case offline."
            );

            break;
        }
    }
}


window.addEventListener(
    "online",
    syncOfflineCases
);


window.addEventListener(
    "load",
    syncOfflineCases
);

window.saveOfflineCase = saveOfflineCase;
window.syncOfflineCases = syncOfflineCases;
window.getOfflineQueue = getOfflineQueue;