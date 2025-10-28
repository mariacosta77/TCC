// Salva o checklist e o progresso no calendário
const salvarBtn = document.getElementById('salvar');
const checkboxes = document.querySelectorAll('#checklist input[type="checkbox"]');
const calendar = document.getElementById('calendar');

const hoje = new Date().toISOString().split('T')[0];
const savedData = JSON.parse(localStorage.getItem('checklistData')) || {};
const completedDays = JSON.parse(localStorage.getItem('completedDays')) || [];

// Restaurar checklist salvo
checkboxes.forEach(chk => {
    if (savedData[chk.dataset.item]) chk.checked = true;
});

// Gerar calendário do mês atual
const date = new Date();
const year = date.getFullYear();
const month = date.getMonth();
const firstDay = new Date(year, month, 1);
const lastDay = new Date(year, month + 1, 0);

for (let d = 1; d <= lastDay.getDate(); d++) {
    const dayElem = document.createElement('div');
    dayElem.textContent = d;
    dayElem.classList.add('day');
    const fullDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    if (completedDays.includes(fullDate)) dayElem.classList.add('completed');
    calendar.appendChild(dayElem);
}

// Função salvar
salvarBtn.addEventListener('click', () => {
    const data = {};
    let allChecked = true;

    checkboxes.forEach(chk => {
        data[chk.dataset.item] = chk.checked;
        if (!chk.checked) allChecked = false;
    });

    localStorage.setItem('checklistData', JSON.stringify(data));

    if (allChecked) {
        if (!completedDays.includes(hoje)) {
            completedDays.push(hoje);
            localStorage.setItem('completedDays', JSON.stringify(completedDays));
            alert('Checklist completo salvo! 🎉');
            location.reload();
        }
    } else {
        alert('Checklist salvo parcialmente!');
    }
});

// ====== CALENDÁRIO INTERATIVO ======
const calendar = document.getElementById("calendar");
const monthYear = document.getElementById("monthYear");
const prevMonth = document.getElementById("prevMonth");
const nextMonth = document.getElementById("nextMonth");
const prevYear = document.getElementById("prevYear");
const nextYear = document.getElementById("nextYear");

let currentDate = new Date();
let completedDays = JSON.parse(localStorage.getItem("completedDays")) || [];

// Renderiza o calendário
function renderCalendar() {
  calendar.innerHTML = "";

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const firstWeekday = firstDay.getDay();

  const monthNames = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
  ];

  monthYear.textContent = `${monthNames[month]} de ${year}`;

  const weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
  weekdays.forEach(dia => {
    const cell = document.createElement("div");
    cell.textContent = dia;
    cell.classList.add("weekday");
    calendar.appendChild(cell);
  });

  for (let i = 0; i < firstWeekday; i++) {
    const empty = document.createElement("div");
    calendar.appendChild(empty);
  }

  for (let d = 1; d <= lastDay.getDate(); d++) {
    const day = document.createElement("div");
    day.textContent = d;
    day.classList.add("day");

    const fullDate = `${year}-${String(month + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
    const today = new Date().toISOString().split("T")[0];

    if (fullDate === today) day.classList.add("today");
    if (completedDays.includes(fullDate)) day.classList.add("completed");

    calendar.appendChild(day);
  }
}

// Botões de navegação
prevMonth.addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() - 1);
  renderCalendar();
});

nextMonth.addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() + 1);
  renderCalendar();
});

prevYear.addEventListener("click", () => {
  currentDate.setFullYear(currentDate.getFullYear() - 1);
  renderCalendar();
});

nextYear.addEventListener("click", () => {
  currentDate.setFullYear(currentDate.getFullYear() + 1);
  renderCalendar();
});

renderCalendar();

// Integração com checklist salvo
document.getElementById("salvar").addEventListener("click", () => {
  const checkboxes = document.querySelectorAll('#checklist input[type="checkbox"]');
  let allChecked = true;

  checkboxes.forEach(chk => {
    if (!chk.checked) allChecked = false;
  });

  const hoje = new Date().toISOString().split("T")[0];

  if (allChecked) {
    if (!completedDays.includes(hoje)) {
      completedDays.push(hoje);
      localStorage.setItem("completedDays", JSON.stringify(completedDays));
      alert("✅ Checklist completo! Dia marcado no calendário.");
      renderCalendar();
    }
  } else {
    alert("Checklist salvo parcialmente!");
  }
});
