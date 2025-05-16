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
    indexList.map(file => fetchJSON(`data_json/${file}`))
  );
  allData = datasets.flat();
}

function filterData(stock, date) {
  return allData.filter(entry => {
    const stockMatch = stock ? entry.SYMBOL.toLowerCase().includes(stock.toLowerCase()) : true;
    const dateMatch = date ? entry.DATE === date : true;
    return stockMatch && dateMatch;
  });
}

function groupByDate(data) {
  const summary = {};
  data.forEach(item => {
    const d = item.DATE;
    if (!summary[d]) summary[d] = { REG_FLAG: 0, ASM1: 0, ASM2: 0, total: 0 };
    if (item.REG_FLAG === '1') summary[d].REG_FLAG++;
    if (item.ASM_STAGE === '1') summary[d].ASM1++;
    if (item.ASM_STAGE === '2') summary[d].ASM2++;
    summary[d].total++;
  });
  return summary;
}

function renderCalendar(data) {
  const events = [];
  const grouped = groupByDate(data);
  for (const [date, count] of Object.entries(grouped)) {
    events.push({
      title: `REG: ${count.REG_FLAG}, ASM1: ${count.ASM1}, ASM2: ${count.ASM2}`,
      date,
      allDay: true
    });
  }

  if (calendar) calendar.destroy();
  calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
    initialView: 'dayGridMonth',
    events,
    height: 550
  });
  calendar.render();
}

function renderSummary(data) {
  const summaryEl = document.getElementById('summary');
  const grouped = groupByDate(data);
  summaryEl.innerHTML = `<h3>Indicator Summary</h3>`;
  Object.entries(grouped).forEach(([date, c]) => {
    const p = document.createElement('p');
    p.textContent = `${date}: REG=${c.REG_FLAG}, ASM1=${c.ASM1}, ASM2=${c.ASM2}, Total=${c.total}`;
    summaryEl.appendChild(p);
  });
}

function onFilter() {
  const stock = document.getElementById('stockFilter').value.trim();
  const date = document.getElementById('dateFilter').value;
  const filtered = filterData(stock, date);
  renderCalendar(filtered);
  renderSummary(filtered);
}

window.addEventListener('DOMContentLoaded', async () => {
  try {
    await loadAllData();
    document.getElementById('stockFilter').addEventListener('input', onFilter);
    document.getElementById('dateFilter').addEventListener('change', onFilter);
    onFilter(); // initial render
  } catch (err) {
    alert('Error loading data: ' + err.message);
  }
});
