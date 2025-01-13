import { recentExpenses } from '../data/expensesData.js';

export function initializeExpensesTable() {
    const tbody = document.querySelector('#expensesTable tbody');
    
    recentExpenses.forEach(expense => {
        const row = document.createElement('tr');
        const date = new Date(expense.date).toLocaleDateString();
        
        row.innerHTML = `
            <td class="date">${date}</td>
            <td class="description">${expense.description}</td>
            <td class="category"><span class="category-tag">${expense.category}</span></td>
            <td class="amount">$${expense.amount.toFixed(2)}</td>
        `;
        
        tbody.appendChild(row);
    });
}