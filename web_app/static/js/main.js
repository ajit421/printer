/**
 * GlassyPrint Hub - Client Logic
 */

let currentUploadedFile = null;

// DOM Elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const dropPrompt = document.getElementById('drop-prompt');
const uploadProgressBox = document.getElementById('upload-progress-box');
const uploadBar = document.getElementById('upload-bar');
const uploadFilename = document.getElementById('upload-filename');

const previewBox = document.getElementById('preview-box');
const previewImage = document.getElementById('preview-image');
const previewGeneric = document.getElementById('preview-generic');
const previewGenericName = document.getElementById('preview-generic-name');
const metaFilename = document.getElementById('meta-filename');
const metaFilesize = document.getElementById('meta-filesize');
const btnClearFile = document.getElementById('btn-clear-file');

const printForm = document.getElementById('print-form');
const btnPrint = document.getElementById('btn-print');
const copiesInput = document.getElementById('copies');
const btnMinus = document.getElementById('btn-minus');
const btnPlus = document.getElementById('btn-plus');

const queueList = document.getElementById('queue-list');
const emptyQueueMsg = document.getElementById('empty-queue-msg');
const queueCountBadge = document.getElementById('queue-count-badge');
const btnRefreshJobs = document.getElementById('btn-refresh-jobs');

const printerStatusText = document.getElementById('printer-status-text');
const printerStatusPill = document.getElementById('printer-status-pill');
const selectedPrinterBadge = document.getElementById('selected-printer-badge');

const globalModal = document.getElementById('global-modal');
const btnGlobalModal = document.getElementById('btn-global-modal');
const btnCloseModal = document.getElementById('btn-close-modal');

// Toast Notification
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Stepper
btnMinus.addEventListener('click', () => {
  let val = parseInt(copiesInput.value) || 1;
  if (val > 1) copiesInput.value = val - 1;
});

btnPlus.addEventListener('click', () => {
  let val = parseInt(copiesInput.value) || 1;
  if (val < 99) copiesInput.value = val + 1;
});

// Drag and drop events
['dragenter', 'dragover'].forEach(eventName => {
  dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('drag-over');
  });
});

['dragleave', 'drop'].forEach(eventName => {
  dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-over');
  });
});

dropZone.addEventListener('drop', (e) => {
  const dt = e.dataTransfer;
  const files = dt.files;
  if (files && files.length > 0) {
    handleFileUpload(files[0]);
  }
});

fileInput.addEventListener('change', (e) => {
  if (fileInput.files && fileInput.files.length > 0) {
    handleFileUpload(fileInput.files[0]);
  }
});

function handleFileUpload(file) {
  const formData = new FormData();
  formData.append('file', file);

  dropPrompt.style.display = 'none';
  uploadProgressBox.style.display = 'block';
  uploadFilename.textContent = `Uploading ${file.name}...`;
  uploadBar.style.width = '30%';

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/api/upload-preview', true);

  xhr.upload.onprogress = (e) => {
    if (e.lengthComputable) {
      const percent = (e.loaded / e.total) * 100;
      uploadBar.style.width = `${Math.max(30, percent)}%`;
    }
  };

  xhr.onload = () => {
    if (xhr.status === 200) {
      const resp = JSON.parse(xhr.responseText);
      currentUploadedFile = resp;
      showToast(`Uploaded "${file.name}" ready for printing!`, 'success');
      displayPreview(resp);
    } else {
      let err = 'Upload failed';
      try { err = JSON.parse(xhr.responseText).error || err; } catch (e) {}
      showToast(err, 'error');
      resetUploadZone();
    }
  };

  xhr.onerror = () => {
    showToast('Network error during upload', 'error');
    resetUploadZone();
  };

  xhr.send(formData);
}

function displayPreview(data) {
  dropZone.style.display = 'none';
  previewBox.style.display = 'block';

  metaFilename.textContent = data.original_name;
  metaFilesize.textContent = `${data.size_kb} KB`;

  if (data.preview_url) {
    previewImage.src = data.preview_url;
    previewImage.style.display = 'block';
    previewGeneric.style.display = 'none';
  } else {
    previewImage.style.display = 'none';
    previewGeneric.style.display = 'flex';
    previewGenericName.textContent = data.original_name;
  }

  btnPrint.disabled = false;
}

function resetUploadZone() {
  currentUploadedFile = null;
  fileInput.value = '';
  dropZone.style.display = 'flex';
  dropPrompt.style.display = 'block';
  uploadProgressBox.style.display = 'none';
  uploadBar.style.width = '0%';
  previewBox.style.display = 'none';
  btnPrint.disabled = true;
}

