// Chart utility functions
export function handleChartResize(chart) {
    if (chart) {
        chart.resize();
    }
}

export function initializeChart(ctx, config) {
    const chart = new Chart(ctx, config);
    
    window.addEventListener('resize', () => handleChartResize(chart));
    
    return chart;
}