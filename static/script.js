/* ── API helper ─────────────────────────────────────────── */
const BASE = '';

async function api(method, path, body) {
    const h = { 'Content-Type': 'application/json' };
    const t = localStorage.getItem('token');
    if (t) h['Authorization'] = 'Bearer ' + t;
    const r = await fetch(BASE + path, { method, headers: h, body: body ? JSON.stringify(body) : null });
    if (r.status === 401) { localStorage.clear(); location.href = '/login'; }
    const d = await r.json().catch(() => ({}));
    if (!r.ok) throw d.detail || 'Error';
    return d;
}

/* ── Shared helpers ─────────────────────────────────────── */
function msg(id, text, type) {
    const el = document.getElementById(id);
    if (el) { el.textContent = text; el.className = type || ''; }
}

function buildTable(rows) {
    if (!rows.length) return '<p class="muted">Nothing found.</p>';
    return '<table><tr><th>Name</th><th>Std</th><th>Roll</th><th>Marks</th><th>Per</th></tr>'
        + rows.map(s => `<tr>
            <td>${s.name || ''}</td>
            <td>${s.standard || ''}</td>
            <td>${s.roll_number || ''}</td>
            <td>${(s.marks || []).join(', ')}</td>
            <td>${s.percentage != null ? s.percentage.toFixed(1) + '%': '—'}</td>
          </tr>`).join('')
        + '</table>';
}

/* ── Dashboard logic ────────────────────────────────────── */
function logout() {
    localStorage.clear();
    location.href = '/login';
}

function show(name) {
    document.querySelectorAll('.nav a').forEach(a => a.classList.remove('active'));
    document.getElementById('n-' + name).classList.add('active');
    const p = document.getElementById('panel');
    if (name === 'view')       renderView(p);
    if (name === 'search')     renderSearch(p);
    if (name === 'percentage') renderPct(p);
    if (name === 'add')        renderAdd(p);
    if (name === 'delete')     renderDelete(p);
}

/* All students */
async function renderView(p) {
    p.innerHTML = '<h2>All Students</h2><p class="muted">Loading…</p>';
    try {
        const d = await api('GET', '/student/view_students');
        p.innerHTML = '<h2>All Students</h2>' + buildTable(Object.values(d));
    } catch (e) { p.innerHTML = '<p class="err">' + e + '</p>'; }
}

/* Search */
function renderSearch(p) {
    p.innerHTML = `
        <h2>Search by Name</h2>
        <div class="box">
            <div class="row">
                <input id="sn" placeholder="Name e.g. Asha" />
                <button onclick="doName()" style="width:auto;padding:8px 16px">Go</button>
            </div>
            <div id="r-name"></div>
        </div>
        <h2>Search by Roll</h2>
        <div class="box">
            <div class="row">
                <input id="ss" placeholder="Standard e.g. 10" />
                <input id="sr" placeholder="Roll e.g. 1" />
                <button onclick="doRoll()" style="width:auto;padding:8px 16px">Go</button>
            </div>
            <div id="r-roll"></div>
        </div>`;
}

async function doName() {
    const el = document.getElementById('r-name');
    try {
        const d = await api('GET', '/student/search_by_name?name=' + encodeURIComponent(document.getElementById('sn').value.trim()));
        el.innerHTML = buildTable(Object.values(d));
    } catch (e) { el.innerHTML = '<p class="err">' + e + '</p>'; }
}

async function doRoll() {
    const el = document.getElementById('r-roll');
    try {
        const d = await api('GET', '/student/search_by_roll?std=' + encodeURIComponent(document.getElementById('ss').value.trim()) + '&roll=' + encodeURIComponent(document.getElementById('sr').value.trim()));
        el.innerHTML = buildTable([d]);
    } catch (e) { el.innerHTML = '<p class="err">' + e + '</p>'; }
}

/* Percentage */
function renderPct(p) {
    p.innerHTML = `
        <h2>Get Percentage</h2>
        <div class="box">
            <input id="ps" placeholder="Standard" />
            <input id="pr" placeholder="Roll number" />
            <button onclick="doPct()">Calculate</button>
            <div id="r-pct"></div>
        </div>`;
}

async function doPct() {
    const el = document.getElementById('r-pct');
    try {
        const v = await api('GET', '/student/percent_student?std=' + encodeURIComponent(document.getElementById('ps').value.trim()) + '&roll=' + encodeURIComponent(document.getElementById('pr').value.trim()));
        el.innerHTML = '<br><strong style="font-size:24px">' + v.toFixed(1) + '%</strong>';
    } catch (e) { el.innerHTML = '<p class="err">' + e + '</p>'; }
}

/* Add student */
function renderAdd(p) {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user.role !== 'admin') {
        p.innerHTML = '<div class="box"><p class="err">Admin access required.</p></div>';
        return;
    }
    p.innerHTML = `
        <h2>Add Student</h2>
        <div class="box">
            <input id="an" placeholder="Full name" />
            <div class="row">
                <input id="astd" placeholder="Standard" />
                <input id="ar"   placeholder="Roll number" />
            </div>
            <input id="am" placeholder="Marks (e.g. 85 90 78)" />
            <button onclick="doAdd()">Add Student</button>
            <div id="r-add"></div>
        </div>`;
}

async function doAdd() {
    const marks = document.getElementById('am').value.trim().split(/[\s,]+/).map(Number).filter(n => !isNaN(n));
    const el = document.getElementById('r-add');
    try {
        await api('POST', '/admin/add_students', {
            name:  document.getElementById('an').value.trim(),
            std:   document.getElementById('astd').value.trim(),
            roll:  document.getElementById('ar').value.trim(),
            marks,
        });
        el.innerHTML = '<p class="ok">Student added.</p>';
        ['an', 'astd', 'ar', 'am'].forEach(id => document.getElementById(id).value = '');
    } catch (e) { el.innerHTML = '<p class="err">' + e + '</p>'; }
}

/* Delete student */
function renderDelete(p) {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user.role !== 'admin') {
        p.innerHTML = '<div class="box"><p class="err">Admin access required.</p></div>';
        return;
    }
    p.innerHTML = `
        <h2>Delete Student</h2>
        <div class="box">
            <div class="row">
                <input id="ds" placeholder="Standard" />
                <input id="dr" placeholder="Roll number" />
            </div>
            <button class="red" onclick="doDelete()">Delete</button>
            <div id="r-del"></div>
        </div>`;
}

async function doDelete() {
    const std  = document.getElementById('ds').value.trim();
    const roll = document.getElementById('dr').value.trim();
    if (!confirm('Delete student ' + std + '-' + roll + '?')) return;
    const el = document.getElementById('r-del');
    try {
        await api('DELETE', '/admin/delete_students?std=' + encodeURIComponent(std) + '&roll=' + encodeURIComponent(roll));
        el.innerHTML = '<p class="ok">Deleted.</p>';
        document.getElementById('ds').value = '';
        document.getElementById('dr').value = '';
    } catch (e) { el.innerHTML = '<p class="err">' + e + '</p>'; }
}