document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', document.getElementById('data-file').files[0]);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    document.getElementById('results').innerText = JSON.stringify(data.results, null, 2);
    document.getElementById('plots').innerHTML = data.plots.map(p => `<img src="${p}">`).join('');
});
