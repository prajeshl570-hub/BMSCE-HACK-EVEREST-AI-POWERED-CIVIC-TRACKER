document.addEventListener("DOMContentLoaded", () => {
    // 1. Map Initialization [cite: 1177-1186]
    const map = L.map('map').setView([12.9716, 77.5946], 12);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);
    let heatLayer = L.heatLayer([], { radius: 35, blur: 25 }).addTo(map);

    // 2. Heatmap Refresh 
    async function updateHeatmap() {
        try {
            const res = await fetch("http://localhost:8000/get-locations");
            const data = await res.json();
            const points = data.map(r => [r.lat, r.lng, r.severity || 0.5]);
            heatLayer.setLatLngs(points);
        } catch (err) { console.error("Map Update Error:", err); }
    }
    updateHeatmap();
    setInterval(updateHeatmap, 10000);

    // 3. AI Submission Logic [cite: 78-130]
    const form = document.getElementById("submissionForm");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const submitBtn = form.querySelector("button[type='submit']");
        submitBtn.disabled = true;
        submitBtn.innerText = "Analyzing with AI...";

        navigator.geolocation.getCurrentPosition(async (pos) => {
            const formData = new FormData();
            formData.append("name", document.getElementById("name").value);
            formData.append("description", document.getElementById("description").value);
            formData.append("latitude", pos.coords.latitude);
            formData.append("longitude", pos.coords.longitude);
            formData.append("image", document.getElementById("image").files[0]);

            try {
                const res = await fetch("http://127.0.0.1:8000/upload", { method: "POST", body: formData });
                const result = await res.json();
                if (res.ok) {
                    alert(`Success: ${result.message}`);
                    bootstrap.Modal.getInstance(document.getElementById('reportModal')).hide();
                    form.reset();
                    updateHeatmap();
                } else {
                    alert(`Issue: ${result.detail || "AI verification failed."}`);
                }
            } catch (err) { alert("Backend server offline."); }
            finally { submitBtn.disabled = false; submitBtn.innerText = "Submit Report"; }
        }, () => { alert("Location access denied."); submitBtn.disabled = false; });
    });
});