import { initializeExpensesChart } from './components/expensesChart.js';
import { initializeIncomeExpenseChart } from './components/incomeExpenseChart.js';
import { initializeExpensesTable } from './components/expensesTable.js';

document.addEventListener('DOMContentLoaded', () => {
    initializeExpensesChart();
    initializeIncomeExpenseChart();
    initializeExpensesTable();
});