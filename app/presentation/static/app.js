const API = "/api/v1";
let token = localStorage.getItem("football_token") || "";
let teamsCache = [];

const $ = (id) => document.getElementById(id);

function showToast(msg, isError = false) {
  const el = $("toast");
  el.textContent = msg;
  el.className = isError ? "toast error" : "toast";
  setTimeout(() => el.classList.add("hidden"), 4000);
}

async function apiFetch(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (options.body && !(options.body instanceof URLSearchParams)) {
    headers["Content-Type"] = "application/json";
  }
  const res = await fetch(`${API}${path}`, { ...options, headers });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `Xatolik: ${res.status}`);
  return data;
}

async function loadUser() {
  if (!token) {
    $("userBadge").textContent = "Mehmon (viewer)";
    $("logoutBtn").classList.add("hidden");
    return;
  }
  try {
    const me = await apiFetch("/auth/me");
    $("userBadge").textContent = `${me.username} (${me.role})`;
    $("logoutBtn").classList.remove("hidden");
  } catch {
    token = "";
    localStorage.removeItem("football_token");
    $("userBadge").textContent = "Mehmon (viewer)";
    $("logoutBtn").classList.add("hidden");
  }
}

async function loadMonitoring() {
  try {
    const health = await apiFetch("/monitoring/health/detailed");
    $("healthBadge").textContent = `● ${health.status.toUpperCase()} (${health.uptime_seconds}s)`;
    $("statRequests").textContent = health.total_requests;
    $("statDb").textContent = health.database === "connected" ? "Ulangan" : "Uzilgan";
  } catch {
    $("healthBadge").textContent = "● OFFLINE";
  }
}

async function loadTeams() {
  teamsCache = await apiFetch("/teams/");
  $("statTeams").textContent = teamsCache.length;

  const list = $("teamsList");
  list.innerHTML = teamsCache.length
    ? teamsCache
        .map(
          (t) => `<li>
            <span><strong>${t.name}</strong> <small>(${t.city})</small></span>
            <button class="btn btn-danger" onclick="deleteTeam(${t.id})">O‘chirish</button>
          </li>`
        )
        .join("")
    : `<li class="empty">Jamoalar yo‘q</li>`;

  const opts = teamsCache.map((t) => `<option value="${t.id}">${t.name}</option>`).join("");
  $("playerTeamSelect").innerHTML = opts || `<option value="">Avval jamoa qo‘shing</option>`;
  $("homeTeamSelect").innerHTML = opts;
  $("awayTeamSelect").innerHTML = opts;
}

window.deleteTeam = async (id) => {
  try {
    await apiFetch(`/teams/${id}`, { method: "DELETE" });
    showToast("Jamoa o‘chirildi");
    await refreshAll();
  } catch (err) {
    showToast(err.message, true);
  }
};

async function loadTournaments() {
  const tours = await apiFetch("/tournaments/");
  $("statTournaments").textContent = tours.length;

  const sel = $("tournamentSelect");
  const prev = sel.value;
  sel.innerHTML = tours.length
    ? tours.map((t) => `<option value="${t.id}">${t.name} (${t.season})</option>`).join("")
    : `<option value="">Turnir yo‘q</option>`;
  if (prev && tours.some((t) => String(t.id) === prev)) sel.value = prev;

  await loadStandingsAndMatches();
}

async function loadStandingsAndMatches() {
  const tourId = $("tournamentSelect").value;
  if (!tourId) {
    $("standingsBody").innerHTML = `<tr><td colspan="8" class="empty">Turnir mavjud emas</td></tr>`;
    $("matchesList").innerHTML = `<li class="empty">Uchrashuvlar yo‘q</li>`;
    return;
  }

  const scoring = $("scoringSelect").value;
  const standings = await apiFetch(`/tournaments/${tourId}/standings?scoring=${scoring}`);
  $("standingsBody").innerHTML = standings.length
    ? standings
        .map(
          (r, i) => `<tr>
            <td>${i + 1}</td><td><strong>${r.team_name}</strong></td>
            <td>${r.played}</td><td>${r.won}</td><td>${r.drawn}</td><td>${r.lost}</td>
            <td>${r.goal_difference > 0 ? "+" : ""}${r.goal_difference}</td>
            <td><strong>${r.points}</strong></td>
          </tr>`
        )
        .join("")
    : `<tr><td colspan="8" class="empty">Jadval bo‘sh</td></tr>`;

  const matches = await apiFetch(`/tournaments/${tourId}/matches`);
  const teamName = (id) => teamsCache.find((t) => t.id === id)?.name || `#${id}`;
  $("matchesList").innerHTML = matches.length
    ? matches
        .map(
          (m) => `<li>
            <span>${teamName(m.home_team_id)} <strong>${m.home_score}:${m.away_score}</strong> ${teamName(m.away_team_id)}
              <small>(${m.status})</small></span>
            <button class="btn btn-sm btn-outline" onclick="recordScore(${m.id})">Hisob</button>
          </li>`
        )
        .join("")
    : `<li class="empty">Uchrashuvlar belgilanmagan</li>`;
}

