import { expensesChartConfig } from '../config/chartConfig.js';
import { initializeChart } from '../utils/chartUtils.js';

export function initializeExpensesChart() {
    const ctx = document.getElementById('expensesPieChart').getContext('2d');
    return initializeChart(ctx, expensesChartConfig);
}