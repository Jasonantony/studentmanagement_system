const ctx = document.getElementById('revenueChart').getContext('2d');
new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Paid Students', 'Unpaid Students'],
        datasets: [{
            data: [parseInt('{{ paid_students|safe }}'), parseInt('{{ unpaid_students|safe }}')],
            backgroundColor: ['#00ff99', '#ff6666'],
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { labels: { color: 'white' } }
        }
    }
});
