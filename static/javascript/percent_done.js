async function makeRequest(url, method, body) {
    let headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-type': 'application/json'
    }

    let response = await fetch(url, {
        method: method,
        headers: headers,
        body: body
    })

    return await response.json()
}

async function getPercentDone() {
    const data = await makeRequest('/get_percent_done', 'get')
    let percent_done = document.getElementById('progress-bar')
    percent_done.style = `width: ${await data['percent_done']}%;`
    percent_done.innerHTML = `${await data['percent_done']}%`
    setTimeout(getPercentDone, 60000)
}

getPercentDone()