btnClearFile.addEventListener('click', resetUploadZone);

// Dispatch Print Job
btnPrint.addEventListener('click', async () => {
  if (!currentUploadedFile) {
    showToast('Please upload a file first', 'error');
    return;
  }

  const colorMode = document.querySelector('input[name="color_mode"]:checked').value;
  const copies = parseInt(copiesInput.value) || 1;
  const mediaSize = document.getElementById('media_size').value;
  const orientation = document.querySelector('input[name="orientation"]:checked').value;
  const pageRange = document.getElementById('page_range').value;
  const printerName = selectedPrinterBadge.textContent.trim() || 'Brother_DCP_T236';

  btnPrint.disabled = true;
  btnPrint.innerHTML = '<span>Sending to Spooler...</span>';

  try {
    const res = await fetch('/api/print', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        filename: currentUploadedFile.saved_filename,
        display_name: currentUploadedFile.original_name,
        printer_name: printerName,
        color_mode: colorMode,
        copies: copies,
        media_size: mediaSize,
        orientation: orientation,
        page_range: pageRange
      })
    });

    const data = await res.json();
    if (res.ok) {
      showToast(`Print job dispatched to Brother DCP-T236!`, 'success');
      fetchJobs();
    } else {
      showToast(data.error || 'Failed to print', 'error');
    }
  } catch (err) {
    showToast('Failed to reach server: ' + err.message, 'error');
  } finally {
    btnPrint.disabled = false;
    btnPrint.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="6 9 6 2 18 2 18 9"></polyline>
        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
        <rect x="6" y="14" width="12" height="8"></rect>
      </svg>
      <span>Dispatch Print Job</span>
    `;
  }
});

// Fetch & Update Jobs
async function fetchJobs() {
  try {
    const res = await fetch('/api/jobs');
    const data = await res.json();
    renderJobs(data.jobs || []);
  } catch (err) {
    console.error('Error fetching jobs:', err);
  }
}

function renderJobs(jobs) {
  const activeCount = jobs.filter(j => j.status === 'Printing' || j.status === 'Queued').length;
  queueCountBadge.textContent = `${activeCount} active`;

  if (jobs.length === 0) {
    emptyQueueMsg.style.display = 'flex';
    queueList.querySelectorAll('.job-item').forEach(el => el.remove());
    return;
  }

  emptyQueueMsg.style.display = 'none';
  queueList.querySelectorAll('.job-item').forEach(el => el.remove());

  jobs.forEach(job => {
    const item = document.createElement('div');
    item.className = 'job-item';
    item.innerHTML = `
      <div class="job-info">
        <div class="job-name">${escapeHtml(job.display_name || job.filename)}</div>
        <div class="job-subtext">
          ${job.copies} copy (${job.media_size}, ${job.color_mode}) • Submitted at ${job.submitted_at}
        </div>
      </div>
      <div style="display: flex; align-items: center; gap: 12px;">
        <span class="job-status-pill ${job.status}">${job.status}</span>
        ${job.status === 'Printing' ? `
          <button class="glass-btn btn-sm" onclick="cancelJob('${job.id}')" title="Cancel print job">Cancel</button>
        ` : ''}
      </div>
    `;
    queueList.appendChild(item);
  });
}

async function cancelJob(jobId) {
  try {
    const res = await fetch(`/api/jobs/${jobId}/cancel`, { method: 'POST' });
    if (res.ok) {
      showToast('Job cancelled', 'success');
      fetchJobs();
    }
  } catch (e) {
    showToast('Failed to cancel job', 'error');
  }
}

// Fetch Status
async function fetchStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    if (data.printers && data.printers.length > 0) {
      const p = data.printers[0];
      printerStatusText.textContent = `${p.name} • ${p.status}`;
      selectedPrinterBadge.textContent = p.name;
    }
  } catch (err) {
    printerStatusText.textContent = 'Server Offline';
  }
}

// Modals
btnGlobalModal.addEventListener('click', () => {
  globalModal.style.display = 'flex';
});

btnCloseModal.addEventListener('click', () => {
  globalModal.style.display = 'none';
});

globalModal.addEventListener('click', (e) => {
  if (e.target === globalModal) globalModal.style.display = 'none';
});

btnRefreshJobs.addEventListener('click', fetchJobs);

function escapeHtml(str) {
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}

// Initial Run and intervals
fetchStatus();
fetchJobs();
setInterval(fetchJobs, 3000);
setInterval(fetchStatus, 10000);