window.recordScore = async (matchId) => {
  const home = prompt("Mezbon jamoa gollari:", "2");
  const away = prompt("Mehmon jamoa gollari:", "1");
  if (home === null || away === null) return;
  try {
    await apiFetch(`/matches/${matchId}/result`, {
      method: "PATCH",
      body: JSON.stringify({ home_score: Number(home), away_score: Number(away) }),
    });
    showToast("Uchrashuv hisobi saqlandi!");
    await refreshAll();
  } catch (err) {
    showToast(err.message, true);
  }
};

async function loadNotifications() {
  const notifs = await apiFetch("/notifications/");
  const list = $("notificationsList");
  list.innerHTML = notifs.length
    ? notifs
        .slice()
        .reverse()
        .map(
          (n) => `<li>
            <strong>${n.event_type}</strong>
            <span>${n.message}</span>
            <span class="feed-meta">${n.timestamp || ""}</span>
          </li>`
        )
        .join("")
    : `<li class="empty">Hozircha hodisalar yo‘q</li>`;
}

async function refreshAll() {
  await Promise.all([loadUser(), loadTeams(), loadNotifications()]);
  await loadTournaments();
  await loadMonitoring();
}

// Hodisa tinglovchilari
$("authToggleBtn").onclick = () => $("authCard").classList.toggle("hidden");
$("closeAuthBtn").onclick = () => $("authCard").classList.add("hidden");
$("logoutBtn").onclick = () => {
  token = "";
  localStorage.removeItem("football_token");
  showToast("Tizimdan chiqildi");
  loadUser();
};

$("loginForm").onsubmit = async (e) => {
  e.preventDefault();
  try {
    const body = new URLSearchParams({
      username: $("loginUsername").value,
      password: $("loginPassword").value,
    });
    const data = await apiFetch("/auth/login", { method: "POST", body });
    token = data.access_token;
    localStorage.setItem("football_token", token);
    $("authCard").classList.add("hidden");
    showToast("Muvaffaqiyatli kirildi!");
    await refreshAll();
  } catch (err) {
    showToast(err.message, true);
  }
};

$("registerForm").onsubmit = async (e) => {
  e.preventDefault();
  try {
    await apiFetch("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        username: $("regUsername").value,
        email: $("regEmail").value,
        password: $("regPassword").value,
        role: $("regRole").value,
      }),
    });
    showToast("Ro‘yxatdan o‘tildi! Endi chap tomondan login qiling.");
    $("registerForm").reset();
  } catch (err) {
    showToast(err.message, true);
  }
};

$("teamForm").onsubmit = async (e) => {
  e.preventDefault();
  try {
    await apiFetch("/teams/", {
      method: "POST",
      body: JSON.stringify({ name: $("teamName").value, city: $("teamCity").value }),
    });
    $("teamForm").reset();
    showToast("Yangi jamoa qo‘shildi!");
    await refreshAll();
  } catch (err) {
    showToast(err.message, true);
  }
};

$("tournamentForm").onsubmit = async (e) => {
  e.preventDefault();
  try {
    await apiFetch("/tournaments/", {
      method: "POST",
      body: JSON.stringify({ name: $("tourName").value, season: $("tourSeason").value }),
    });
    $("tournamentForm").reset();
    showToast("Yangi turnir yaratildi!");
    await refreshAll();
  } catch (err) {
    showToast(err.message, true);
  }
};

$("playerForm").onsubmit = async (e) => {
  e.preventDefault();
  try {
    await apiFetch("/players/", {
      method: "POST",
      body: JSON.stringify({
        full_name: $("playerName").value,
        team_id: Number($("playerTeamSelect").value),
        jersey_number: Number($("playerNumber").value),
        position: $("playerPos").value,
      }),
    });
    $("playerForm").reset();
    showToast("O‘yinchi muvaffaqiyatli qo‘shildi!");
    await loadMonitoring();
  } catch (err) {
    showToast(err.message, true);
  }
};

$("matchForm").onsubmit = async (e) => {
  e.preventDefault();
  const tourId = $("tournamentSelect").value;
  if (!tourId) return showToast("Avval turnir yarating!", true);
  try {
    await apiFetch("/matches/", {
      method: "POST",
      body: JSON.stringify({
        tournament_id: Number(tourId),
        home_team_id: Number($("homeTeamSelect").value),
        away_team_id: Number($("awayTeamSelect").value),
      }),
    });
    showToast("Uchrashuv belgilandi!");
    await refreshAll();
  } catch (err) {
    showToast(err.message, true);
  }
};

$("tournamentSelect").onchange = loadStandingsAndMatches;
$("scoringSelect").onchange = loadStandingsAndMatches;
$("refreshStandingsBtn").onclick = loadStandingsAndMatches;
$("refreshNotifBtn").onclick = loadNotifications;

refreshAll();