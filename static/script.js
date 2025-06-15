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

            // Update fraudulent transaction table
            const fraudulent_tx_table = document.getElementById("fraudulent_tx_table");
            fraudulent_tx_table.innerHTML = '';

            data.latest_fraudulent_transactions.forEach(tx => {
                const row = `
                            <tr>
                            <td>${tx.id}</td>
                            <td>${tx.amount}</td>
                            <td>${tx.fraud}</td>
                            <td>${tx.time}</td>
                            </tr>
                            `;
                fraudulent_tx_table.innerHTML += row;
            });

            // Update all transactions table
            const all_tx_table = document.getElementById('all_tx_table');
            all_tx_table.innerHTML = '';

            data.latest_transactions.forEach(tx => {
                const row = `
                            <tr>
                            <td>${tx.id}</td>
                            <td>${tx.amount}</td>
                            <td>${tx.fraud}</td>
                            <td>${tx.time}</td>
                            </tr>
                            `;
                all_tx_table.innerHTML += row;
            });

            // Update suspicious transactions table
            const suspicious_tx_table = document.getElementById('suspicious_tx_table');
            suspicious_tx_table.innerHTML = '';

            data.suspicious_transactions.forEach(tx => {
                const row = `
                            <tr>
                            <td>${tx.id}</td>
                            <td>${tx.amount}</td>
                            <td>${tx.fraud_score}</td>
                            <td>${tx.time}</td>
                            </tr>
                            `;
                suspicious_tx_table.innerHTML += row;
            });
        });
}, 2500)