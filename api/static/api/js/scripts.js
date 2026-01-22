document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('pieChart').getContext('2d');
    const pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Happy', 'Stressed', 'Calm'],
            datasets: [{
                data: [70, 15, 15],  // Hardcoded; fetch from API later
                backgroundColor: ['#FFD700', '#FFA500', '#00BFA5'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
});