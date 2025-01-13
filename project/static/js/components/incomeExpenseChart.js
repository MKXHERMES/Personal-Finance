import { incomeExpenseConfig } from '../config/chartConfig.js';
import { initializeChart } from '../utils/chartUtils.js';

export function initializeIncomeExpenseChart() {
    const ctx = document.getElementById('incomeExpenseChart').getContext('2d');
    return initializeChart(ctx, incomeExpenseConfig);
}