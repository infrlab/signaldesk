/* Centralized, same-origin API client: no API tokens are embedded in the browser. */
const api = {
  async request(path, options = {}) {
    const response = await fetch(`/api${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    });
    if (!response.ok) {
      let reason = 'Request failed';
      try {
        const detail = await response.json();
        reason = typeof detail.detail === 'string' ? detail.detail : JSON.stringify(detail.detail);
      } catch { /* Keep original message. */ }
      throw new Error(reason);
    }
    if (response.status === 204) return null;
    return response.json();
  },
  list(query = '', status = '') {
    const params = new URLSearchParams({ q: query, ...(status ? { status } : {}) });
    return this.request(`/contacts?${params}`);
  },
  summary() { return this.request('/summary'); },
  create(data) { return this.request('/contacts', { method: 'POST', body: JSON.stringify(data) }); },
  update(id, data) { return this.request(`/contacts/${id}`, { method: 'PATCH', body: JSON.stringify(data) }); },
  delete(id) { return this.request(`/contacts/${id}`, { method: 'DELETE' }); },
};

const $ = (id) => document.getElementById(id);
const labels = { planned: 'Planned', sent: 'Sent', replied: 'Replied', confirmed: 'Confirmed', closed: 'Closed' };
let contacts = [];
let editing = null;
let readOnly = false;

function showBanner(message, error = false) {
  const banner = $('banner');
  banner.hidden = false;
  banner.textContent = message;
  banner.classList.toggle('error', error);
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function renderContacts() {
  const target = $('contactsBody');
  target.replaceChildren();
  $('recordCount').textContent = `${contacts.length} RECORDS`;
  if (!contacts.length) {
    const tr = el('tr');
    const td = el('td', 'empty', 'No matching contacts. Try another search or add an outlet.');
    td.colSpan = 5;
    tr.append(td);
    target.append(tr);
    return;
  }
  for (const contact of contacts) {
    const tr = el('tr');
    const title = el('td');
    title.append(el('span', 'outlet', contact.outlet));
    if (contact.notes) title.append(el('span', 'note', contact.notes));
    tr.append(title);
    tr.append(el('td', 'channel', contact.channel));
    const state = el('td');
    state.append(el('span', `status-pill status-${contact.status}`, labels[contact.status]));
    tr.append(state);
    tr.append(el('td', '', contact.due_date || '—'));
    const actions = el('td', 'right');
    if (!readOnly) {
      const edit = el('button', 'action', 'Edit');
      edit.type = 'button';
      edit.addEventListener('click', () => openEditor(contact));
      const remove = el('button', 'action danger', 'Delete');
      remove.type = 'button';
      remove.addEventListener('click', () => removeContact(contact));
      actions.append(edit, remove);
    } else {
      actions.append(el('span', 'note', 'Read-only demo'));
    }
    tr.append(actions);
    target.append(tr);
  }
}

async function refresh() {
  try {
    const [list, summary] = await Promise.all([
      api.list($('searchInput').value.trim(), $('filterStatus').value),
      api.summary(),
    ]);
    contacts = list;
    $('statTotal').textContent = summary.total;
    $('statSent').textContent = summary.by_status.sent;
    $('statReplied').textContent = summary.by_status.replied;
    $('statConfirmed').textContent = summary.by_status.confirmed;
    renderContacts();
  } catch (error) { showBanner(`Could not load contacts: ${error.message}`, true); }
}

function openEditor(contact = null) {
  editing = contact;
  $('contactForm').reset();
  $('modalTitle').textContent = contact ? 'Edit contact' : 'Add a contact';
  $('saveButton').textContent = contact ? 'Save changes' : 'Save contact';
  $('formError').hidden = true;
  if (contact) {
    for (const field of ['outlet', 'channel', 'status', 'due_date', 'notes']) {
      $(field).value = contact[field] || '';
    }
  }
  $('contactDialog').showModal();
  $('outlet').focus();
}

async function removeContact(contact) {
  if (!confirm(`Delete ${contact.outlet}? This action cannot be undone.`)) return;
  try { await api.delete(contact.id); showBanner('Contact deleted.'); await refresh(); }
  catch (error) { showBanner(error.message, true); }
}

function parseForm() {
  return {
    outlet: $('outlet').value.trim(),
    channel: $('channel').value,
    status: $('status').value,
    due_date: $('due_date').value || null,
    notes: $('notes').value.trim(),
  };
}

async function saveForm(event) {
  event.preventDefault();
  const data = parseForm();
  if (data.outlet.length < 2) {
    $('formError').textContent = 'Outlet name must be at least two characters.';
    $('formError').hidden = false;
    return;
  }
  $('saveButton').disabled = true;
  try {
    if (editing) await api.update(editing.id, data);
    else await api.create(data);
    $('contactDialog').close();
    showBanner(editing ? 'Contact updated.' : 'Contact added.');
    await refresh();
  } catch (error) {
    $('formError').textContent = error.message;
    $('formError').hidden = false;
  } finally { $('saveButton').disabled = false; }
}

let debounceTimer;
$('searchInput').addEventListener('input', () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(refresh, 160);
});
$('filterStatus').addEventListener('change', refresh);
$('newButton').addEventListener('click', () => openEditor());
$('closeButton').addEventListener('click', () => $('contactDialog').close());
$('cancelButton').addEventListener('click', () => $('contactDialog').close());
$('contactForm').addEventListener('submit', saveForm);

// A public demo should be read-only; the Docker Compose local app remains writable.
fetch('/health').then(async (r) => {
  if (!r.ok) throw new Error('Health check failed');
  const payload = await r.json();
  return payload;
}).catch(() => showBanner('Service connection is unavailable.', true));

// Server signals write policy using harmless OPTIONS? Use a direct read-only feature flag in page state.
fetch('/api/config').then((r) => r.json()).then((config) => {
  readOnly = Boolean(config.read_only);
  document.body.classList.toggle('readonly', readOnly);
  if (readOnly) showBanner('Public portfolio demo: sample data is read-only. Run locally to create or edit records.');
  refresh();
}).catch(() => refresh());
