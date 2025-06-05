const ctx = document.getElementById('fraudRateChart').getContext('2d');

const fraudRateChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Fraud Rate',
            data: [],
            borderColor: 'red',
            borderWidth: 2,
            fill: false
        }]
    }
});

// Poll backend every 2.5 seconds for the per-day fraud rate chart
setInterval(() => {
    fetch('/api/fraud-rate')
        .then(res => res.json())
        .then(data => {
            fraudRateChart.data.labels = data.labels;
            fraudRateChart.data.datasets[0].data = data.values;
            fraudRateChart.update();
        });
}, 2500);


// poll backend every 2.5 seconds for the latest transactions
setInterval(() => {
    fetch('/api/transactions')
        .then(res => res.json())
        .then(data => {
            // Update metrics
            document.getElementById("total_tx").textContent = data.total_tx;
            document.getElementById("frauds").textContent = data.frauds;
            document.getElementById("fraud_rate").textContent = data.fraud_rate + "%";

            // Update transaction table
            const tableBody = document.getElementById("tx_table");
            tableBody.innerHTML = '';
            data.latest_transactions.forEach(tx => {
                const row = "<tr>\n"
                    + `<td>${tx.id}</td>\n`
                    + `<td>${tx.amount}</td>\n`
                    + `<td>${tx.fraud}</td>\n`
                    + `<td>${tx.time}</td>\n`
                    + `</tr>`;
                tableBody.innerHTML += row;
            });
        });
}, 2500)