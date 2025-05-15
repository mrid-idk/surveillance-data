// script.js

const dateInput = document.getElementById('date-select');
const stockSearch = document.getElementById('stock-search');
const filterInput = document.getElementById('filter-input');
const tableBody = document.querySelector('#indicators-table tbody');

let currentData = [];

// Format date like DDMMYY (e.g. 020425 for 2nd April 2025)
function formatDateToFilename(dateStr) {
  const date = new Date(dateStr);
  const dd = String(date.getDate()).padStart(2, '0');
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const yy = String(date.getFullYear()).slice(-2);
  return `IND${dd}${mm}${yy}.json`;
}

// Load JSON data for selected date
async function loadData(dateStr) {
  if (!dateStr) return;
  const filename = formatDateToFilename(dateStr);
  try {
    const response = await fetch(`data_json/${filename}`);
    if (!response.ok) throw new Error('File not found');
    const data = await response.json();
    currentData = data;
    renderTable(data);
  } catch (err) {
    tableBody.innerHTML = `<tr><td colspan="10">No data for selected date</td></tr>`;
    currentData = [];
  }
}

// Render stocks and indicators into the table
function renderTable(data) {
  tableBody.innerHTML = '';
  data.forEach(stock => {
    const tr = document.createElement('tr');
    // Assuming JSON structure has stock symbol and some indicators like indicator1, indicator2...
    tr.innerHTML = `
      <td>${stock.symbol}</td>
      <td>${stock.indicator1 || '-'}</td>
      <td>${stock.indicator2 || '-'}</td>
      <td>${stock.indicator3 || '-'}</td>
      <!-- add more columns as per your JSON structure -->
    `;
    tableBody.appendChild(tr);
  });
  applyFilters();
}

// Filter table rows based on search inputs
function applyFilters() {
  const stockFilter = stockSearch.value.toLowerCase();
  const indicatorFilter = filterInput.value.toLowerCase();

  Array.from(tableBody.rows).forEach(row => {
    const stockName = row.cells[0].textContent.toLowerCase();
    const indicatorText = Array.from(row.cells).slice(1).map(td => td.textContent.toLowerCase()).join(' ');
    if (stockName.includes(stockFilter) && indicatorText.includes(indicatorFilter)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

// Event listeners
dateInput.addEventListener('change', () => loadData(dateInput.value));
stockSearch.addEventListener('input', applyFilters);
filterInput.addEventListener('input', applyFilters);

// Optionally, load today’s data on page load
const todayStr = new Date().toISOString().slice(0, 10);
dateInput.value = todayStr;
loadData(todayStr);

