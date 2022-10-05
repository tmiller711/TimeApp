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

async function getTime() {
    const data = await makeRequest('/', 'get')
    let time_h1 = document.getElementById('time')
    let time_h2 = document.getElementById('time2')
    time_h1.innerHTML = await data['time']
    time_h2.innerHTML = await data['time']
    setTimeout(getTime, 30000)
}

getTime()