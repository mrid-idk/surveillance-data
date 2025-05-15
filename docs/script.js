async function fetchStockData(fileName) {
  const response = await fetch(`../data_json/${fileName}`);
  return await response.json();
}

function extractIndicators(data) {
  return data.map(entry => ({
    symbol: entry.SYMBOL,
    date: entry.DATE,
    indicators: {
      regFlag: entry.REG_FLAG,
      asmStage: entry.ASM_STAGE,
      gsmStage: entry.GSM_STAGE || null,
    }
  }));
}

function groupByDate(data) {
  const summary = {};

  data.forEach(entry => {
    const date = entry.date;
    if (!summary[date]) {
      summary[date] = {
        regCount: 0,
        asm1Count: 0,
        asm2Count: 0,
        total: 0,
      };
    }

    if (entry.indicators.regFlag === '1') summary[date].regCount += 1;
    if (entry.indicators.asmStage === '1') summary[date].asm1Count += 1;
    if (entry.indicators.asmStage === '2') summary[date].asm2Count += 1;
    summary[date].total += 1;
  });

  return summary;
}

function convertToCalendarEvents(summary) {
  return Object.entries(summary).map(([date, stats]) => ({
    title: `REG: ${stats.regCount}, ASM1: ${stats.asm1Count}, ASM2: ${stats.asm2Count}`,
    date,
    allDay: true
  }));
}

function displaySummary(summary) {
  const container = document.getElementById('indicatorSummary');
  container.innerHTML = '<h3>Daily Summary</h3>';
  Object.entries(summary).forEach(([date, stats]) => {
    const div = document.createElement('div');
    div.textContent = `${date}: REG=${stats.regCount}, ASM1=${stats.asm1Count}, ASM2=${stats.asm2Count}`;
    container.appendChild(div);
  });
}

function renderCalendar(events) {
  document.getElementById('calendar').innerHTML = '';
  const calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
    initialView: 'dayGridMonth',
    events: events
  });
  calendar.render();
}

document.getElementById('fileSelector').addEventListener('change', async function () {
  const file = this.value;
  const rawData = await fetchStockData(file);
  const indicators = extractIndicators(rawData);
  const summary = groupByDate(indicators);
  const events = convertToCalendarEvents(summary);

  renderCalendar(events);
  displaySummary(summary);
});

// Load default file on first render
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('fileSelector').dispatchEvent(new Event('change'));
});
