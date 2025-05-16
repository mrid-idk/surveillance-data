let allData = [];
let calendar;

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch ${url}`);
  return res.json();
}

async function loadAllData() {
  const indexList = await fetchJSON('data_json/index.json');
  const datasets = await Promise.all(
    indexList.map(filename => fetchJSON(`data_json/${filename}`))
  );
  allData = datasets.flat();
}

function filterData(stockSymbol, date) {
  return allData.filter(item => {
    const symbolMatch = stockSymbol ? item.SYMBOL.toLowerCase().includes(stockSymbol.toLowerCase()) : true;
    const dateMatch = date ? item.DATE === date : true;
    return symbolMatch && dateMatch;
  });
}

function groupByDate(data) {
  const summary = {};
  data.forEach(item => {
    const d = item.DATE;
    if (!summary[d]) summary[d] = { REG_FLAG: 0, ASM_STAGE_1: 0, ASM_STAGE_2: 0, total: 0 };
    if (item.REG_FLAG === '1') summary[d].REG_FLAG += 1;
    if (item.ASM_STAGE === '1') summary[d].ASM_STAGE_1 += 1;
    if (item.ASM_STAGE === '2') summary[d].ASM_STAGE_2 += 1;
    summary[d].total += 1;
  });
  return summary;
}

function renderCalendar(data) {
  const events = [];
  const summary = groupByDate(data);
  for (const [date, counts] of Object.entries(summary)) {
    const title = `REG: ${counts.REG_FLAG}, ASM1: ${counts.ASM_STAGE_1}, ASM2: ${counts.ASM_STAGE_2}`;
    events.push({ title, date, allDay: true });
  }

  if (calendar) calendar.destroy();

  const calendarEl = document.getElementById('calendar');
  calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events,
    height: 500,
  });
  calendar.render();
}

function renderSummary(data) {
  const container = document.getElementById('summary');
  const summary = groupByDate(data);
  container.innerHTML = '<h3>Daily Aggregated Indicator Counts</h3>';

  for (const [date, counts] of Object.entries(summary)) {
    const div = document.createElement('div');
    div.textContent = `${date} - REG: ${counts.REG_FLAG}, ASM1: ${counts.ASM_STAGE_1}, ASM2: ${counts.ASM_STAGE_2}, Total: ${counts.total}`;
    container.appendChild(div);
  }
}

function onFilterChange() {
  const stockSymbol = document.getElementById('stockFilter').value.trim();
  const date = document.getElementById('dateFilter').value;
  const filtered = filterData(stockSymbol, date);
  renderCalendar(filtered);
  renderSummary(filtered);
}

window.addEventListener('DOMContentLoaded', async () => {
  try {
    await loadAllData();
    document.getElementById('stockFilter').addEventListener('input', onFilterChange);
    document.getElementById('dateFilter').addEventListener('change', onFilterChange);
    onFilterChange(); // initial render
  } catch (e) {
    alert('Error loading data: ' + e.message);
  }
});
