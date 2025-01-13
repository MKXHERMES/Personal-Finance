// Chart configuration and data
export const expensesChartConfig = {
    type: 'pie',
    data: {
        labels: ['Housing', 'Food', 'Transportation', 'Entertainment', 'Utilities'],
        datasets: [{
            data: [1200, 800, 600, 400, 450],
            backgroundColor: [
                '#10b981',
                '#3b82f6',
                '#f59e0b',
                '#ef4444',
                '#8b5cf6'
            ],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 10,
                    usePointStyle: true
                }
            }
        }
    }
};

export const incomeExpenseConfig = {
    type: 'bar',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June'],
        datasets: [
            {
                label: 'Income',
                data: [8250, 7800, 8500, 8100, 8600, 8250],
                backgroundColor: '#10b981',
                borderRadius: 4
            },
            {
                label: 'Expenses',
                data: [3450, 3200, 3800, 3300, 3600, 3450],
                backgroundColor: '#ef4444',
                borderRadius: 4
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'bottom'
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: value => 'Rs.' + value.toLocaleString()
                }
            }
        }
    }
};